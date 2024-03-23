from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.config import config
from src.helper.token_abstract import get_balance_in_ether
from src.lib.exception import BadRequest
from src.lib.authentication import JsonWebToken
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)

class Balance(HTTPEndpoint):
    @executor(login_require=login_require)
    async def get(self, user):
        address = user['public_key']
        balance = get_balance_in_ether(address)
        return balance