# -*- coding: utf-8 -*-

import jinja2


def describe_Registry():

    def must_properly_register_filter(jinja_registry):

        assert len(list(jinja_registry)) == 0

        def fltr(d):
            return d

        res = jinja_registry.add(fltr)
        assert res is fltr
        assert fltr in jinja_registry


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

    def must_use_markdown_filter(template_with_markdown):
        content = template_with_markdown.render(content=CONTENT)
        assert 'Hello' in content and 'world' in content
