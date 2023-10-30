from starlette.endpoints import HTTPEndpoint
from src.lib.executor import executor
from src.connect import session
from src.models.user import Users
from src.helper.encrypt_password import generate_hased_password
from src.helper.register import is_exists_email
from sqlalchemy import select, insert
from src.schema.register import Register
from src.tasks import task
from src.lib.exception import BadRequest



from sqlalchemy import select


class Register(HTTPEndpoint):

    @executor(form_data = Register)
    async def post(self,form_data):
        if await is_exists_email(form_data['email']):
            raise BadRequest(errors="Email exists")
        (password, b_pasword) = generate_hased_password(12)
        # store data of user to posgreSQL
        (password, b_pasword) = generate_hased_password(12)
        form_data['password'] = b_pasword
        await session.execute(
            insert(Users).
            values(form_data)
        )
        await session.commit()
        # send email notification
        message = 'This is your password {}'.format(password)
        task.send_task('worker.send_mail', ("customer_email", form_data['email'], message), queue = 'send_mail')
        return "success"