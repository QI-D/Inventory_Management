import connexion
import datetime
import json
import swagger_ui_bundle
import yaml
import logging
import logging.config

from connexion import NoContent
from base import Base
from expense import Expense
from revenue import Revenue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


with open('app_config.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

DB_ENGINE = create_engine(f'mysql+pymysql://{app_config["datastore"]["user"]}:{app_config["datastore"]["password"]}@{app_config["datastore"]["hostname"]}:{app_config["datastore"]["port"]}/{app_config["datastore"]["db"]}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def placeOrder(body):

    trace_id = body['trace_id']
    session = DB_SESSION()

    expense = Expense(body['order_id'],
                      body['item_id'],
                      body['item_name'],
                      body['quantity'],
                      body['price'],
                      body['timestamp'],
                      trace_id)

    session.add(expense)

    session.commit()
    session.close()

    logging.info(f'Stored event expenseEvent with a trace id of {trace_id}')

    return NoContent, 201

def revenueReport(body):

    trace_id = body['trace_id']
    session = DB_SESSION()

    revenue = Revenue(body['submission_id'],
                      body['store_id'],
                      body['employee_id'],
                      body['revenue'],
                      body['report_period'],
                      body['timestamp'],
                      trace_id)

    session.add(revenue)

    session.commit()
    session.close()

    logging.info(f'Stored event revenueEvent with a trace id of {trace_id}')

    return NoContent, 201


def getExpense(timestamp):

    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    expenses = session.query(Expense).filter(Expense.date_created >= timestamp_datetime)

    results_list = []
    for expense in expenses:
        results_list.append(expense.to_dict())
    print(results_list)

    session.close()
    logger.info("Query for get expenses after %s returns %d results" % (timestamp, len(results_list)))

    return results_list, 200


def getRevenue(timestamp):

    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    revenue_reports = session.query(Revenue).filter(Revenue.date_created >= timestamp_datetime)

    results_list = []
    for revenue_report in revenue_reports:
        results_list.append(revenue_report.to_dict())
    print(results_list)

    session.close()
    logger.info("Query for get revenue report after %s returns %d results" % (timestamp, len(results_list)))

    return results_list, 200


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

with open('log_config.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

if __name__ == "__main__":
    app.run(port=8090)
