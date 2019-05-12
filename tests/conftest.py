# -*- coding: utf-8 -*-
"""
    conftest
    ~~~~~~~~~~~~~~~
  

"""

import pytest
from aiohttp import web

from aiohttp_jwt_auth.consts import JWT_PUBLIC_KEY, JWT_AUTH_APP

from tests.mock_app import init_mock_app


@pytest.fixture
async def app(loop) -> web.Application:
    """
    Returns app object
    """
    app = await init_mock_app()

    return app


@pytest.fixture
async def api_client(app: web.Application, aiohttp_client):
    """
    Returns object for API calls
    """
    return await aiohttp_client(app)


@pytest.fixture
def url_test_mixin(app: web.Application):
    """
    Returns URL for mixin unittests
    """
    return app.router['for_test_mixin'].url_for()


@pytest.fixture
def url_no_expired(app: web.Application):
    """
    Returns URL for mixin unittests
    """
    return app.router['no_expired'].url_for()


@pytest.fixture
async def api_mixin_test(api_client, url_test_mixin):
    """
    For test JWTAuthMixin
    """

    async def send_request(header):
        return await api_client.get(url_test_mixin, headers={'Authorization': header})

    return send_request


@pytest.fixture
async def api_mixin_test_no_expired(api_client, url_no_expired):
    """
    For test JWTAuthMixin
    """

    async def send_request(header):
        return await api_client.get(url_no_expired, headers={'Authorization': header})

    return send_request


@pytest.fixture
def public_key(app):
    return app[JWT_AUTH_APP][JWT_PUBLIC_KEY]
