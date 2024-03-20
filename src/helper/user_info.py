from src.connect import session
from sqlalchemy import select
from src.models.merchant import Merchants
from src.models.user import Users
from src.models.wallet import Wallet

async def get_name_by_email(email):
    result = await session.execute(select(Users).filter_by(**{'email':email}))
    list = result.fetchall()
    await session.close()
    if len(list):
        item = list[0]
        name = item[0].as_dict['name']
        return name
    else:
        return None

async def get_merchant_info_by_email(email):
    result = await session.execute(select(Merchants).filter_by(**{'merchant_email':email}))
    list = result.fetchall()
    await session.close()
    if len(list):
        item = list[0]
        data = {key: value for key, value in item[0].as_dict.items() if key not in ['created_at', 'updated_at']}
        print(data)
        return data
    else:
        return None
    
async def get_publickey_by_email(email):
    result = await session.execute(select(Wallet).filter_by(**{'email':email}))
    list = result.fetchall()
    await session.close()
    if len(list):
        item = list[0]
        public_key = item[0].as_dict['key']['public_key']
        return public_key
    else:
        return None