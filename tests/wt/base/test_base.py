# -*- coding: utf-8 -*-

import os

import pytest

from wt.base import (
    dict_to_object, process_list, Object, Config, Content, Page, Post)


@pytest.fixture(scope='function',
                params=[{'foo': 12}, {'foo': object()}, {'foo': True}],
                ids=['int', 'object', 'bool'])
def sample_dict(request):
    return request.param


@pytest.fixture(scope='function',
                params=[[{'foo': 12}, {'foo': object()}], [{'foo': True}]],
                ids=['list-1', 'list-2'])
def sample_list(request):
    return request.param


@pytest.fixture(scope='function')
def sample_object():
    return dict_to_object({
        'foo': '${URL1}',
        'bar': {
            'baz': '${URL2}'
        },
        'boo': '${HOST}',
    })


PAGES = """\
---
title: Item 1
---
title: Item 2
---
title: Item 3
...
"""
TEXT = """\
---
mainpage:
    title: mainpage title
    text: mainpage text
foo: some text
bar:
    baz: 12
...
"""


@pytest.fixture(scope='function')
def sample_object_with_file(tmpdir):
    pages = tmpdir.join('pages.yaml')
    pages.write_text(PAGES, 'utf-8')
    text = tmpdir.join('text.yaml')
    text.write_text(TEXT, 'utf-8')

    def factory(workdir=True):
        if workdir:
            os.environ['WT_WORKDIR'] = str(tmpdir)
        else:
            os.environ.pop('WT_WORKDIR', None)

        data = {
            'title': 'Hello',
            'pages': '{file}pages.yaml',
            'data': {
                'text': '{file}text.yaml'
            }
        }

        return dict_to_object(data)

    return factory


@pytest.fixture(scope='function')
def content(tmpdir):
    fn = tmpdir.mkdir('content').join('foo.md')
    fn.write('bar')
    data = {
        'src': 'foo.md'
    }
    return Content.from_dict(str(tmpdir), data)


@pytest.fixture(scope='function')
def content_without_src(tmpdir):
    return Content.from_dict(str(tmpdir), {})


@pytest.fixture(scope='function')
def post(tmpdir):
    fn = tmpdir.mkdir('content').mkdir('posts').join('lorem.md')
    fn.write('ipsum')
    data = {
        'src': 'lorem.md',
        'url': '/lorem/'
    }
    return Post.from_dict(str(tmpdir), data)


@pytest.fixture(scope='function')
def page(tmpdir):
    fn = tmpdir.mkdir('content').mkdir('pages').join('ipsum.md')
    fn.write('lorem')
    data = {
        'src': 'ipsum.md',
        'url': '/ipsum/'
    }
    return Page.from_dict(str(tmpdir), data)


def describe_dict_to_object():

    def must_return_Object_instance(sample_dict):
        assert isinstance(dict_to_object(sample_dict), Object)

    def must_have_attribute(sample_dict):
        assert dict_to_object(sample_dict).foo == sample_dict['foo']


def describe_process_list():

    def must_return_new_list(sample_list):
        dst = process_list(sample_list)
        assert dst is not sample_list
        assert isinstance(dst, list)

    def must_replace_dict_with_Object(sample_list):
        target = process_list(sample_list)
        for src, dst in zip(sample_list, target):
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

    def must_return_empty_dict_for_paginate_or_jinja_attr():
        c = Config()
        assert isinstance(c.paginate, dict)
        assert c.paginate == {}
        assert isinstance(c.jinja, dict)
        assert c.jinja == {}

    def must_return_dict_for_paginate_or_jinja_attr():
        c = Config(paginate={'foo': 12}, jinja={'bar': 'baz'})
        assert isinstance(c.paginate, dict)
        assert c.paginate == {'foo': 12}
        assert isinstance(c.jinja, dict)
        assert c.jinja == {'bar': 'baz'}

    def must_call_super_for_not_paginate_or_jinja_attr():
        c = Config(foo='bar')
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
