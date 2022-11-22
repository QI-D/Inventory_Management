import connexion
import datetime
import json
import swagger_ui_bundle
import yaml
import logging
import logging.config
import requests
import time
import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS, cross_origin


def health():
    curr_time = datetime.datetime.now()
    curr_time_str = curr_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    health = {}

    receiver_health = app_config["receiverHealth"]
    storage_health = app_config["storageHealth"]
    processing_health = app_config["processingHealth"]
    audit_health = app_config["auditHealth"]
    timeout = app_config["timeout"]

    health_list = [receiver_health, storage_health, processing_health, audit_health]

    for health_check in health_list:
        try:
            requests.get(health_check["url"], timeout=timeout)
            health[health_check["service"]] = "Running"
        except Exception as e:
            health[health_check["service"]] = "Down"

    health["last_updated"] = curr_time_str

    logger.info(f"Health Check: {health}")

    with open("health_check.json", "w+") as f:
        json.dump(health, f, indent=4)

    return health, 200

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(health,
                  'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()


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

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8120, use_reloader=False)