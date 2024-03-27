from src.connect import session
from sqlalchemy import select
from src.models.orders import Orders
import json
from datetime import datetime

async def get_orders():
    result = await session.execute(select(Orders))
    list = result.fetchall()
    await session.close()
    if len(list):
        orders = [item[0].as_dict for item in list]
        for order in orders:
            order['date'] = str(order['date']) # Convert datetime to string
        return orders
    else:
        return None