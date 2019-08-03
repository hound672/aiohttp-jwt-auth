# -*- coding: utf-8 -*-
"""
    conftest
    ~~~~~~~~~~~~~~~
  

"""

import os

import jwt
import pytest
from aiohttp import web
from faker import Factory

from aiohttp_jwt_auth import init_app_auth
from aiohttp_jwt_auth.consts import APP_JWT_AUTH
from aiohttp_jwt_auth.structs import JwtAuthApp


def key_path(key_name) -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'keys', key_name)


########################################################

@pytest.fixture
def faker():
    """Faker object"""
    return Factory.create()

@pytest.fixture
def public_key():
    """Get public key"""
    with open(key_path('testkey.pub'), 'r') as key_file:
        return key_file.read()


@pytest.fixture
def private_key():
    """Get private key"""
    with open(key_path('testkey.pem'), 'r') as key_file:
        return key_file.read()


@pytest.fixture
def decode_jwt(private_key):
    def _decode(payload: dict):
        _jwt = jwt.encode(
            payload=payload,
            key=private_key,
            algorithm='RS256'
        )
        return _jwt.decode('utf8')
    return _decode
