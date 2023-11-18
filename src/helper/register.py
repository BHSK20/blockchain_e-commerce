from src.connect import session
from src.models.user import Users
from sqlalchemy import select
async def is_exists_email(email):
    result = await session.execute(select(Users).filter_by(**{'email' : email}))
    data = result.fetchall()
    session.close()
    return len(data)
