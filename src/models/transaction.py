from src.connect import db
from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, BOOLEAN
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'Transaction'
    id = Column(String, primary_key=True)
    type = Column(String, name='type', default='Transfer')
    date = Column(TIMESTAMP, name='date', default=datetime.now)
    amount = Column(Float, name='amount', nullable=True)
    currency = Column(String, name='currency', nullable=True)
    status = Column(String, name='status', nullable=True)