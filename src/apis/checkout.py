from cryptography.hazmat.primitives import hashes
import json
import base64
import secrets


import requests
import json
from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.connect import session
from src.schema.checkout import Checkout
from sqlalchemy import select
from src.lib.roles import Role
from src.config import config
from src.lib.authentication import JsonWebToken
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)

MERCHANT_ID = '536e2d3a-1ac6-4071-8836-1abd5fba5fd5'
API_KEY = '536e2d3a-1ac6-4071-8836-1abd5fba5fd5-536e2d3a-1ac6-4071-8836-1abd5fba5fd5'
class Checkout(HTTPEndpoint):

    @executor(form_data=Checkout)
    async def post(self, form_data):
        amount = form_data['amount']
        currency = form_data['currency']
        # call api
        data = {
            'amount': amount,
            'currency': currency,
            'order_id': secrets.token_hex(12)
        }
        data_json = json.dumps(data)
        # Base64 encode the JSON data
        base64_encoded = base64.b64encode(data_json.encode())
        # Create MD5 hash
        md5_hash = hashes.Hash(hashes.MD5())
        combined_data = base64_encoded + API_KEY.encode()

        md5_hash.update(combined_data)
        digest = md5_hash.finalize()
        sign = digest.hex()
        print(sign)
        headers = {
            'merchant': MERCHANT_ID,
            'sign': sign
        }

        response = requests.post('https://api.cryptomus.com/v1/payment', data=json.dumps(data), headers=headers)
        return response.text
