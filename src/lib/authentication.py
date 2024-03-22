from starlette.requests import Request
from src.lib.exception import Forbidden
from abc import ABC, abstractmethod
import datetime
import jwt
import traceback

class Authorization(ABC):

    @abstractmethod
    def validate(self, request: Request, *arg, **kwargs):
        pass


class JsonWebToken(Authorization):
    def __init__(self, key, algorithm, *args, **kwargs) -> None:
        super(JsonWebToken, self).__init__(*args, **kwargs)
        self.key = key
        self.algorithm = algorithm

    def create_token(self, payload_data, *arg, **kwargs):
        token  = jwt.encode(payload={
            "payload": payload_data,
            "exp":datetime.datetime.now() + datetime.timedelta(days=2)
        }, key=self.key, algorithm=self.algorithm)
        refresh_token = jwt.encode(payload={
            "payload": payload_data,
            "exp":datetime.datetime.now() + datetime.timedelta(days=2)
        }, key=self.key, algorithm=self.algorithm)
        return {
            "token": token,
            "refresh_token": refresh_token
        }

    def validate(self, request: Request, *arg, **kwargs):
        super(JsonWebToken, self).validate(request, *arg, **kwargs)
        try:
            _authorization = request.headers.get('authorization')
            if not _authorization:
                raise
            _type, _token = _authorization.split()
            if _type.lower() != 'bearer':
                raise
            _decode = jwt.decode(_token, key=self.key,
                                    algorithms=[self.algorithm])
            return _decode.get('payload')
        except:
            traceback.print_exc()
            raise Forbidden()

    def refresh_token(self, refresh_token):
        try:
            _decode = jwt.decode(refresh_token, key=self.key, algorithms=self.algorithm)
            token  = jwt.encode(payload={
                    "payload": _decode.get("payload"),
                    "exp":datetime.datetime.now() + datetime.timedelta(minutes=30)
                }, key=self.key, algorithm=self.algorithm)
            return token
        except:
            raise Forbidden()

    def get_payload(self, token):
        try:
            _decode = jwt.decode(token, key=self.key, algorithms=self.algorithm)
            return _decode.get('payload')
        except:
            raise Forbidden()
    def update_payload(self, token, new_payload):
        try:
            # Decode the JWT
            _decode = jwt.decode(token, key=self.key, algorithms=self.algorithm)
            # Update the payload
            _decode['payload'].update(new_payload)
            # Re-encode the JWT
            updated_token = jwt.encode(payload=_decode, key=self.key, algorithm=self.algorithm)
            return updated_token
        except Exception as e:
            print(e)
            raise Forbidden()