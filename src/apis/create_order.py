from cryptography.hazmat.primitives import hashes
import json
import base64
import secrets

import aiohttp
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
API_KEY = 'jG-eyTRJBaz8JRjS78WSpEpM9CKYEsNNTNF1sYh7Q3E='
PARTNER_CODE = 'c799b631f54dc2867fc049c220a062cb'
class CreateOrder(HTTPEndpoint):

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
        sign = create_signature(data, API_KEY)
        headers = {
            "Content-Type": "application/json",
            'merchant': PARTNER_CODE,
            'sign': sign,
            'api_key': API_KEY
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://on-shop-blockchain.onrender.com/get_order_input', json=data, headers=headers, timeout=60) as response:
                    # Check if the request was successful
                    if response.status == 200:
                        text = await response.json()
                        return text
                    else:
                        # Handle unsuccessful response
                        print(f"Error: Received status code {response.status}")
                        return None
        except Exception as e:
            # Handle exceptions that may occur during the request
            print(f"Error: {str(e)}")
            return None
