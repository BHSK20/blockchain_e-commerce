from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.connect import session
from src.models.merchant import Merchants
from src.models.user import Users
from src.schema.merchant_register import MerchantRegister
from sqlalchemy import select, insert, update
from src.lib.roles import Role
from src.config import config
from src.helper.merchant_register import *
from src.lib.authentication import JsonWebToken
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)

class MerchantRegister(HTTPEndpoint):

    @executor(form_data=MerchantRegister, login_require=login_require, allow_roles=[Role.USER.value])
    async def post(self, form_data, user):
        # register
        json_data = register_merchant()
        # store db
        await session.execute(
            insert(Merchants).
            values(
                    merchant_email = user['email'],
                    merchant_name = form_data['merchant_name'],
                    country = form_data['country'],
                    zipcode = form_data['zipcode'],
                    city = form_data['city'],
                    address1 = form_data['address1'],
                    address2 = form_data['address2'],
                    partner_code = json_data['partner_code'],
                    api_key = json_data['api_key'])
            )
        
        # update user role
        await session.execute(update(Users).
                                where(Users.email == user['email']).
                                values(role = Role.MERCHANT.value))
        
        await session.commit()
        await session.close()
        return json_data
