from src.connect import session
from sqlalchemy import select
from src.models.transaction import Transaction
import json
from src.lib.transaction_type import TransactionType
from datetime import datetime

async def get_transfer_log():
    result = await session.execute(select(Transaction).filter_by(**{'type':TransactionType.TRANSFER.value}))
    list = result.fetchall()
    await session.close()
    if len(list):
        transactions = [item[0].as_dict for item in list]
        for transaction in transactions:
            transaction['date'] = str(transaction['date']) # Convert datetime to string
        return transactions
    else:
        return None
    
async def get_transfer_order_log():
    result = await session.execute(select(Transaction).filter_by(**{'type':TransactionType.TRANSFER_ORDER.value}))
    list = result.fetchall()
    await session.close()
    if len(list):
        transactions = [item[0].as_dict for item in list]
        for transaction in transactions:
            transaction['date'] = str(transaction['date']) # Convert datetime to string
        return transactions
    else:
        return None
