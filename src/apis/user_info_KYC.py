from src.models.user_info import UsersInfo
from src.connect import session, redis
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
        data = redis.get("KYC_{}".format(user['email']))
        json_data = json.loads(data) if data else None
        if json_data:
            return json_data
        user_info  = await get_user_info_KYC(user['email'])
        return user_info
    @executor(login_require=login_require, form_data=UpdateUserInfo)
    async def post(self, user, form_data):
        form_data['email'] = user['email']
        gender = form_data['gender']
        # Convert to boolean
        form_data['gender'] = gender.lower() == 'female'
        redis.set("KYC_{}".format(form_data['email']), json.dumps(form_data))
        return form_data

    @executor(login_require=login_require, form_data=UpdateUserInfo)
    async def put(self, user, form_data):
        data = redis.get("KYC_{}".format(user['email']))
        json_data = json.loads(data) if data else None
        if not json_data:
            raise BadRequest('Please update user info first')

        gender = form_data['gender']
        # Convert to boolean
        form_data['gender'] = gender.lower() == 'female'
        # compare
        if json_data != form_data.json():
            return {'status': 'fail'}
        form_data['email'] = user['email'],
        await session.execute(
            insert(UsersInfo).
            values(
                form_data,
                KYC_check = True,
            ))
        await session.commit()
        await session.close()
        redis.delete("KYC_{}".format(user['email']))
        return {'status': 'success'}
