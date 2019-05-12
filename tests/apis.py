# -*- coding: utf-8 -*-
"""
    apis
    ~~~~~~~~~~~~~~~
  

"""

from aiohttp import web

from aiohttp_jwt_auth.mixins import JWTAuthMixin
from aiohttp_jwt_auth.structs import UserDataToken


class Index(JWTAuthMixin, web.View):
    async def get(self):
        # return user data
        user_data_token = self.request['user']  # type: UserDataToken
        return web.json_response(user_data_token.to_dict())


class NoExpired(JWTAuthMixin, web.View):
    _verify_expired = False

    async def get(self):
        # for check expired token
        user_data_token = self.request['user']  # type: UserDataToken
        return web.json_response(user_data_token.to_dict())
