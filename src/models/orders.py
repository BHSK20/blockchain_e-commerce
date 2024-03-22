from src.connect import db
from sqlalchemy import Column, Integer, Sequence, String, TIMESTAMP, Float
from datetime import datetime

class Orders(db.Model):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True)
    order_name = Column(String, name='order_name', nullable=True)
    merchant = Column(String, name='merchant', nullable=True)
    amount = Column(Float, name='amount', nullable=True)
    currency = Column(String, name='currency', nullable=True)
    date = Column(TIMESTAMP, name='date' , default=datetime.now)