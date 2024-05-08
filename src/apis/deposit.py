from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.connect import session, redis
from src.config import config
from src.helper.token_abstract import get_balance_in_ether, transfer, wait_for_transaction, status_value_of_transaction
from src.helper.user_info import get_publickey_by_email, get_privatekey_by_email, get_address_by_merchant_name
from src.lib.status import Status
from src.lib.exception import BadRequest
from src.lib.authentication import JsonWebToken
from src.schema.checkout import Checkout
from sqlalchemy import insert, update
from src.models.transaction import Transaction
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)
from src.helper.test_transaction import check
class Deposit(HTTPEndpoint):
    @executor(login_require=login_require, form_data=Checkout)
    async def post(self, user, form_data):
        from_address = config.AD_PUBLIC_KEY
        to_address = user['public_key']
        # balance = get_balance_in_ether(address)
        amount = form_data['amount']
        currency = form_data['currency']
        
        # laod private_key from database
        private_key = config.AD_PRIVATE_KEY
        # transfer
        tx_hash = transfer(from_address,private_key, amount, to_address)
        tx_hash = tx_hash.hex()
        # pending insert db
        await session.execute(
            insert(Transaction).
            values(
                id = tx_hash,
                type = 'Deposit',
                amount = amount,
                currency = currency,
                status = Status.PENDING.value
            ))
        await session.commit()
        await session.close()
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
        return balance