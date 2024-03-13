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
from src.helper.merchant_register import create_signature
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)
API_KEY = '1asdasd'
PARTNER_CODE = '123123123'
class CreateOrder(HTTPEndpoint):

    @executor(form_data=Checkout)
    async def post(self, form_data):
        print(1)
        amount = form_data['amount']
        currency = form_data['currency']
        # call api
        data = {
            'amount': amount,
            'currency': currency,
            'order_id': secrets.token_hex(12)
        }
        sign = create_signature(data, API_KEY)
        headers = {
            "Content-Type": "application/json",
            'merchant': PARTNER_CODE,
            'sign': sign
        }
        print('ok')
        try:
            response = await requests.post('https://on-shop-blockchain.onrender.com', json=data, headers=headers, timeout=100)
            # response = requests.get("https://scrapingbee.com/",timeout=30)
            print('2')
            # Check if the request was successful
            if response.status_code == 200:
                return str(response.content)
            else:
                # Handle unsuccessful response
                print(f"Error: Received status code {response.status_code}")
                return None
        except Exception as e:
            # Handle exceptions that may occur during the request
            print(f"An error occurred: {e}")
            return None

