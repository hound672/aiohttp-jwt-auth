# -*- coding: utf-8 -*-

"""Structs."""

from dataclasses import dataclass
from typing import Type

from pydantic import BaseModel

from aiohttp_jwt_auth._types import PublicKey


@dataclass
class JwtAuthApp:
    """Stores jwt_auth app."""

    public_key: PublicKey
    jwt_header_prefix: str
    user_model: Type['BaseUserDataToken']


########################################################

class BaseUserDataToken(BaseModel):
    """Base model for describe User."""
