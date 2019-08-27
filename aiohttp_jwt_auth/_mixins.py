# -*- coding: utf-8 -*-

"""Mixins."""

import logging

from aiohttp.web_request import Request
from pydantic import ValidationError

from aiohttp_jwt_auth import _exceptions as jwt_auth_exceptions
from aiohttp_jwt_auth.consts import APP_JWT_AUTH
from aiohttp_jwt_auth._structs import BaseUserDataToken, JwtAuthApp
from aiohttp_jwt_auth._utils import (
    decode_token,
    get_authorization_header,
    get_jwt_string,
)

logger = logging.getLogger(__name__)


class JWTAuthMixin:
    """
    Mixin for aiohttp.web.View.

    Validate JWT token in HTTP header
    If do not need to verify expired token (on Refresh case for example):
    set _verify_expired to False
    """

    _verify_expired = True

    def __init__(self, request: Request) -> None:
        """Look for auth header and checj it."""
        user_data = self._authenticate(request)
        request['user'] = user_data
        super().__init__(request)  # type: ignore

    def _authenticate(self, request: Request) -> 'BaseUserDataToken':
        """Authenticate user and returns its data."""
        assert APP_JWT_AUTH in request.config_dict, 'No APP_JWT_AUTH in app'
        app_auth: JwtAuthApp = request.config_dict[APP_JWT_AUTH]

        auth_header = get_authorization_header(request)
        jwt_string = get_jwt_string(
            header=auth_header,
            jwt_header_prefix=app_auth.jwt_header_prefix,
        )
        decoded_jwt = decode_token(
            jwt_string=jwt_string,
            public_key=app_auth.public_key,
            verify_exp=self._verify_expired,
        )

        UserModel = app_auth.user_model  # noqa: N806
        try:
            return UserModel(**decoded_jwt)
        except ValidationError:  # noqa: WPS329
            raise jwt_auth_exceptions.AuthFailedInvalidClaims
