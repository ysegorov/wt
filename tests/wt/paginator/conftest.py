# -*- coding: utf-8 -*-

import string

import pytest

from wt.paginator import Paginator


L = string.ascii_lowercase


@pytest.fixture
def ascii():
    return L


@pytest.fixture(scope='function')
def letters_factory():

    def factory(href='/', **kwargs):
        kwargs.setdefault('page_size', 5)
        kwargs.setdefault('orphans', 2)
        return Paginator(L, href, **kwargs)

    return factory


@pytest.fixture(scope='session')
def paginator_factory():

    def factory(*args, **kwargs):
        return Paginator(*args, **kwargs)

    return factory
