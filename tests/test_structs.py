# -*- coding: utf-8 -*-
"""
    test_structs
    ~~~~~~~~~~~~~~~
  

"""

import pytest
import pydantic

from aiohttp_jwt_auth.structs import BaseUserDataToken


class UserDataToken(BaseUserDataToken):
    sub: str
    some_field: str
    exp: int
    jti: str


########################################################

def test_user_data_token_success(faker):
    data = {'some_field': faker.word(), 'sub': faker.uuid4(),
            'exp': faker.random_int(), 'jti': faker.uuid4()}

    try:
        user_data_token = UserDataToken(**data)
    except Exception as err:
        pytest.fail(f'Exception raised when it do not: {err}')
    else:
        assert user_data_token.sub == data['sub']
        assert user_data_token.exp == data['exp']
        assert user_data_token.jti == data['jti']
        assert user_data_token.some_field == data['some_field']
        assert user_data_token.dict() == data


########################################################


def test_user_data_not_all_data(faker):
    data = {'some_field': faker.word(), 'sub': faker.uuid4(),
            'exp': faker.random_int()}

    with pytest.raises(pydantic.ValidationError):
        UserDataToken(**data)
