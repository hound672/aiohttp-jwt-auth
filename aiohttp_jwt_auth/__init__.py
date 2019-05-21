# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~~~~~
  

"""

import re
from collections import namedtuple
from typing import Union, Match

from .init import init_auth

__all__ = ('init_auth', 'version_info')

__version__ = '0.0.2'

VersionInfo = namedtuple('VersionInfo',
                         'major minor micro')


def _parse_version(ver: str) -> VersionInfo:
    RE = (r'^(?P<major>\d+)\.(?P<minor>\d+)\.'
          '(?P<micro>\d+)')
    match: Union[Match[str], None] = re.match(RE, ver)
    # reveal_type(match)
    try:
        major = int(match.group('major'))  # type: ignore
        minor = int(match.group('minor'))  # type: ignore
        micro = int(match.group('micro'))  # type: ignore
        return VersionInfo(major, minor, micro)
    except Exception:
        raise ImportError("Invalid package version {}".format(ver))


version_info = _parse_version(__version__)
