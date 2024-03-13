from functools import wraps
from typing import Optional, Type
from starlette.requests import Request
from starlette.responses import Response
from starlette.datastructures import UploadFile
from src.lib.exception import BadRequest, BaseException as BE
from src.lib.authentication import Authorization
from pydantic import BaseModel

import traceback
import asyncio
import json
import tracemalloc

def executor(
    login_require: Optional[Authorization] = None,
    query_params: Optional[Type[BaseModel]] = None,
    form_data: Optional[Type[BaseModel]] = None,
    path_params: Optional[Type[BaseModel]] = None,
    header_data: Optional[Type[BaseModel]] = None,
    
    trace_error: bool=True,
    allow_roles = ['ALL'],
):
    def _internal(f):
        @wraps(f)
        async def decorated(*args, **kwargs):
            tracemalloc.start()

            _res = {
                'data': '',
                'msg': '',
                'errors': {},
            }
            try:
                _kwargs = {}
                _request: Request = args[1]
                _self = args[0]

                if header_data:
                    _header_data = _request.headers
                    try:
                        _header = header_data(**_header_data)
                        _kwargs['header_data'] = json.loads(_header.model_dump_json())
                    except Exception as e:
                        raise BadRequest(errors=json.loads(e.json()))
                    
                if login_require:
                    _payload = login_require.validate(_request)
                    _kwargs['user'] = _payload

                if len(allow_roles) > 0 and 'ALL' not in allow_roles:
                    _role = _kwargs['user'].get('role')
                    if _role not in allow_roles:
                        raise BadRequest(msg='Permission denied')

                if query_params:
                    _params_data = _request.query_params._dict
                    try:
                        _prams = query_params(**_params_data)
                        _kwargs['query_params'] = json.loads(_prams.model_dump_json())
                    except Exception as e:
                        raise BadRequest(errors=json.loads(e.json()))
                    
                if path_params:
                    _path_data = _request.path_params
                    try:
                        _prams = path_params(**_path_data)
                        _kwargs['path_params'] = json.loads(_prams.model_dump_json())
                    except Exception as e:
                        raise BadRequest(errors=json.loads(e.json()))

                if form_data:
                    _content_type = _request.headers.get('content-type')
                    if _content_type is None:
                        raise BadRequest(errors="data is required")

                    if _content_type == 'application/json':
                        try:
                            _form_data = await _request.json()
                            _data = form_data(**_form_data)
                            _kwargs['form_data'] =json.loads(_data.model_dump_json())
                        except Exception as e:
                            raise BadRequest(errors=json.loads(e.json()))

                    elif _content_type.startswith('multipart/form-data'):
                        async with _request.form() as form:
                            _data = {}
                            for k, v in form._dict.items():
                                if isinstance(v, UploadFile):
                                    _data[k] = await v.read()
                                else:
                                    _data[k] = v
                            try:
                                _data = form_data(**_data)
                                _kwargs['form_data'] = json.loads(_data.model_dump_json())
                            except Exception as e:
                                raise BadRequest(errors=json.loads(e.json()))

                if asyncio.iscoroutinefunction(f):
                    _response = await f(_self, **_kwargs)
                else:
                    _response = f(_self, **_kwargs)
                if isinstance(_response, Response):
                    return _response
                else:
                    _res['data'] = _response
                return Response(
                    content=json.dumps(_res),
                    status_code=200,
                    headers={'Content-type': 'application/json'}
                )
            except Exception as e:
                if trace_error and not isinstance(e, BE):
                    traceback.print_exc()
                _exc_header = {'Content-type': 'application/json'}
                _status = 400
                if isinstance(e, BE):
                    _res['errors'] = e.errors
                    _res['msg'] = e.msg
                    _status = e.status
                else:
                    _res['errors'] = str(e)
                    _status = 400
                tracemalloc.stop()
                return Response(json.dumps(_res), status_code=_status, headers=_exc_header)
        return decorated
    return _internal
