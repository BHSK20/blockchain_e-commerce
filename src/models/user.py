from src.connect import db
from sqlalchemy import Column, Integer, Sequence, String, Boolean, TIMESTAMP, BINARY, LargeBinary
from datetime import datetime

class Users(db.Model):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(String, name='name', nullable=True)
    email = Column(String, name='email', nullable=True)
    password = Column(LargeBinary, name='password', nullable=True)
    is_active = Column(Boolean, name='is_active', nullable=True, default=True)
    role = Column(String, name='role', nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)