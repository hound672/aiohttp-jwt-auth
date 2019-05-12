# -*- coding: utf-8 -*-
"""
    test_settings
    ~~~~~~~~~~~~~~~
  
"""

from aiohttp_jwt_auth.consts import JWT_PUBLIC_KEY, JWT_AUTH_APP

from tests.utils import key_path


async def test_public_key(app):
    """
    Убеждаемся, что в fixture ранее записался верный public key
    """
    with open(key_path('testkey.pub'), 'rb') as key_file:
        public_key = key_file.read()

    auth_app = app[JWT_AUTH_APP]
    assert public_key == auth_app[JWT_PUBLIC_KEY]
