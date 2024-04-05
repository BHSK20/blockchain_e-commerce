from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.connect import session, redis
from src.models.transaction import Transaction
from src.models.orders import Orders
from src.schema.transfer import Transfer, TransferOrder
from src.schema.header import HeaderUserPayload
from sqlalchemy import insert, update
from src.lib.roles import Role
from src.config import config
from src.helper.register import is_exists_email
from src.helper.user_info import get_publickey_by_email, get_privatekey_by_email, get_address_by_merchant_name
from src.helper.token_abstract import *
from src.lib.exception import BadRequest
from src.lib.transaction_type import TransactionType
from src.lib.status import Status
import json
from src.lib.authentication import JsonWebToken
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)

class Transfer(HTTPEndpoint):
    @executor(form_data=Transfer, login_require=login_require, header_data=HeaderUserPayload)
    async def post(self, form_data, user, header_data):
        amount = form_data['amount']
        currency = form_data['currency']
        # to address query form database
        to_address = await get_publickey_by_email(form_data['email'])
        if not await is_exists_email(form_data['email']):
            raise BadRequest('Email not found')
        from_address = await get_publickey_by_email(user['email'])
        # laod private_key from database
        private_key = await get_privatekey_by_email(user['email'])
        # transfer
        tx_hash = transfer(from_address,private_key, amount, to_address)
        tx_hash = tx_hash.hex()
        # pending insert db
        await session.execute(
            insert(Transaction).
            values(
                id = tx_hash,
                amount = amount,
                currency = currency,
                status = Status.PENDING.value
            ))
        await session.commit()
        # wait for transaction
        wait_for_transaction(tx_hash)
        # update database after transaction
        status, amount = status_value_of_transaction(tx_hash)
        # update transaction status
        await session.execute(update(Transaction).where(Transaction.id == tx_hash)
                              .values(status = Status.SUCCESS.value if status else Status.FAILURE.value))
        await session.commit()
        await session.close()
        return tx_hash

class TransferOrder(HTTPEndpoint):
    @executor(path_params=TransferOrder, login_require=login_require)
    async def get(self, path_params, user):
        order_id = path_params['order_id']
        data = redis.get(order_id)
        return json.loads(data) if data else None
    @executor(path_params=TransferOrder, login_require=login_require)
    async def post(self, path_params, user):
        order_id = path_params['order_id']
        data = redis.get(order_id)
        order = json.loads(data)
        ## transfer
        amount = order['amount']
        currency = order['currency']
        from_address = user['public_key']
        # laod private_key from database
        private_key = await get_privatekey_by_email(user['email'])
        # to address query form database
        to_address = await get_address_by_merchant_name(order['merchant'])
        # pending insert db
        await session.execute(
            insert(Transaction).
            values(
                id = tx_hash,
                amount = amount,
                type = TransactionType.TRANSFER_ORDER.value,
                currency = currency,
                status = Status.PENDING.value
            ))
        await session.commit()
        # transfer
        tx_hash, _ = transfer(from_address, private_key, amount, to_address)
        tx_hash = tx_hash.hex()
        # update database
        status, amount = status_value_of_transaction(tx_hash)
        
        # update transaction status
        await session.execute(update(Transaction).where(Transaction.id == tx_hash)
                              .values(status = Status.SUCCESS.value if status else Status.FAILURE.value))
        await session.commit()
        await session.close()
        
        if status:
            await session.execute(
                insert(Orders).
                values(
                    id = order_id,
                    order_name = order['order_name'],
                    user = user['email'],
                    merchant = order['merchant'],
                    amount = amount,
                    currency = currency
                ))
            await session.commit()
            redis.delete(order_id)
        await session.close()
        
        return tx_hash