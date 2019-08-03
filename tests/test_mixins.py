import time

import pytest
from aiohttp import web
from aiohttp import web_exceptions

from aiohttp_jwt_auth import init_app_auth
from aiohttp_jwt_auth.structs import BaseUserDataToken
from aiohttp_jwt_auth.mixins import JWTAuthMixin


class UserModel(BaseUserDataToken):
    user_name: str
    value: int


JWT_HEADER_PREFIX: str = 'JWT'


########################################################

class _Index(JWTAuthMixin, web.View):
    async def get(self):
        user_data: UserModel = self.request['user']
        return web.json_response(user_data.dict())


@pytest.fixture
async def app_test_mixin(loop, public_key):
    app = web.Application()
    init_app_auth(
        app,
        public_key=public_key,
        jwt_header_prefix=JWT_HEADER_PREFIX,
        user_model=UserModel
    )
    app.add_routes([
        web.view('/index', _Index, name='index')
    ])
    return app


@pytest.fixture
async def client_test_mixin(app_test_mixin, aiohttp_client):
    async def _send_request(url, header):
        client = await aiohttp_client(app_test_mixin)
        return await client.get(url, headers={'Authorization': header})

    return _send_request


########################################################

async def test_JWTAuthMixin_empty_header(client_test_mixin):
    res = await client_test_mixin('/index', '')
    assert res.status == web_exceptions.HTTPUnauthorized.status_code


async def test_JWTAuthMixin_expired(client_test_mixin, decode_jwt, faker):
    _for_token = {
        'user_name': faker.word(),
        'exp': int(time.time()) - 10
    }
    jwt = decode_jwt(_for_token)
    res = await client_test_mixin('/index', f'{JWT_HEADER_PREFIX} {jwt}')

    assert res.status == web_exceptions.HTTPUnauthorized.status_code


async def test_JWTAuthMixin_error_user_struct(client_test_mixin, decode_jwt, faker):
    _for_token = {
        'user_name': faker.word(),
        'value': faker.word(),
        'exp': int(time.time()) + 10
    }
    jwt = decode_jwt(_for_token)
    res = await client_test_mixin('/index', f'{JWT_HEADER_PREFIX} {jwt}')

    assert res.status == web_exceptions.HTTPUnauthorized.status_code


async def test_JWTAuthMixin_success(client_test_mixin, decode_jwt, faker):
    _user = UserModel(
        user_name=faker.word(),
        value=faker.random_int()
    )
    _for_token = {
        **_user.dict(),
        'exp': int(time.time()) + 10
    }
    jwt = decode_jwt(_for_token)
    res = await client_test_mixin('/index', f'{JWT_HEADER_PREFIX} {jwt}')
    answer = await res.json()

    assert res.status == web_exceptions.HTTPOk.status_code
    assert _user.dict() == answer
