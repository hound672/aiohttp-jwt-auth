# -*- coding: utf-8 -*-
"""
    structs
    ~~~~~~~~~~~~~~~


"""

import jwt

from typing import Union


class BaseUserDataToken:
    """
    Stored required fields
    """
    _sub: Union[str, int]
    _exp: int
    _jti: Union[str, int]

    @property
    def sub(self) -> Union[str, int]:
        return self._sub

    @sub.setter
    def sub(self, sub: Union[str, int]) -> None:
        self._sub = sub

    @property
    def exp(self) -> int:
        return self._exp

    @exp.setter
    def exp(self, exp: int) -> None:
        self._exp = exp

    @property
    def jti(self) -> Union[str, int]:
        return self._jti

    @jti.setter
    def jti(self, jti: Union[str, int]) -> None:
        self._jti = jti

    def from_dict(self, data: dict) -> None:
        self._sub = data.get('sub')  # type: ignore
        self._exp = data.get('exp')  # type: ignore
        self._jti = data.get('jti')  # type: ignore

    def to_dict(self) -> dict:
        return {
            'sub': self.sub,
            'exp': self.exp,
            'jti': self.jti,
        }


class UserDataToken(BaseUserDataToken):
    """
    Class for keeping user data getting from JWT
    Object of this class is created by JWTAuthMixin and stored in "request" dict (key: user)
    """

    _rest: dict

    def __init__(self, _user_data: dict) -> None:
        user_data = {**_user_data}
        try:
            self._sub = user_data.pop('sub')
            self._exp = user_data.pop('exp')
            self._jti = user_data.pop('jti')

        except KeyError as key:
            raise jwt.MissingRequiredClaimError(key.args[0])

        # getting other fields
        self._rest = user_data

        super().__init__()

    def __str__(self) -> str:
        return f'UserDataToken: {self.sub}'

    def __repr__(self) -> str:
        return f'UserDataToken: {self.sub}'

    @property
    def rest(self) -> dict:
        return self._rest

    def get(self, key: str) -> Union[str, int]:
        return self._rest.get(key)  # type: ignore

    def set(self, key: str, value: Union[str, int]) -> None:
        if key in self._rest:
            self._rest[key] = value

    def to_dict(self) -> dict:
        """
        Convert all data to dict
        """
        return {
            **super().to_dict(),
            **self.rest
        }
