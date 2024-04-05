from src.connect import session
from sqlalchemy import select
from src.models.transaction import Transaction
import json
from datetime import datetime

async def get_transfer_log():
    result = await session.execute(select(Transaction))
    list = result.fetchall()
    await session.close()
    if len(list):
        transactions = [item[0].as_dict for item in list]
        for transaction in transactions:
            transaction['date'] = str(transaction['date']) # Convert datetime to string
        return transactions
    else:
        return None
