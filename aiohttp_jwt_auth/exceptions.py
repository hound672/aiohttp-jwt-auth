# -*- coding: utf-8 -*-
"""
    exceptions
    ~~~~~~~~~~~~~~~
  

"""

from typing import Optional


class JwtAuthBaseException(Exception):
    _detail: str = 'Something went wrong'

    def __init__(self, detail: Optional[str] = None) -> None:
        self._detail = detail or self._detail

    def __str__(self) -> str:
        return self._detail

    @classmethod
    def get_detail(cls) -> str:
        return cls._detail


class InternalServerError(JwtAuthBaseException):
    _detail = 'Internal server error'


class AuthFailed(JwtAuthBaseException):
    _detail = 'Incorrect authentication credentials.'


class AuthFailedNoHeader(AuthFailed):
    _detail = 'There is no authorization header.'


class AuthFailedNoCredentials(AuthFailed):
    _detail = 'No credentials provided.'


class AuthFailedInvalidHeaderPrefix(AuthFailed):
    _detail = 'Invalid header prefix.'


class AuthFailedSpaces(AuthFailed):
    _detail = 'Credentials string should not contain spaces.'


class AuthFailedDecodeError(AuthFailed):
    def __init__(self, detail: str = None):
        self._detail = f'Error decode token: {detail}'


class PublicKeyEmptyError(InternalServerError):
    _detail = 'Public key is empty!'
