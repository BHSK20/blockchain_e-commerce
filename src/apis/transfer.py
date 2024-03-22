from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.connect import session
from src.models.merchant import Merchants
from src.models.user import Users
from src.schema.transfer import Transfer
from sqlalchemy import select, insert, update
from src.lib.roles import Role
from src.config import config
from src.helper.user_info import get_publickey_by_email
from src.helper.token_abstract import *
import json
from src.lib.authentication import JsonWebToken
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)

class Transfer(HTTPEndpoint):
    @executor(form_data=Transfer, login_require=login_require)
    async def post(self, form_data, user):
        amount = form_data['amount']
        currency = form_data['currency']
        # to address query form database
        to_address = await get_publickey_by_email(form_data['email'])
        from_address = await get_publickey_by_email(user['email'])
        private_key = 'ffd576077aace63c3885551850642f3554fd4e30c2affef010300cfc3e37452d'
        tx_hash, transaction_json = transfer(from_address,private_key, amount, to_address)
        # Parse JSON into a Python object
        # Delete a field
        #update user's balance
        tx_hash = tx_hash.hex()
        transaction_detail = convert_hexbytes_to_string(dict(transaction_json))
        print(web3.eth.get_transaction(tx_hash))
        # update db
        
        return tx_hash
