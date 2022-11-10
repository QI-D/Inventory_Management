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
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread


with open('app_config.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

DB_ENGINE = create_engine(f'mysql+pymysql://{app_config["datastore"]["user"]}:{app_config["datastore"]["password"]}@{app_config["datastore"]["hostname"]}:{app_config["datastore"]["port"]}/{app_config["datastore"]["db"]}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def placeOrder(payload):

    trace_id = payload['trace_id']
    session = DB_SESSION()

    expense = Expense(payload['order_id'],
                      payload['item_id'],
                      payload['item_name'],
                      payload['quantity'],
                      payload['price'],
                      payload['timestamp'],
                      trace_id)

    session.add(expense)

    session.commit()
    session.close()

    logger.info(f'Stored event expenseEvent with a trace id of {trace_id}')
    logger.info(f'Connecting to DB at {app_config["datastore"]["hostname"]} on port {app_config["datastore"]["port"]}')

    return "Saved expense to db"

def revenueReport(payload):

    trace_id = payload['trace_id']
    session = DB_SESSION()

    revenue = Revenue(payload['submission_id'],
                      payload['store_id'],
                      payload['employee_id'],
                      payload['revenue'],
                      payload['report_period'],
                      payload['timestamp'],
                      trace_id)

    session.add(revenue)

    session.commit()
    session.close()

    logger.info(f'Stored event revenueEvent with a trace id of {trace_id}')
    
    logger.info(f'Connecting to DB at {app_config["datastore"]["hostname"]} on port {app_config["datastore"]["port"]}')

    return "Saved revenue report to db"


def getExpense(start_timestamp, end_timestamp):

    session = DB_SESSION()
    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%SZ")

    expenses = session.query(Expense).filter(
        and_(Expense.date_created >= start_timestamp_datetime,
             Expense.date_created <= end_timestamp_datetime))

    results_list = []
    for expense in expenses:
        results_list.append(expense.to_dict())
    print(results_list)

    session.close()
    logger.info("Query for get expenses after %s returns %d results" % (start_timestamp, len(results_list)))

    return results_list, 200


def getRevenue(start_timestamp, end_timestamp):

    session = DB_SESSION()
    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%SZ")

    revenue_reports = session.query(Revenue).filter(
        and_(Revenue.date_created >= start_timestamp_datetime,
             Revenue.date_created <= end_timestamp_datetime))

    results_list = []
    for revenue_report in revenue_reports:
        results_list.append(revenue_report.to_dict())
    print(results_list)

    session.close()
    logger.info("Query for get revenue report after %s returns %d results" % (start_timestamp, len(results_list)))

    return results_list, 200


def process_messages():
    """ Process event messages """

    hostname = f"{app_config['events']['hostname']}:{app_config['events']['port']}"
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config['events']['topic'])]

    # Create a consume on a consumer group, that only reads new messages
    # # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)

    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info(f"Message : {msg}")

        payload = msg["payload"]

        if msg["type"] == "expenseEvent":
            placeOrder(payload)
        elif msg["type"] == "revenueEvent":
            revenueReport(payload)

        # Commit the new message as being read
        consumer.commit_offsets()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

with open('log_config.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
