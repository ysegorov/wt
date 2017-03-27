# -*- coding: utf-8 -*-

import os

import pytest

from wt.base import Object


def describe_dict_to_object():

    def must_return_Object_instance(sample_dict):
        src, dst = sample_dict
        assert isinstance(dst, Object)

    def must_have_attribute(sample_dict):
        src, dst = sample_dict
        assert dst.foo == src['foo']


def describe_process_list():

    def must_return_new_list(sample_list):
        src, dst = sample_list
        assert dst is not src
        assert isinstance(dst, list)

    def must_replace_dict_with_Object(sample_list):
        left, right = sample_list
        for src, dst in zip(left, right):
            assert isinstance(dst, Object)
            assert dst.foo == src['foo']


def describe_process_str_env():

    def must_replace_placeholder_with_value_from_env(sample_object):
        os.environ.setdefault('URL1', 'http://foo.com')
        os.environ.setdefault('URL2', 'bar.com')
        assert sample_object.foo == 'http://foo.com'
        assert sample_object.bar.baz == 'bar.com'

    def must_keep_placeholder_if_no_value_in_env(sample_object):
        assert sample_object.boo == '${HOST}'


def describe_process_str_file():

    def must_load_referenced_file(sample_object_with_file):
        conf = sample_object_with_file()
        assert isinstance(conf.pages, list), 'List of pages expected'
        assert len(conf.pages) == 3, 'Pages list must have 3 items'
        assert isinstance(conf.data.text, Object), 'Object expected'
        assert conf.data.text.bar.baz == 12

    def must_raise_if_referenced_file_not_found(sample_object_with_file):
        conf = sample_object_with_file(workdir=False)
        with pytest.raises(FileNotFoundError):
            conf.data.text


def describe_config():

    def must_return_empty_dict_for_paginate_or_jinja_attr(config_factory):
        c = config_factory()
        assert isinstance(c.paginate, dict)
        assert c.paginate == {}
        assert isinstance(c.jinja, dict)
        assert c.jinja == {}

    def must_return_dict_for_paginate_or_jinja_attr(config_factory):
        c = config_factory(paginate={'foo': 12}, jinja={'bar': 'baz'})
        assert isinstance(c.paginate, dict)
        assert c.paginate == {'foo': 12}
        assert isinstance(c.jinja, dict)
        assert c.jinja == {'bar': 'baz'}

    def must_call_super_for_not_paginate_or_jinja_attr(config_factory):
        c = config_factory(foo='bar')
        assert c.foo == 'bar'
        assert c.bar is None


def describe_content():

    def must_properly_load_text(content):
        assert os.path.isabs(content.src)
        assert content.text == 'bar'

    def must_properly_work_without_src(content_without_src):
        assert content_without_src.src is None
        assert content_without_src.text == ''


def describe_page():

    def must_load_page_content(page):
        assert page.text == 'lorem'


def describe_post():

    def must_load_post_content(post):
        assert post.text == 'ipsum'
