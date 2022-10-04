from decimal import Decimal
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL
from base import Base
import datetime


class Expense(Base):

    __tablename__ = "expense"

    id = Column(Integer, primary_key=True)
    order_id = Column(String(36), nullable=False)
    item_id = Column(String(36), nullable=False)
    item_name = Column(String(250), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL, nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(36), nullable=False)

    def __init__(self, order_id, item_id, item_name, quantity, price, timestamp, trace_id):
        """ Initializes a expense """
        self.order_id = order_id
        self.item_id = item_id
        self.item_name = item_name
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a expense """
        dict = {}
        dict['id'] = self.id
        dict['order_id'] = self.order_id
        dict['item_id'] = self.item_id
        dict['item_name'] = self.item_name
        dict['quantity'] = self.quantity
        dict['price'] = self.price
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict
