from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.connect import session
from src.models.merchant import Merchants
from src.schema.merchant_register import MerchantRegister
from sqlalchemy import select, insert
from src.lib.roles import Role
from src.config import config
from src.helper.merchant_register import *
from src.lib.authentication import JsonWebToken
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)

class MerchantRegister(HTTPEndpoint):

    @executor(form_data=MerchantRegister)
    async def post(self, form_data):
        # check form
        # register
        json_data = register_merchant()
        # store db
        await session.execute(
            insert(Merchants).
            values(partner_code = json_data['partner_code'],
                   api_key = json_data['api_key'],
                   merchant_name = form_data['merchant_name'],
                   tax_number = form_data['tax_number'],
                   address = form_data['address'])
            )
        await session.commit()
        await session.close()
        return json_data
