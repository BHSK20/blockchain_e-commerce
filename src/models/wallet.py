from src.connect import db
from sqlalchemy import Column, Integer, Sequence, String, Boolean, TIMESTAMP, BINARY
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

class Wallet(db.Model):
    __tablename__ = 'Wallet'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('Users.id'))
    merchant = Column(String, nullable=True)
    key = Column(JSONB, nullable=True)
    created_time = Column(TIMESTAMP, default=datetime.utcnow)
    updated_time = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Wallet {self.userId}>'