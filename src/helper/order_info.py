from src.connect import session
from sqlalchemy import select
from src.models.orders import Orders
from src.helper.user_info import get_merchant_name_by_email
import json
from datetime import datetime

async def get_orders_user(email):
    result = await session.execute(select(Orders).filter_by(**{'user':email}))
    list = result.fetchall()
    await session.close()
    if len(list):
        orders = [item[0].as_dict for item in list]
        for order in orders:
            order['date'] = str(order['date']) # Convert datetime to string
        return orders
    else:
        return None
    
async def get_orders_merchant(email):
    merchant_name = await get_merchant_name_by_email(email)
    result = await session.execute(select(Orders).filter_by(**{'merchant':merchant_name}))
    list = result.fetchall()
    await session.close()
    if len(list):
        orders = [item[0].as_dict for item in list]
        for order in orders:
            order['date'] = str(order['date']) # Convert datetime to string
        return orders
    else:
        return None