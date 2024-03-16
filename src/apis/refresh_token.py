from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.schema.refresh_token import RefreshToken
from src.config import config
from src.lib.authentication import JsonWebToken

import json
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)
from src.lib.exception import BadRequest
class RefreshToken(HTTPEndpoint):
    @executor(form_data = RefreshToken)
    def post(self,form_data):
        return login_require.refresh_token(refresh_token=form_data['refresh_token'])