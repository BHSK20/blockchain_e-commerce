from src.connect import db
from sqlalchemy import Column, Integer, Sequence, String, Boolean, TIMESTAMP, BINARY
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

class Wallet(db.Model):
    __tablename__ = 'Wallet'
    id = Column(Integer, primary_key=True)
    email = Column(String, ForeignKey('Users.email'))
    merchant = Column(String, nullable=True)
    key = Column(JSONB, nullable=True)
    created_time = Column(TIMESTAMP, default=datetime.now)
    updated_time = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<Wallet {self.userId}>'