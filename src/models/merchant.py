from src.connect import db
from sqlalchemy import Column, Integer, Sequence, String, Boolean, TIMESTAMP, BINARY
from datetime import datetime

class Merchants(db.Model):
    __tablename__ = 'Merchants'
    merchant_email = Column(String, name='merchant_email', primary_key=True, nullable=False)
    merchant_name = Column(String, name='merchant_name', nullable=True)
    country = Column(String, name='country', nullable=True)
    zipcode = Column(Integer, name='zipcode', nullable=True)
    city = Column(String, name='city', nullable=True)
    address1 = Column(String, name='address1', nullable=True)
    address2 = Column(String, name='address2', nullable=True)
    phone = Column(Integer, name='phone', nullable=True)
    partner_code = Column(String, name = 'partner_code', nullable=True)
    api_key = Column(String, name = 'api_key', nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.utcnow)