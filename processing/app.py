import connexion
import datetime
import json
import swagger_ui_bundle
import yaml
import logging
import logging.config
import requests
import os
import sqlite3

from apscheduler.schedulers.background import BackgroundScheduler
from base import Base
from connexion import NoContent
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from stats import Stats


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                  'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()


def create_database():
    conn = sqlite3.connect(DATABASE)

    c = conn.cursor()
    c.execute('''
            CREATE TABLE stats
            (id INTEGER PRIMARY KEY ASC,
            total_expense DECIMAL NOT NULL,
            total_item VARCHAR(100) NOT NULL,
            popular_item VARCHAR(100) NOT NULL,
            max_quantity INT NOT NULL,
            daily_revenue DECIMAL NOT NULL,
            last_updated VARCHAR(100) NOT NULL)
            ''')
    conn.commit()
    conn.close()

    logger.info("Database created.")


def populate_stats():
    session = DB_SESSION()

    curr_time = datetime.datetime.now()
    curr_time_str = curr_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    # logging.info("Start Periodic Processing")

    last_updated = curr_time_str

    latest = session.query(Stats).order_by(Stats.last_updated.desc())
    if len(latest.all()) > 0:
        last_updated = latest[0].to_dict()["last_updated"].strftime("%Y-%m-%dT%H:%M:%SZ")

    expense_response = requests.get(app_config["getExpense"]["url"], params={"start_timestamp": last_updated, "end_timestamp": curr_time_str})
    expense_status_code = expense_response.status_code
    expense_json = expense_response.json()
    print("expense", expense_response.json(), "\n-----------------\n")

    revenue_response = requests.get(app_config["getRevenue"]["url"], params={"start_timestamp": last_updated, "end_timestamp": curr_time_str})
    revenue_status_code = revenue_response.status_code
    revenue_json = revenue_response.json()
    print("revenue", revenue_response.json())

    if expense_status_code== 200:
        logger.info(f"Received {len(expense_json)} events.")
    else:
        logger.error(f"The storage API has returned code {expense_response.status_code}.")

    if revenue_status_code == 200:
        logger.info(f"Received {len(revenue_json)} events.")
    else:
        logger.error(f"The storage API has returned code {revenue_response.status_code}.")

    rows = session.query(func.count(Stats.id)).scalar()

    if rows > 0:
        recent = session.query(Stats).order_by(Stats.last_updated.desc())[0].to_dict()

        total_expense = float(recent["total_expense"])
        total_item = int(recent["total_item"])
        popular_item = recent["popular_item"]
        max_quantity = int(recent["max_quantity"])
        daily_revenue = float(recent["daily_revenue"])
    else:
        total_expense = 0
        total_item = 0
        popular_item = ""
        max_quantity = 0
        daily_revenue = 0

    for event in expense_json:
        if int(event["quantity"]) > max_quantity:
            max_quantity = int(event["quantity"])
            popular_item = event["item_name"]

        total_expense += float(event["price"]) * int(event["quantity"])
        total_item += int(event["quantity"])
        logger.debug(f"Event processed:\n{event}\n")

    for event in revenue_json:
        daily_revenue = float(event["revenue"]) / int(event["report_period"])
        logger.debug(f"Event processed:\n{event}\n")

    last_updated = curr_time

    stats = Stats(total_expense,
                  total_item,
                  popular_item,
                  max_quantity,
                  daily_revenue,
                  last_updated)

    session.add(stats)

    session.commit()
    session.close()


def get_stats():
    logger.info("Received request for getting the latest stats, processing...")

    session = DB_SESSION()
    results = session.query(Stats).order_by(Stats.last_updated.desc())
    session.close()
    print(results)

    result = results[0].to_dict()

    logger.debug(f"The latest stats:\n{result}\n")
    logger.info("The request has been completed.")

    return result, 200


def health():

    return 200


app = connexion.FlaskApp(__name__, specification_dir='')


app.add_api("openapi.yml", base_path="/processing", strict_validation=True, validate_responses=True)

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

    CORS(app.app)
    app.app.config['CORS_HEADERS'] = 'Content-Type'

with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

DATABASE = app_config['datastore']['filename']
DB_ENGINE = create_engine(f"sqlite:///{DATABASE}")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

logger = logging.getLogger('basicLogger')

if not os.path.isfile(DATABASE):
    create_database()

logger.info(f"App Conf File: {app_conf_file}")
logger.info(f"Log Conf File: {log_conf_file}")

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)
