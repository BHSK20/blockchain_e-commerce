from src.connect import session
from sqlalchemy import select, join
from src.models.merchant import Merchants
from src.models.user import Users
from src.models.wallet import Wallet
from src.models.user_info import UsersInfo
from sqlalchemy.orm import joinedload

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

async def get_merchant_name_by_email(email):
    result = await session.execute(select(Merchants).filter_by(**{'merchant_email':email}))
    list = result.fetchall()
    await session.close()
    if len(list):
        item = list[0]
        name = item[0].as_dict['merchant_name']
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

async def get_address_by_merchant_name(merchant_name):
    join_statement = join(Merchants, Wallet, Merchants.merchant_email == Wallet.email)
    result = await session.execute(select(Wallet, Merchants).select_from(join_statement).filter(Merchants.merchant_name == merchant_name))
    list = result.fetchall()
    await session.close()
    if len(list):
        item = list[0]
        public_key = item[0].as_dict['key']['public_key']
        return public_key
    else:
        return None
async def get_name_role_public_key(email):
    join_statement = join(Wallet, Users, Wallet.email == Users.email)
    result = await session.execute(select(Users, Wallet).select_from(join_statement).filter(Wallet.email == email))
    list = result.fetchall()
    await session.close()
    if len(list):
        item = list[0]
        user_data = item[0].as_dict
        wallet_data = item[1].as_dict
        return {**user_data, **wallet_data}
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
    
async def get_privatekey_by_email(email):
    result = await session.execute(select(Wallet).filter_by(**{'email':email}))
    list = result.fetchall()
    await session.close()
    if len(list):
        item = list[0]
        private_key = item[0].as_dict['key']['private_key']
        return private_key
    else:
        return None
    
async def get_user_info_KYC(email):
    result = await session.execute(select(UsersInfo).filter_by(**{'email':email}))
    list = result.fetchall()
    await session.close()
    if len(list):
        item = list[0]
        return item[0].as_dict
    else:
        return None