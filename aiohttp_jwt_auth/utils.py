# -*- coding: utf-8 -*-
"""
    utils
    ~~~~~~~~~~~~~~~
  

"""

import jwt

from aiohttp.web_request import Request

from aiohttp_jwt_auth import exceptions as jwt_auth_exceptions
from aiohttp_jwt_auth.structs import UserDataToken


def get_authorization_header(request: Request) -> str:
    """
    Return request's 'Authorization:' header
    """
    return request.headers.get('Authorization', '')


def validate_header(*,
                    header: str,
                    jwt_header_prefix: str) -> str:
    """
    Just validate header
    Returns token from header
    """
    auth = header.split()
    jwt_prefix = jwt_header_prefix.lower()

    if not auth:
        raise jwt_auth_exceptions.AuthFailedNoHeader
    if len(auth) == 1:
        raise jwt_auth_exceptions.AuthFailedNoCredentials
    if auth[0].lower() != jwt_prefix:
        raise jwt_auth_exceptions.AuthFailedInvalidHeaderPrefix
    if len(auth) > 2:
        raise jwt_auth_exceptions.AuthFailedSpaces

    return auth[1]


def validate_token(*, token: str, public_key: str, verify_exp: bool = True) -> UserDataToken:
    """
    Validate JWT
    :param token: JWT string
    :param public_key: public key for check sign
    :param verify_exp: flag for verify expired time
    :return: user's payload
    """
    options = {
        'verify_exp': verify_exp,
        'require_exp': True
    }

    try:
        payload = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms='RS256',
            options=options
        )  # type: ignore
        user_data_token = UserDataToken(payload)  # type: ignore

    except jwt.DecodeError as err:
        raise jwt_auth_exceptions.AuthFailedDecodeError(str(err))
    except jwt.MissingRequiredClaimError as err:
        raise jwt_auth_exceptions.AuthFailedDecodeError(str(err))
    except jwt.ExpiredSignature as err:
        raise jwt_auth_exceptions.AuthFailedDecodeError(str(err))

    return user_data_token
