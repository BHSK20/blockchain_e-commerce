from src.connect import db
from sqlalchemy import Column, Integer, Sequence, String, Boolean, TIMESTAMP, BINARY, JSONB
from datetime import datetime
from sqlalchemy import ForeignKey


class Wallet(db.Model):
    __tablename__ = 'wallet'

    userId = Column(String, ForeignKey('Users.id'))
    merchant = Column(String, nullable=True)
    key = Column(JSONB)
    created_time = Column(TIMESTAMP, default=datetime.utcnow)
    updated_time = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Wallet {self.userId}>'