from src.models.user_info import UsersInfo
from src.connect import session
from src.models.user_info import UsersInfo
from sqlalchemy import insert, update
from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.schema.user_info import UpdateUserInfo
from src.schema.header import HeaderUserPayload
from src.config import config
from src.lib.authentication import JsonWebToken
from src.helper.user_info import get_user_info_KYC

import json
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)
from src.lib.exception import BadRequest
class UserInfoKYC(HTTPEndpoint):
    @executor(login_require=login_require)
    async def get(self, user):
        user_info  = await get_user_info_KYC(user['email'])
        return user_info
    @executor(login_require=login_require, form_data=UpdateUserInfo)
    async def post(self, user, form_data):
        await session.execute(
            insert(UsersInfo).
            values(
                form_data,
                email = user['email'],
                KYC_check = True,
            ))
        await session.commit()
        await session.close()
        return {'status': 'success'}
