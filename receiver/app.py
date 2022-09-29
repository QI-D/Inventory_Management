import connexion
import datetime
import json
import swagger_ui_bundle

from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


EVENT_FILE = "events.json"
MAX_EVENTS = 10


def recent_events(body, request_data, data=[]):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    data.insert(0, {"received_timestamp":timestamp, "request_data": request_data})

    if len(data) == MAX_EVENTS:
        with open(EVENT_FILE, 'w+') as f:
            json.dump(data, f, indent=4)
        data = []

    return data

def placeOrder(body):
    request_data = f"You have ordered {body['quantity']} {body['item_name']}."

    data = recent_events(body, request_data)

    return data, 201

def revenueReport(body):
    request_data = f"You have submitted a revenue report with ${body['revenue']} in {body['report_period']} days."

    data = recent_events(body, request_data)

    return data, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)
