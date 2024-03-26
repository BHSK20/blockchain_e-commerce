from cryptography.hazmat.primitives import hashes

import json
from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.schema.checkout import GetOrder
from src.schema.header import Header
from src.lib.roles import Role
from src.config import config
from src.helper.merchant_register import create_signature, authorize_merchant
from src.lib.exception import BadRequest
from src.models.orders import Orders
from sqlalchemy import insert
from src.connect import session, redis
from src.lib.authentication import JsonWebToken
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)

class GetOrderInput(HTTPEndpoint):

    @executor(form_data = GetOrder, header_data = Header)
    async def post(self, form_data, header_data):
        data = form_data
        merchant_header = header_data['merchant']
        sign_header = header_data['sign']
        api_key_header = header_data['api_key']
        # authorize merchant
        merchant_name =  await authorize_merchant(partner_code=merchant_header)
        if not merchant_name:
            raise BadRequest('Merchant not found')
        sign = create_signature(data, api_key_header)
        if sign != sign_header:
            raise BadRequest('Signature not match')

        form_data['merchant'] = merchant_name
        order_id = form_data['order_id']
        del form_data['order_id']
        redis.set(order_id, json.dumps(form_data), db=1)
        return {'order_id': order_id}