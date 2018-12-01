# -*- coding: utf-8 -*-

from unittest import mock

import jinja2
import pytest

from wt import jinja


def describe_Registry():

    def must_properly_register_filter(jinja_registry):

        assert len(list(jinja_registry)) == 0

        def fltr(d):
            return d

        res = jinja_registry.add(fltr)
        assert res is fltr
        assert fltr in jinja_registry

    def must_raise_value_error_if_filter_has_no_name(tmpdir):
        with mock.patch('wt.jinja.filters', jinja.Registry()):

            class Fltr(object):

                def __call__(self, text):
                    return text

            jinja.filters.add(Fltr())

            with pytest.raises(ValueError):
                jinja.get_env(str(tmpdir))

    def must_raise_value_error_if_function_has_no_name(tmpdir):
        with mock.patch('wt.jinja.functions', jinja.Registry()):

            class Function(object):

                def __call__(self, text):
                    return text

            jinja.functions.add(Function())

            with pytest.raises(ValueError):
                jinja.get_env(str(tmpdir))

    def must_properly_register_class_based_filter(jinja_registry):

        class Fltr(object):
            filter_name = 'class_based_filter'

            def __call__(self, text):
                return text

        fltr = Fltr()

        res = jinja_registry.add(fltr)
        assert isinstance(res, Fltr)
        assert fltr in jinja_registry


def describe_Baseurl():

    def must_return_concatenated_baseurl_and_url():

        baseurl, url = '/foo', '/baz'

        u = jinja.Baseurl(baseurl)

        assert u(url) == '/foo/baz'

    def must_return_url_if_baseurl_is_None():

        url = '/baz'

        u = jinja.Baseurl(None)

        assert u(url) == url

    def must_return_url_if_baseurl_is_empty():

        url = '/baz'

        u = jinja.Baseurl('')

        assert u(url) == url


def describe_get_env():

    def must_return_jinja2_environment(jinja_env):
        assert isinstance(jinja_env, jinja2.Environment)

    def must_properly_register_helpers(jinja_env_with_helpers):
        assert 'demo_filter' in jinja_env_with_helpers.filters
        assert 'my_demo_fn' in jinja_env_with_helpers.globals

    CONTENT = """\
    # H1

    Hello, [world](http://example.com)!
    """

    def must_use_markdown_function(template_with_markdown):
        content = template_with_markdown.render(content=CONTENT)
        assert 'Hello' in content and 'world' in content
