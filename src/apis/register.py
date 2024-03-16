from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.connect import session
from src.models.user import Users
from src.models.wallet import Wallet

from src.helper.encrypt_password import generate_hased_password
from src.helper.register import is_exists_email
from src.helper.send_email import send_email
from sqlalchemy import select, insert, update
from src.schema.register import Register, VerifyAccount
# from src.tasks import task
from src.config import config
from src.lib.exception import BadRequest
from src.lib.authentication import JsonWebToken
import jwt, json
from src.connect import redis
from src.lib.roles import Role
from src.helper.create_wallet import create_wallet

from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse
class Register(HTTPEndpoint):

    @executor(form_data = Register)
    async def post(self,form_data):
        if await is_exists_email(form_data['email']):
            raise BadRequest(errors="Email exists")
        # store data of user to posgreSQL
        b_pasword = generate_hased_password(form_data['password'])
        form_data['password'] = b_pasword
        # send email notification
        register_token = JsonWebToken(config.KEY_JWT, config.ALGORITHM_HASH_TOKEN)
        data = json.dumps({'email':form_data['email'], 'name': form_data['name'], 'password': b_pasword.decode('utf-8')})
        temp = register_token.create_token(payload_data=data)
        token = temp.get('token')
        redis.set(form_data['email'], token)
        message = 'Your account has been create successfully, please click the link to verify your account: {}?token={}'.format(config.BASE_URL_TOKEN,token)
        tasks = BackgroundTasks()
        tasks.add_task(send_email, form_data['email'], subject='Verify your account', message=message)
        return JSONResponse('success', background=tasks)

    @executor(query_params=VerifyAccount)
    async def get(self, query_params):
        token = query_params['token']
        _decode = jwt.decode(token, key=config.KEY_JWT,
                                    algorithms=[config.ALGORITHM_HASH_TOKEN])
        str_data = _decode.get('payload')
        data = json.loads(str_data)
        # check if verified
        if await is_exists_email(data['email']):
            return 'already verified'
        stored_token = redis.get(data['email']).decode()
        if stored_token == token:
            await session.execute(
            insert(Users).
            values(email = data['email'], name=data['name'], password = data['password'].encode(), role = Role.USER.value)
            )
            await session.commit()
            # create wallet
            result = await session.execute(select(Users).filter_by(**{'email' : data['email']}))
            result = result.fetchall()
            item = result[0]
            dict_item = item[0].as_dict
            user_id = dict_item['id']
            
            public_key, private_key = create_wallet()
            key = {'public_key': public_key, 'private_key': private_key}
            result = await session.execute(insert(Wallet).values(**{'userId' : user_id, 'key' : key}))
            await session.commit()
            await session.close()

            return "success"
        else:
            raise BadRequest(errors="Token does not match")