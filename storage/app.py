import connexion
import datetime
import json
import swagger_ui_bundle

from connexion import NoContent
from base import Base
from expense import Expense
from revenue import Revenue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_ENGINE = create_engine("sqlite:///business.sqlite")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def placeOrder(body):

    session = DB_SESSION()

    expense = Expense(body['order_id'],
                      body['item_id'],
                      body['item_name'],
                      body['quantity'],
                      body['price'],
                      body['timestamp'])

    session.add(expense)

    session.commit()
    session.close()

    return NoContent, 201

def revenueReport(body):

    session = DB_SESSION()

    revenue = Revenue(body['submission_id'],
                      body['store_id'],
                      body['employee_id'],
                      body['revenue'],
                      body['report_period'],
                      body['timestamp'])

    session.add(revenue)

    session.commit()
    session.close()

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8090)
