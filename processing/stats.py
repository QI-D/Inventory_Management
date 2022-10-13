from decimal import Decimal
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Float
from base import Base


class Stats(Base):

    __tablename__ = "stats"

    id = Column(Integer, primary_key=True)
    total_expense = Column(Float, nullable=False)
    total_item = Column(Integer, nullable=False)
    popular_item = Column(String(100), nullable=False)
    max_quantity = Column(Integer, nullable=False)
    daily_revenue = Column(Float, nullable=False)
    last_updated = Column(DateTime, nullable=False)

    def __init__(self, total_expense, total_item, popular_item, max_quantity, daily_revenue, last_updated):
        self.total_expense = total_expense
        self.total_item = total_item
        self.popular_item = popular_item
        self.max_quantity = max_quantity
        self.daily_revenue = daily_revenue
        self.last_updated = last_updated

    def to_dict(self):
        dict = {}
        dict['id'] = self.id
        dict['total_expense'] = self.total_expense
        dict['total_item'] = self.total_item
        dict['popular_item'] = self.popular_item
        dict['max_quantity'] = self.max_quantity
        dict['daily_revenue'] = self.daily_revenue
        dict['last_updated'] = self.last_updated

        return dict