# -*- coding: utf-8 -*-
"""
    test_utils
    ~~~~~~~~~~~~~~~
  

"""

import pytest
import datetime

from aiohttp.test_utils import make_mocked_request

from tests.utils import create_jwt_token, get_fake_jwt_token, \
    get_header_with_token, get_valid_jwt_token, faker

from aiohttp_jwt_auth.utils import get_authorization_header, validate_token, validate_header
from aiohttp_jwt_auth import exceptions as jwt_exceptions

JWT_HEADER: str = 'JWT'


def test_get_authorization_header_valid():
    text_token = get_valid_jwt_token()
    request = make_mocked_request('GET', '/', headers={'Authorization': text_token})

    header = get_authorization_header(request)
    assert header == text_token


def test_get_authorization_header_empty():
    request = make_mocked_request('GET', '/')

    header = get_authorization_header(request)
    assert not header


# unittests для проверки метода JWTAuthMixin.validate_header

def test_validate_header_failed_no_header():
    header = ''

    with pytest.raises(jwt_exceptions.AuthFailedNoHeader):
        validate_header(header=header,
                        jwt_header_prefix=JWT_HEADER)


def test_validate_header_failed_no_credentials():
    header = f'{JWT_HEADER}'

    with pytest.raises(jwt_exceptions.AuthFailedNoCredentials):
        validate_header(header=header,
                        jwt_header_prefix=JWT_HEADER)


def test_validate_header_failed_invalid_header_prefix():
    header = f'INV{JWT_HEADER} some_jwt'

    with pytest.raises(jwt_exceptions.AuthFailedInvalidHeaderPrefix):
        validate_header(header=header,
                        jwt_header_prefix=JWT_HEADER)


def test_validate_header_failed_spaces():
    header = f'{JWT_HEADER} jwt also'

    with pytest.raises(jwt_exceptions.AuthFailedSpaces):
        validate_header(header=header,
                        jwt_header_prefix=JWT_HEADER)


def test_validate_header_no_failed():
    """
    В данном тесте сама валидность токена не важна, так как мы
    проверяем метод валидации заголовка, а не валидности самого токена
    """
    header = f'{JWT_HEADER} jwt_token'

    try:
        validate_header(header=header,
                        jwt_header_prefix=JWT_HEADER)
    except Exception as err:
        pytest.fail(f'Exception rised when it do not: {err}')


def test_validate_header_return_token():
    mock_token = get_valid_jwt_token()
    header = get_header_with_token(mock_token)

    token = validate_header(header=header,
                            jwt_header_prefix=JWT_HEADER)
    assert token == mock_token


def test_validate_token_decode_error(public_key):
    token = get_fake_jwt_token()

    with pytest.raises(jwt_exceptions.AuthFailedDecodeError):
        validate_token(token=token, public_key=public_key)


def test_validate_token_success(public_key):
    token = get_valid_jwt_token()

    try:
        validate_token(token=token, public_key=public_key)
    except Exception as err:
        pytest.fail(f'Exception rised when it do not: {err}')


def test_validate_token_missing_exp(public_key):
    payload = {
        'sub': 'user',
        'jti': faker.random_int()
    }
    token = create_jwt_token(payload=payload)

    with pytest.raises(jwt_exceptions.AuthFailedDecodeError):
        validate_token(token=token, public_key=public_key)


def test_validate_token_missing_jti(public_key):
    payload = {
        'sub': 'user',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
    }
    token = create_jwt_token(payload=payload)

    with pytest.raises(jwt_exceptions.AuthFailedDecodeError):
        validate_token(token=token, public_key=public_key)


def test_validate_token_expired_signature(public_key):
    payload = {
        'sub': faker.random_int(),
        'exp': datetime.datetime.utcnow() - datetime.timedelta(seconds=5),
        'jti': faker.random_int()
    }
    token = create_jwt_token(payload=payload)

    with pytest.raises(jwt_exceptions.AuthFailedDecodeError):
        validate_token(token=token, public_key=public_key)


def test_validate_token_not_verify_expired_signature(public_key):
    payload = {
        'sub': faker.random_int(),
        'exp': datetime.datetime.utcnow() - datetime.timedelta(seconds=5),
        'jti': faker.random_int()
    }
    token = create_jwt_token(payload=payload)

    try:
        validate_token(token=token, public_key=public_key, verify_exp=False)
    except Exception as err:
        pytest.fail(f'Exception rised when it do not: {err}')
