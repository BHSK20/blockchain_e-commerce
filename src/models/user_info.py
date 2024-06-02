from src.connect import db
from sqlalchemy import Column, Integer, Sequence, String, Boolean, TIMESTAMP, BINARY, LargeBinary
from datetime import datetime

class UsersInfo(db.Model):
    __tablename__ = 'UsersInfo'
    email = Column(String, name='email', primary_key=True)
    name = Column(String, name='name', nullable=True)
    card_number = Column(Integer, name='card_number', nullable=True)
    date_of_birth = Column(TIMESTAMP, nullable=True)
    nationality = Column(String, nullable=True)
    gender = Column(Boolean, nullable=True) # True if female
    KYC_check = Column(Boolean, name='KYC_check', nullable=True, default=False)