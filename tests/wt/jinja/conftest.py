# -*- coding: utf-8 -*-

import sys

import pytest

from wt import jinja


@pytest.fixture(scope='function')
def jinja_registry(tmpdir):
    return jinja.Registry()


@pytest.fixture(scope='function')
def jinja_env(tmpdir):
    return jinja.get_env(str(tmpdir))


TEMPLATE = """\
{{ markdown(content) }}
"""


@pytest.fixture(scope='function')
def template_with_markdown(jinja_env):
    return jinja_env.from_string(TEMPLATE)


JINJA_HELPERS = """

from wt.jinja import filters, functions

@filters.add
def demo_filter(d):
    return d

@functions.add
def demo_fn(d):
    return d
demo_fn.function_name = 'my_demo_fn'
"""


@pytest.fixture(scope='function')
def jinja_env_with_helpers(tmpdir):
    jinja_filters = tmpdir.join('jinja_helpers.py')
    jinja_filters.write(JINJA_HELPERS)

    sys.path.insert(0, str(tmpdir))
    env = jinja.get_env(str(tmpdir))
    yield env
    sys.path.pop(0)
