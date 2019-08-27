# -*- coding: utf-8 -*-

"""Init."""

from typing import Type

from aiohttp import web

from aiohttp_jwt_auth.consts import APP_JWT_AUTH
from aiohttp_jwt_auth._structs import BaseUserDataToken, JwtAuthApp
from aiohttp_jwt_auth._types import PublicKey


def init_app_auth(
    app: web.Application,
    *,
    public_key: PublicKey,
    jwt_header_prefix: str = 'JWT',
    user_model: Type['BaseUserDataToken'] = BaseUserDataToken,
) -> None:
    """
    Init JWT Auth app.

    :param app: main aiohttp application's object
    :param public_key: public key for AES256
    :param jwt_header_prefix: prefix for jwt on authenticate header
    :param user_model: user's model
    :return:
    """
    app_uth = JwtAuthApp(
        public_key=public_key,
        jwt_header_prefix=jwt_header_prefix,
        user_model=user_model,
    )
    app[APP_JWT_AUTH] = app_uth
