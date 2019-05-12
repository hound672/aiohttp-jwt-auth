# -*- coding: utf-8 -*-
"""
    test_structs
    ~~~~~~~~~~~~~~~
  

"""

import pytest
import jwt

from aiohttp_jwt_auth.structs import UserDataToken, BaseUserDataToken

from tests.utils import faker


def test_user_data_token_success():
    data = {'some_field': faker.word(), 'sub': faker.uuid4(),
            'exp': faker.random_int(), 'jti': faker.uuid4()}

    try:
        user_data_token = UserDataToken(data)
    except Exception as err:
        pytest.fail(f'Exception raised when it do not: {err}')
    else:
        assert user_data_token.sub == data['sub']
        assert user_data_token.exp == data['exp']
        assert user_data_token.jti == data['jti']
        assert user_data_token.rest.get('some_field') == data['some_field']
        assert user_data_token.to_dict() == data
        assert user_data_token.get('some_field') == data['some_field']
        assert user_data_token.get(faker.word()) is None


def test_base_user_data_token_form_dict_success():
    data = {'sub': faker.uuid4(),
            'exp': faker.random_int(), 'jti': faker.uuid4()}

    user_data_token = BaseUserDataToken()
    user_data_token.from_dict(data)

    assert user_data_token.sub == data['sub']
    assert user_data_token.exp == data['exp']
    assert user_data_token.jti == data['jti']
    assert user_data_token.to_dict() == data


def test_user_data_not_all_data():
    data = {'some_field': faker.word(), 'sub': faker.uuid4(),
            'exp': faker.random_int()}

    with pytest.raises(jwt.MissingRequiredClaimError):
        user_data_token = UserDataToken(data)


def test_user_data_setter():
    data = {'some_field': faker.word(), 'sub': faker.uuid4(),
            'exp': faker.random_int(), 'jti': faker.uuid4()}

    user_data_token = UserDataToken(data)

    assert user_data_token.sub == data['sub']
    assert user_data_token.exp == data['exp']
    assert user_data_token.jti == data['jti']
    assert user_data_token.get('some_field') == data['some_field']

    # change data

    user_data_token.sub = faker.random_int()
    user_data_token.exp = faker.uuid4()
    user_data_token.jti = faker.uuid4()
    user_data_token.set('some_field', faker.word())

    assert user_data_token.sub != data['sub']
    assert user_data_token.exp != data['exp']
    assert user_data_token.jti != data['jti']
    assert user_data_token.get('some_field') != data['some_field']

    try:
        # do not have to raise any exeptions when try to set data with wrong key
        user_data_token.set(faker.word(), faker.word())
    except Exception as err:
        pytest.fail(f'Exception rised when it do not: {err}')
