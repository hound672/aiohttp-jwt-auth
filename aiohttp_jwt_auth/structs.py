# -*- coding: utf-8 -*-
"""
    structs
    ~~~~~~~~~~~~~~~


"""

from typing import Type
from dataclasses import dataclass

from pydantic import BaseModel

from .types import PublicKey


@dataclass
class JwtAuthApp:
    """
    Stores jwt_auth app
    """
    public_key: PublicKey
    jwt_header_prefix: str
    user_model: Type['BaseUserDataToken']



########################################################

class BaseUserDataToken(BaseModel):
    """
    Base model for describe User
    """
    pass
