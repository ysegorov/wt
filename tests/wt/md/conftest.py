# -*- coding: utf-8 -*-

import pytest

from wt import md


CONTENT = """
# Foo page title

[bar link](/bar/)

![Logo](/logo96.png)

"""


@pytest.fixture(scope='function')
def markdown_content():
    return CONTENT


@pytest.fixture(scope='function')
def markdown_filter_factory():

    def factory(baseurl):
        return md.make_jinja_filter(baseurl)

    return factory
