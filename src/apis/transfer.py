from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.connect import session
from src.models.merchant import Merchants
from src.models.user import Users
from src.schema.transfer import Transfer
from sqlalchemy import select, insert, update
from src.lib.roles import Role
from src.config import config
from src.helper.transfer import transfer
from src.helper.user_info import get_publickey_by_email
from src.lib.authentication import JsonWebToken
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)

class Transfer(HTTPEndpoint):
    @executor(form_data=Transfer, login_require=login_require)
    async def post(self, form_data, user):
        amount = form_data['amount']
        currency = form_data['currency']
        # to address query form database
        to_address = await get_publickey_by_email(form_data['email'])
        from_address = user['public_key']
        private_key = '0xffd576077aace63c3885551850642f3554fd4e30c2affef010300cfc3e37452d'
        tx_hash, transaction_json = transfer(from_address,private_key, amount, to_address)
        
        return {'tx_hash': tx_hash, 'transaction_json': transaction_json}
