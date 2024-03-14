from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.connect import session
from src.models.test import Test
from sqlalchemy import select
from src.lib.roles import Role
from src.config import config
from src.lib.authentication import JsonWebToken
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)

class HealthCheck(HTTPEndpoint):

    @executor(login_require=login_require)
    async def get(self):
        return "health check"