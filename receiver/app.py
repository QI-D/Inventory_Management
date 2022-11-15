import connexion
import datetime
import json
import swagger_ui_bundle
import yaml
import logging
import logging.config
import uuid
import time
import os

from connexion import NoContent
from pykafka import KafkaClient


def placeOrder(body):
    trace_id = str(uuid.uuid4())
    body["trace_id"] = trace_id

    producer = topic.get_sync_producer()
    msg = {
        "type": "expenseEvent",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "payload": body
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f'Reveived event expenseEvent request with a trace id of {trace_id}')

    return NoContent, 201

def revenueReport(body):
    trace_id = str(uuid.uuid4())
    body["trace_id"] = trace_id

    producer = topic.get_sync_producer()
    msg = {
        "type": "revenueEvent",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "payload": body
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f'Reveived event revenueEvent request with a trace id of {trace_id}')

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_config.yml"
    log_conf_file = "/config/log_config.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_config.yml"
    log_conf_file = "log_config.yml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info(f"App Conf File: {app_conf_file}")
logger.info(f"Log Conf File: {log_conf_file}")

# connect to Kafka when receiver service starts instead of making connection in each endpoint
retry = 0
max_retry = app_config['retry']['max_retry']
sleep = app_config['retry']['sleep']
hostname = f"{app_config['events']['hostname']}:{app_config['events']['port']}"

while retry < max_retry:
    retry += 1
    try:
        logger.info(f"{retry} attempt to connect to Kafka...")
        client = KafkaClient(hosts=hostname)
        topic = client.topics[str.encode(app_config['events']['topic'])]
    except Exception as e:
        logger.error(f"Failed to connect to Kafka at attempt {retry}. Retrying in {sleep} seconds, {max_retry - retry} remaining... ")
        time.sleep(sleep)

if __name__ == "__main__":
    app.run(port=8080)
