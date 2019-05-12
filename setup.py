# -*- coding: utf-8 -*-
"""
    setup
    ~~~~~~~~~~~~~~~


"""

import os
import re
from setuptools import setup, find_packages


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(os.path.join(package, '__init__.py'), 'rb') as init_py:
        src = init_py.read().decode('utf-8')
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", src).group(1)


# define version of package
version = get_version('aiohttp_jwt_auth')

setup(
    name='aiohttp-jwt-auth',
    version=version,
    author='Vasiliy Bliznetcov',
    author_email='hound672@gmail.com',
    description='Library for simple JWT authenticate for an aiohttp application',
    url='https://github.com/hound672/aiohttp-jwt-auth',
    packages=['aiohttp_jwt_auth'],
    include_package_data=True,
    install_requires=[
        'PyJWT==1.7.1',
        'aiohttp==3.5.4',
        'cryptography==2.6.1'
    ],

    test_suite='tests'
)
