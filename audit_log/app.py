import connexion
import json
import swagger_ui_bundle
import yaml
import logging
import logging.config
import os

from flask_cors import CORS, cross_origin
from pykafka import KafkaClient

def expense_event(index):
    hostname = f"{app_config['events']['hostname']}:{app_config['events']['port']}"
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config['events']['topic'])]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=1000)

    logger.info(f"Retriving expense at index {index}")
    try:
        msg_list = []
        for msg in consumer:
            msg_str = msg.value.decode("utf-8")
            msg = json.loads(msg_str)
            if msg["type"] == "expenseEvent":
                msg_list.append(msg["payload"])

        event = [msg_list[index]]

        return event, 200

    except:
        logger.error("No messages found")

    logger.error(f"Could not find expense at index {index}")

    return {"message": "Not Found"}, 404

def revenue_event(index):
    hostname = f"{app_config['events']['hostname']}:{app_config['events']['port']}"
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config['events']['topic'])]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=1000)

    logger.info(f"Retriving revenue report at index {index}")
    try:
        msg_list = []
        for msg in consumer:
            msg_str = msg.value.decode("utf-8")
            msg = json.loads(msg_str)
            if msg["type"] == "revenueEvent":
                msg_list.append(msg["payload"])

        event = [msg_list[index]]

        return event, 200

    except:
        logger.error("No messages found")

    logger.error(f"Could not find revenue report at index {index}")

    return {"message": "Not Found"}, 404

def health():

    return 200


app = connexion.FlaskApp(__name__, specification_dir='')

CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

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


if __name__ == "__main__":
    app.run(port=8110)

