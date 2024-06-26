from src.connect import db
from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, BOOLEAN
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
class Transaction(db.Model):
    __tablename__ = 'Transaction'
    id = Column(String, primary_key=True)
    from_address = Column(String, name='from_address', nullable=True)
    type = Column(String, name='type', default='Transfer')
    date = Column(TIMESTAMP(timezone=True), name='date', default=datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')))
    amount = Column(Float, name='amount', nullable=True)
    currency = Column(String, name='currency', nullable=True)
    status = Column(String, name='status', nullable=True)