from cryptography.hazmat.primitives import hashes
import json
import base64
import secrets


from fastapi import Request
import json
from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.connect import session
from src.schema.checkout import Checkout
from src.schema.header import Header
from sqlalchemy import select
from src.lib.roles import Role
from src.config import config
from src.lib.authentication import JsonWebToken
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)

class GetOrderInput(HTTPEndpoint):

    @executor(form_data = Checkout, header_data = Header)
    async def post(self, form_data, header_data):
        data = form_data
        merchant_header = header_data['merchant']
        sign_header = header_data['sign']
        return {
            'data': data,
            'headers': {
                'merchant': merchant_header,
                'sign': sign_header
            }
        }