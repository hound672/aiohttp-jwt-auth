# -*- coding: utf-8 -*-
"""
    mock_app
    ~~~~~~~~~~~~~~~
  

"""

from aiohttp import web

from aiohttp_jwt_auth import init_auth

from tests.routes import init_routes
from tests.utils import read_public_key


async def init_mock_app() -> web.Application:
    """
    Инициалзирует mock объект приложения
    """
    app = web.Application()

    public_key = read_public_key()
    init_routes(app)
    init_auth(app=app,
              public_key=public_key,
              jwt_header_prefix='JWT')

    return app
