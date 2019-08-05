# -*- coding: utf-8 -*-
"""
    exceptions
    ~~~~~~~~~~~~~~~
  

"""

from aiohttp import web_exceptions


class JwtAuthMixinException:
    _detail: str = 'Something went wrong'

    def __init__(self) -> None:
        super().__init__(text=self._detail)  # type: ignore


class JwtAuthBaseException(JwtAuthMixinException, web_exceptions.HTTPUnauthorized):
    pass


########################################################


class AuthFailedInvalidClaims(JwtAuthBaseException):
    _detail = 'Invalid claims'


class AuthFailedNoHeader(JwtAuthBaseException):
    _detail = 'There is no authorization header'


class AuthFailedNoJwt(JwtAuthBaseException):
    _detail = 'No credentials provided.'


class AuthFailedInvalidHeaderPrefix(JwtAuthBaseException):
    _detail = 'Invalid header prefix.'


class AuthFailedSpaces(JwtAuthBaseException):
    _detail = 'Credentials string should not contain spaces.'


class AuthFailedDecodeError(JwtAuthBaseException):
    def __init__(self, detail: str = None):
        self._detail = f'Error decode token: {detail}'
        super().__init__()
