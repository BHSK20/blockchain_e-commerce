from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.connect import session
from src.models.user import Users
from src.helper.encrypt_password import generate_hased_password
from src.helper.register import is_exists_email
from src.helper.send_email import send_email
from sqlalchemy import select, insert
from src.schema.register import Register, VerifyAccount
# from src.tasks import task
from src.config import config
from src.lib.exception import BadRequest
from src.lib.authentication import JsonWebToken
import jwt, json
from src.connect import redis
from src.lib.roles import Role
from sqlalchemy import select


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
        data = json.dumps({'email':form_data['email'], 'first_name': form_data['first_name'], 'last_name':form_data['last_name'], 'password': b_pasword.decode('utf-8')})
        temp = register_token.create_token(payload_data=data)
        token = temp.get('token')
        redis.set(form_data['email'], token)
        message = 'Your account has been create successfully, please click the link to verify your account: {}?token={}'.format(config.BASE_URL_TOKEN,token)
        # task.send_task('worker.send_mail', ("customer_email", form_data['email'], message), queue = 'send_mail')
        send_email(form_data['email'], subject='Your account has been created', message=message)
        return "success"

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
            print('ok')
            await session.execute(
            insert(Users).
            values(email = data['email'], first_name = data['first_name'], last_name = 'USER', password = data['password'].encode(), role = Role.USER.value)
            )
            await session.commit()
            await session.close()
            return "success"
        else:
            raise BadRequest(errors="Token does not match")