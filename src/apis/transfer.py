from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.connect import session
from src.models.transaction import Transaction
from src.schema.transfer import Transfer
from src.schema.header import HeaderUserPayload
from sqlalchemy import select, insert, update
from src.lib.roles import Role
from src.config import config
from src.helper.user_info import get_publickey_by_email, get_privatekey_by_email
from src.helper.token_abstract import *
import json
from src.lib.authentication import JsonWebToken
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)

class Transfer(HTTPEndpoint):
    @executor(form_data=Transfer, login_require=login_require, header_data=HeaderUserPayload)
    async def post(self, form_data, user, header_data):
        _, token = header_data['authorization'].split(' ')
        amount = form_data['amount']
        currency = form_data['currency']
        # to address query form database
        to_address = await get_publickey_by_email(form_data['email'])
        from_address = await get_publickey_by_email(user['email'])
        # laod private_key from database
        private_key = await get_privatekey_by_email(user['email'])
        # transfer
        tx_hash, _ = transfer(from_address,private_key, amount, to_address)
        tx_hash = tx_hash.hex()
        # update database
        status, amount = status_value_of_transaction(tx_hash)
        # update user's balance
        updated_token = None
        if status:
            updated_token = login_require.update_payload(token, {'balance': get_balance_in_ether(from_address)})
        await session.execute(
            insert(Transaction).
            values(
                id = tx_hash,
                amount = amount,
                currency = currency,
                status = (status==1)
            ))
        await session.commit()
        return tx_hash, updated_token
