# -*- coding: utf-8 -*-

"""Exceptions."""

from typing import Optional

from aiohttp import web_exceptions


class JwtAuthMixinException:
    """Mixin for exception."""

    _detail: str = 'Something went wrong'

    def __init__(self) -> None:
        super().__init__(text=self._detail)  # type: ignore


class JwtAuthBaseException(JwtAuthMixinException, web_exceptions.HTTPUnauthorized):
    """Base module's exception."""


########################################################


class AuthFailedInvalidClaims(JwtAuthBaseException):
    """Invalid claims."""

    _detail = 'Invalid claims'


class AuthFailedNoHeader(JwtAuthBaseException):
    """Auth header was not found."""

    _detail = 'There is no authorization header'


class AuthFailedNoJwt(JwtAuthBaseException):
    """JWT was not found."""

    _detail = 'No credentials provided.'


class AuthFailedInvalidHeaderPrefix(JwtAuthBaseException):
    """Invalid JWT prefix."""

    _detail = 'Invalid header prefix.'


class AuthFailedSpaces(JwtAuthBaseException):
    """Error spaces in in credentails string."""

    _detail = 'Credentials string should not contain spaces.'


class AuthFailedDecodeError(JwtAuthBaseException):
    """Exception for error decode JWT."""

    def __init__(self, detail: Optional[str] = None):
        self._detail = 'Error decode token: {0}'.format(detail)
        super().__init__()
