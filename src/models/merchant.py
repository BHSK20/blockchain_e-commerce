from src.connect import db
from sqlalchemy import Column, Integer, Sequence, String, Boolean, TIMESTAMP, BINARY
from datetime import datetime

class Merchants(db.Model):
    __tablename__ = 'Merchants'
    merchant_id = Column(Integer, name='merchant_id', primary_key=True)
    partner_code = Column(String, name = 'partner_code', nullable=True)
    api_key = Column(String, name = 'api_key', nullable=True)
    merchan_name = Column(String, name='merchant_name', nullable=True)
    tax_number = Column(String, name='tax_number', nullable=True)
    address = Column(String, name='address', nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)