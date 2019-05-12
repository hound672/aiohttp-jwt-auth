# -*- coding: utf-8 -*-
"""
    routes
    ~~~~~~~~~~~~~~~
  

"""

from aiohttp import web

from tests import apis


def init_routes(app: web.Application) -> None:
    app.add_routes([
        web.view('/test-mixin', apis.Index, name='for_test_mixin'),
        web.view('/test-mixin-no-expired', apis.NoExpired, name='no_expired')
    ])
