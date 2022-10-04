from sqlalchemy import Column, Integer, String, DateTime, DECIMAL
from base import Base
import datetime


class Revenue(Base):

    __tablename__ = "revenue"

    id = Column(Integer, primary_key=True)
    submission_id = Column(String(36), nullable=False)
    store_id = Column(String(20), nullable=False)
    employee_id = Column(String(20), nullable=False)
    revenue = Column(DECIMAL, nullable=False)
    report_period = Column(Integer, nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(36), nullable=False)

    def __init__(self, submission_id, store_id, employee_id, revenue, report_period, timestamp, trace_id):
        """ Initializes a revenue report """
        self.submission_id = submission_id
        self.store_id = store_id
        self.employee_id = employee_id
        self.revenue = revenue
        self.report_period = report_period
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a revenue report """
        dict = {}
        dict['id'] = self.id
        dict['submission_id'] = self.submission_id
        dict['store_id'] = self.store_id
        dict['employee_id'] = self.employee_id
        dict['revenue'] = self.revenue
        dict['report_period'] = self.report_period
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict
