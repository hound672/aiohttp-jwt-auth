# -*- coding: utf-8 -*-
"""
    utils
    ~~~~~~~~~~~~~~~
  

"""

import os
import jwt
import datetime

from faker import Factory

faker = Factory.create()
JWT_HEADER: str = 'JWT'


def key_path(key_name) -> object:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'keys', key_name)


def get_header_with_token(token: str) -> str:
    header_return_token = f'{JWT_HEADER} {token}'
    return header_return_token


def create_jwt_token(payload: dict) -> str:
    """
    Генерирует JWT токен из набор данных
    и подписывает его валидным ключем
    """
    private_key = read_private_key()
    token = jwt.encode(
        payload=payload,
        key=private_key,
        algorithm='RS256'
    )
    return token.decode('utf-8')


def read_public_key() -> bytes:
    """
    Читает публиный ключ из файла
    """
    with open(key_path('testkey.pub'), 'rb') as key_file:
        return key_file.read()


def read_notmy_public_key() -> bytes:
    """
    Читает "не наш" публичный ключ
    """
    with open(key_path('notmytestkey.pub'), 'rb') as key_file:
        return key_file.read()


def read_private_key() -> bytes:
    """
    Читает приватный ключ из файла
    """
    with open(key_path('testkey.pem'), 'rb') as key_file:
        return key_file.read()


def read_notmy_private_key() -> bytes:
    """
    Читает "не наш" приватный ключ из файла
    """
    with open(key_path('notmytestkey.pem'), 'rb') as key_file:
        return key_file.read()


def get_notmy_jwt_token() -> str:
    """
    Генерирует JWT токен подписанный "не нашим" ключем
    """
    payload = {
        'sub': 'user',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5),
        'jti': faker.random_int()
    }
    private_key = read_notmy_private_key()
    token = jwt.encode(
        payload=payload,
        key=private_key,
        algorithm='RS256'
    )
    return token.decode('utf-8')



def get_fake_jwt_token() -> str:
    """
    Генерирует заведомо невалдный JWT
    """
    return faker.md5()


def get_valid_jwt_token() -> str:
    payload = {
        'sub': faker.random_int(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5),
        'jti': faker.random_int()
    }

    return create_jwt_token(payload)
