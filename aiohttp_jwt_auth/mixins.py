# -*- coding: utf-8 -*-
"""
    mixins
    ~~~~~~~~~~~~~~~
  

"""

import logging

from aiohttp import web_exceptions
from aiohttp.web_request import Request
from pydantic import ValidationError

from . import exceptions as jwt_auth_exceptions
from .structs import JwtAuthApp, BaseUserDataToken
from .consts import APP_JWT_AUTH
from .utils import get_authorization_header, get_jwt_string, decode_token

logger = logging.getLogger(__name__)


class JWTAuthMixin:
    """
    Mixin for aiohttp.web.View
    Validate JWT token in HTTP header
    If do not need to verify expired token (on Refresh case for example):
        set _verify_expired to False
    """

    _verify_expired = True

    def __init__(self, request: Request) -> None:
        try:
            user_data = self._authenticate(request)
            request['user'] = user_data

        except jwt_auth_exceptions.AuthFailed as err:
            raise web_exceptions.HTTPUnauthorized(
                reason=str(err),
                content_type='application/json'
            )
        except jwt_auth_exceptions.InternalServerError as err:
            raise web_exceptions.HTTPInternalServerError(
                reason=str(err),
                content_type='application/json'
            )

        super().__init__(request)  # type: ignore

    def _authenticate(self, request: Request) -> 'BaseUserDataToken':
        """
        Authenticate user and returns its data
        """
        assert APP_JWT_AUTH in request.config_dict, 'There is no APP_JWT_AUTH in aiohttp app'
        app_auth: JwtAuthApp = request.config_dict[APP_JWT_AUTH]

        auth_header = get_authorization_header(request)
        jwt_string = get_jwt_string(header=auth_header,
                                    jwt_header_prefix=app_auth.jwt_header_prefix)
        decoded_jwt = decode_token(jwt_string=jwt_string,
                                   public_key=app_auth.public_key,
                                   verify_exp=self._verify_expired)

        UserModel = app_auth.user_model
        try:
            user_data = UserModel(**decoded_jwt)
        except ValidationError:
            raise jwt_auth_exceptions.InvalidClaims
        return user_data
