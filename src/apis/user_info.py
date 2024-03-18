from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.schema.user_info import GetPayload, GetMerchantInfo
from src.schema.header import HeaderUserPayload
from src.config import config
from src.lib.authentication import JsonWebToken
from src.helper.user_info import get_merchant_info_by_email

import json
login_require = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)
from src.lib.exception import BadRequest
class UserPayload(HTTPEndpoint):
    @executor(header_data=HeaderUserPayload)
    def get(self, header_data):
        print(header_data['authorization'])
        _, token = header_data['authorization'].split(' ')
        return login_require.get_payload(token)
class MerchantInfo(HTTPEndpoint):
    @executor(query_params=GetMerchantInfo)
    async def get(self,query_params):
        return await get_merchant_info_by_email(query_params['email'])