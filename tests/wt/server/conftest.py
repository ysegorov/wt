# -*- coding: utf-8 -*-

import pytest

from wt.engine import WT
from wt.utils import init
from wt import server


@pytest.fixture(scope='function')
def sample_blog(tmpdir):
    init(str(tmpdir))
    return WT(str(tmpdir.join('wt.yaml')))


BROKEN_CONTENT = """\
{% extends "base.html" %}
{% block content %}
{{ contet.text|markdown }}
{% endblock %}
"""


@pytest.fixture(scope='function')
def broken_sample_blog(tmpdir):
    init(str(tmpdir))
    mainpage = tmpdir.join('templates', 'content.html')
    mainpage.write(BROKEN_CONTENT)
    return WT(str(tmpdir.join('wt.yaml')))


@pytest.fixture(scope='function')
def server_app_factory(sample_blog):

    def factory(loop):
        return server.aiohttp_app(sample_blog.config_filename, loop=loop)

    return factory


@pytest.fixture(scope='function')
def broken_server_app_factory(broken_sample_blog):

    def factory(loop):
        return server.aiohttp_app(
            broken_sample_blog.config_filename, loop=loop)

    return factory
