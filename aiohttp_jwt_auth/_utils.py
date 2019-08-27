# -*- coding: utf-8 -*-

"""Some utils for aiohttp-jwt-auth."""

from typing import Any, Mapping

import jwt
from aiohttp.web_request import Request

from aiohttp_jwt_auth import _exceptions as jwt_auth_exceptions
from aiohttp_jwt_auth._types import HttpAuthHeader, JWTString, PublicKey


def get_authorization_header(request: Request) -> HttpAuthHeader:
    """
    Return http authorization header from request.

    :param request: Request's object
    :return: authorization header
    """
    header = request.headers.get('Authorization', '')
    return HttpAuthHeader(header)


def get_jwt_string(
    *,
    header: HttpAuthHeader,
    jwt_header_prefix: str,
) -> JWTString:
    """
    Validate authorization header and return JWT string.

    :param header: authorization header
    :param jwt_header_prefix: prefix for jwt
    :return: string with JWT
    """
    auth = header.split()
    jwt_prefix = jwt_header_prefix.lower()

    if not auth:
        raise jwt_auth_exceptions.AuthFailedNoHeader
    if len(auth) == 1:
        raise jwt_auth_exceptions.AuthFailedNoJwt
    if auth[0].lower() != jwt_prefix:
        raise jwt_auth_exceptions.AuthFailedInvalidHeaderPrefix
    if len(auth) > 2:
        raise jwt_auth_exceptions.AuthFailedSpaces

    return JWTString(auth[1])


def decode_token(
    *,
    jwt_string: JWTString,
    public_key: PublicKey,
    verify_exp: bool = True,
) -> Mapping[str, Any]:
    """
    Validate and decode JWT from JWTString.

    Return decoded token

    :param jwt_string: JWT string
    :param public_key: public key for check sign
    :param verify_exp: flag for verify expired time
    :return: user's payload
    """
    options = {
        'verify_exp': verify_exp,
        'require_exp': True,
    }

    try:
        return jwt.decode(
            jwt=jwt_string,
            key=public_key,
            algorithms='RS256',
            options=options,
        )

    except jwt.DecodeError as exc_decode:
        raise jwt_auth_exceptions.AuthFailedDecodeError(str(exc_decode))
    except jwt.MissingRequiredClaimError as exc_claim:
        raise jwt_auth_exceptions.AuthFailedDecodeError(str(exc_claim))
    except jwt.ExpiredSignature as exc_exp_sign:
        raise jwt_auth_exceptions.AuthFailedDecodeError(str(exc_exp_sign))
