# -*- coding: utf-8 -*-
"""
    test_utils
    ~~~~~~~~~~~~~~~


"""

import pytest
import time

from aiohttp.test_utils import make_mocked_request

from aiohttp_jwt_auth import exceptions as jwt_exceptions
from aiohttp_jwt_auth.utils import get_authorization_header, get_jwt_string, decode_token
from aiohttp_jwt_auth.types import HttpAuthHeader, JWTString

JWT_HEADER: str = 'JWT'


########################################################
#  get_authorization_header
########################################################

def test_get_authorization_header_valid(faker):
    auth_header = faker.word()
    request = make_mocked_request('GET', '/', headers={'Authorization': auth_header})
    header = get_authorization_header(request)
    assert header == auth_header


def test_get_authorization_header_empty():
    request = make_mocked_request('GET', '/')
    header = get_authorization_header(request)
    assert not header


########################################################
#  validate_header
########################################################

def test_get_jwt_string_failed_no_header():
    header = HttpAuthHeader('')

    with pytest.raises(jwt_exceptions.AuthFailedNoHeader):
        get_jwt_string(header=header,
                       jwt_header_prefix=JWT_HEADER)


def test_get_jwt_string_header_failed_no_credentials():
    header = HttpAuthHeader(f'{JWT_HEADER}')

    with pytest.raises(jwt_exceptions.AuthFailedNoJwt):
        get_jwt_string(header=header,
                       jwt_header_prefix=JWT_HEADER)


def test_get_jwt_string_header_failed_invalid_header_prefix():
    header = HttpAuthHeader(f'INV{JWT_HEADER} some_jwt')

    with pytest.raises(jwt_exceptions.AuthFailedInvalidHeaderPrefix):
        get_jwt_string(header=header,
                       jwt_header_prefix=JWT_HEADER)


def test_get_jwt_string_header_failed_spaces():
    header = HttpAuthHeader(f'{JWT_HEADER} jwt also')

    with pytest.raises(jwt_exceptions.AuthFailedSpaces):
        get_jwt_string(header=header,
                       jwt_header_prefix=JWT_HEADER)


def test_get_jwt_string_header_success(faker):
    _jwt = faker.word()
    header = HttpAuthHeader(f'{JWT_HEADER} {_jwt}')

    try:
        jwt = get_jwt_string(header=header,
                             jwt_header_prefix=JWT_HEADER)
    except Exception as err:
        pytest.fail(f'Unexpected exception: {err}')

    assert jwt == _jwt


########################################################
#  validate_token
########################################################

def test_decode_token_decode_error(faker, public_key):
    jwt = JWTString(faker.word())
    with pytest.raises(jwt_exceptions.AuthFailedDecodeError):
        decode_token(
            jwt_string=jwt,
            public_key=public_key
        )


def test_decode_token_missing_exp(faker, decode_jwt, public_key):
    payload = {faker.word(): faker.word()}
    jwt = decode_jwt(payload)
    with pytest.raises(jwt_exceptions.AuthFailedDecodeError):
        decode_token(jwt_string=jwt,
                     public_key=public_key)

def test_decode_token_expired(decode_jwt, public_key):
    payload = {'exp': int(time.time()) - 10,}
    jwt = decode_jwt(payload)
    with pytest.raises(jwt_exceptions.AuthFailedDecodeError):
        decode_token(jwt_string=jwt,
                     public_key=public_key)


def test_decode_success(faker, decode_jwt, public_key):
    payload = {
        'exp': int(time.time()) + 10,
        faker.word(): faker.word(),
        faker.word(): faker.word()
    }
    jwt = decode_jwt(payload)
    _decoded = decode_token(jwt_string=jwt,
                 public_key=public_key)
    assert _decoded == payload
