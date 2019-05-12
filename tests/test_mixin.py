# -*- coding: utf-8 -*-
"""
    test_url
    ~~~~~~~~~~~~~~~
  

"""

import datetime

from aiohttp import web_exceptions

from aiohttp_jwt_auth.consts import JWT_AUTH_APP, JWT_PUBLIC_KEY
from aiohttp_jwt_auth import exceptions as jwt_auth_exceptions

from tests.utils import (
    get_header_with_token, get_notmy_jwt_token, create_jwt_token, faker
)


JWT_HEADER: str = 'JWT'


async def test_JWTAuthMixin_no_header(api_mixin_test):
    res = await api_mixin_test('')

    status_code = res.status
    answer = await res.json()

    assert status_code == web_exceptions.HTTPUnauthorized.status_code
    assert answer.get('error') == jwt_auth_exceptions.AuthFailedNoHeader.get_detail()


async def test_JWTAuthMixin_no_credentials(api_mixin_test):
    header = f'{JWT_HEADER}'
    res = await api_mixin_test(header)

    status_code = res.status
    answer = await res.json()

    assert status_code == web_exceptions.HTTPUnauthorized.status_code
    assert answer.get('error') == jwt_auth_exceptions.AuthFailedNoCredentials.get_detail()


async def test_JWTAuthMixin_failed_invalid_header_prefix(api_mixin_test):
    header = f'INV{JWT_HEADER} some_jwt'
    res = await api_mixin_test(header)

    status_code = res.status
    answer = await res.json()

    assert status_code == web_exceptions.HTTPUnauthorized.status_code
    assert answer.get('error') == jwt_auth_exceptions.AuthFailedInvalidHeaderPrefix.get_detail()


async def test_JWTAuthMixin_failed_spaces(api_mixin_test):
    header = get_header_with_token('jwt jwt')
    res = await api_mixin_test(header)

    status_code = res.status
    answer = await res.json()

    assert status_code == web_exceptions.HTTPUnauthorized.status_code
    assert answer.get('error') == jwt_auth_exceptions.AuthFailedSpaces.get_detail()


async def test_JWTAuthMixin_decode_error(api_mixin_test):
    token = get_notmy_jwt_token()
    header = get_header_with_token(token)
    res = await api_mixin_test(header)

    status_code = res.status
    answer = await res.json()

    assert status_code == web_exceptions.HTTPUnauthorized.status_code
    assert answer.get('error') == 'Error decode token: Signature verification failed'


async def test_JWTAuthMixin_success(api_mixin_test):
    payload = {
        'sub': 'user',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5),
        'jti': faker.random_int()
    }
    token = create_jwt_token(payload=payload)
    header = get_header_with_token(token)
    res = await api_mixin_test(header)

    status_code = res.status
    answer = await res.json()

    assert status_code == web_exceptions.HTTPOk.status_code
    assert answer == payload


async def test_JWTAuthMixin_missing_exp(api_mixin_test):
    payload = {
        'sub': 'user',
        'jti': faker.random_int()
    }
    token = create_jwt_token(payload=payload)
    header = get_header_with_token(token)
    res = await api_mixin_test(header)

    status_code = res.status
    answer = await res.json()

    assert status_code == web_exceptions.HTTPUnauthorized.status_code
    assert answer.get('error') == 'Error decode token: Token is missing the "exp" claim'


async def test_JWTAuthMixin_missing_jti(api_mixin_test):
    payload = {
        'sub': 'user',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
    }
    token = create_jwt_token(payload=payload)
    header = get_header_with_token(token)
    res = await api_mixin_test(header)

    status_code = res.status
    answer = await res.json()

    assert status_code == web_exceptions.HTTPUnauthorized.status_code
    assert answer.get('error') == 'Error decode token: Token is missing the "jti" claim'


async def test_JWTAuthMixin_token_expired_signature(api_mixin_test):
    payload = {
        'sub': 'user',
        'exp': datetime.datetime.utcnow() - datetime.timedelta(seconds=5),
        'jti': faker.random_int()
    }
    token = create_jwt_token(payload=payload)
    header = get_header_with_token(token)
    res = await api_mixin_test(header)

    status_code = res.status
    answer = await res.json()

    assert status_code == web_exceptions.HTTPUnauthorized.status_code
    assert answer.get('error') == 'Error decode token: Signature has expired'


async def test_JWTAuthMixin_token_not_verify_expired_signature(api_mixin_test_no_expired):
    payload = {
        'sub': 'user',
        'exp': datetime.datetime.utcnow() - datetime.timedelta(seconds=5),
        'jti': faker.random_int()
    }
    token = create_jwt_token(payload=payload)
    header = get_header_with_token(token)
    res = await api_mixin_test_no_expired(header)

    status_code = res.status
    answer = await res.json()

    assert status_code == web_exceptions.HTTPOk.status_code


async def test_JWTAuthMixin_public_key_empty(api_mixin_test, app):
    # remove public key
    app[JWT_AUTH_APP].pop(JWT_PUBLIC_KEY)

    payload = {
        'sub': 'user',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5),
        'jti': faker.random_int()
    }
    token = create_jwt_token(payload=payload)
    header = get_header_with_token(token)
    res = await api_mixin_test(header)

    status_code = res.status
    answer = await res.json()

    assert status_code == web_exceptions.HTTPInternalServerError.status_code
    assert answer.get('error') == jwt_auth_exceptions.PublicKeyEmptyError.get_detail()
