from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.config import config
from sqlalchemy import select
from src.helper.order_info import get_orders
from src.lib.authentication import JsonWebToken
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)

class Orders(HTTPEndpoint):
    @executor(login_require=login_require)
    async def get(self, user):
        res = await get_orders()
        return res