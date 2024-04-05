from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.config import config
from sqlalchemy import select
from src.helper.order_info import get_orders_merchant, get_orders_user
from src.lib.authentication import JsonWebToken
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)

class OrdersUser(HTTPEndpoint):
    @executor(login_require=login_require)
    async def get(self, user):
        res = await get_orders_user(user['email'])
        return res

class OrdersMerchant(HTTPEndpoint):
    @executor(login_require=login_require)
    async def get(self, user):
        res = await get_orders_merchant(user['email'])
        return res
