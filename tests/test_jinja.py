# -*- coding: utf-8 -*-

import sys

import jinja2

from wt import jinja


def intial_registry__is_empty():
    r = jinja.Registry()
    assert len(list(r)) == 0


def register_filter__returns__registered_function():

    def fltr(d):
        return d

    filters = jinja.Registry()

    assert filters.add(fltr) is fltr


def register_filter__stores__function_name():

    def fltr(d):
        return d

    filters = jinja.Registry()
    filters.add(fltr)

    assert fltr in filters


def get_env__returns__jinja2_environment_instance(tmpdir):
    assert isinstance(jinja.get_env(str(tmpdir)), jinja2.Environment)


def get_env__returns__env_with_registered_filter(tmpdir):

    def fltr(d):
        return d
    fltr.filter_name = 'my_filter'

    jinja.filters.add(fltr)

    env = jinja.get_env(str(tmpdir))

    assert 'my_filter' in env.filters


TEMPLATE = """\
{{ content|markdown }}
"""

CONTENT = """\
# H1

Hello, [world](http://example.com)!
"""


def template_render__uses__markdown_filter(tmpdir):
    env = jinja.get_env(str(tmpdir))
    tmpl = env.from_string(TEMPLATE)

    content = tmpl.render(content=CONTENT)
    assert 'Hello' in content and 'world' in content


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


def get_env__imports_and_uses_filters_from_jinja_helpers(tmpdir):
    jinja_filters = tmpdir.join('jinja_helpers.py')
    jinja_filters.write(JINJA_HELPERS)

    sys.path.insert(0, str(tmpdir))
    env = jinja.get_env(str(tmpdir))
    sys.path.pop(0)

    assert 'demo_filter' in env.filters


def get_env__imports_and_uses_functions_from_jinja_helpers(tmpdir):
    jinja_filters = tmpdir.join('jinja_helpers.py')
    jinja_filters.write(JINJA_HELPERS)

    sys.path.insert(0, str(tmpdir))
    env = jinja.get_env(str(tmpdir))
    sys.path.pop(0)

    assert 'my_demo_fn' in env.globals
