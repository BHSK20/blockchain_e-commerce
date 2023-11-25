from src.connect import db
from sqlalchemy import Column, Integer, Sequence, String, Boolean, TIMESTAMP, BINARY
from datetime import datetime

class Users(db.Model):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, name='first_name', nullable=True)
    last_name = Column(String, name='last_name', nullable=True)
    email = Column(String, name='email', nullable=True)
    password = Column(BINARY, name='password', nullable=True)
    is_active = Column(Boolean, name='is_active', nullable=True, default=True)
    role = Column(String, name='role', nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)