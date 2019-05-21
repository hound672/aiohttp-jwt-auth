# -*- coding: utf-8 -*-
"""
    mixins
    ~~~~~~~~~~~~~~~
  

"""

import json
import logging

from aiohttp.web_request import Request
from aiohttp import web_exceptions

from aiohttp_jwt_auth import exceptions as jwt_auth_exceptions
from aiohttp_jwt_auth.structs import UserDataToken
from aiohttp_jwt_auth.consts import JWT_AUTH_APP, JWT_PUBLIC_KEY, JWT_HEADER_PREFIX
from aiohttp_jwt_auth.utils import get_authorization_header, validate_header, validate_token

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
            user_data_token = self.authenticate(request)
            request['user'] = user_data_token
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

    def authenticate(self, request: Request) -> UserDataToken:
        """
        Authenticate user and returns its dict
        """
        try:
            auth_app = request.config_dict[JWT_AUTH_APP]
            public_key = auth_app[JWT_PUBLIC_KEY]
            jwt_header_prefix = auth_app[JWT_HEADER_PREFIX]
        except KeyError:
            raise jwt_auth_exceptions.PublicKeyEmptyError

        header = get_authorization_header(request)
        token = validate_header(header=header,
                                jwt_header_prefix=jwt_header_prefix)

        user_data_token = validate_token(token=token, public_key=public_key,
                                         verify_exp=self._verify_expired)
        return user_data_token
