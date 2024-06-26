from src.connect import session
from sqlalchemy import select
from src.models.user import Users

async def get_role_by_email(email):
    result = await session.execute(select(Users).filter_by(**{'email':email}))
    list = result.fetchall()
    if len(list):
        item = list[0]
        user_role = item[0].as_dict['role']
        return user_role
    else:
        return None