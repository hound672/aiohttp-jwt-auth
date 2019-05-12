# -*- coding: utf-8 -*-
"""
    init
    ~~~~~~~~~~~~~~~
  

"""

from aiohttp import web

from aiohttp_jwt_auth.consts import JWT_PUBLIC_KEY, JWT_AUTH_APP, JWT_HEADER_PREFIX


def init_auth(*, app: web.Application,
              public_key: bytes,
              jwt_header_prefix: str) -> None:
    auth_app = web.Application()

    auth_app[JWT_PUBLIC_KEY] = public_key
    auth_app[JWT_HEADER_PREFIX] = jwt_header_prefix

    app[JWT_AUTH_APP] = auth_app
