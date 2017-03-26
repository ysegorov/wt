# -*- coding: utf-8 -*-

import pytest

from wt.decorators import reloadable


@pytest.fixture(scope='function')
def reloadable_factory():

    def factory():
        buf = []

        @reloadable('foo')
        def load(filename):
            buf.append(1)
            try:
                with open(filename, 'rt') as f:
                    return f.read()
            except FileNotFoundError:
                return -1

        return buf, load

    return factory
