# -*- coding: utf-8 -*-

import os

import pytest

from wt.base import dict_to_object, process_list, Config, Content


@pytest.fixture(scope='function',
                params=[{'foo': 12}, {'foo': object()}, {'foo': True}],
                ids=['int', 'object', 'bool'])
def sample_dict(request):
    return request.param, dict_to_object(request.param)


@pytest.fixture(scope='function',
                params=[[{'foo': 12}, {'foo': object()}], [{'foo': True}]],
                ids=['list-1', 'list-2'])
def sample_list(request):
    return request.param, process_list(request.param)


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
def config_factory():

    def factory(**kwargs):
        return Config(**kwargs)

    return factory


@pytest.fixture(scope='function')
def content(tmpdir):
    fn = tmpdir.mkdir('content').join('foo.md')
    fn.write('bar')
    return Content(src=str(fn))


@pytest.fixture(scope='function')
def content_without_src(tmpdir):
    return Content()


@pytest.fixture(scope='function')
def post(tmpdir):
    fn = tmpdir.mkdir('content').mkdir('posts').join('lorem.md')
    text = '\n'.join([
        '---',
        'url: /lorem/',
        '---',
        'ipsum',
    ])
    fn.write(text)
    return Content(src=str(fn))


@pytest.fixture(scope='function')
def page(tmpdir):
    fn = tmpdir.mkdir('content').mkdir('pages').join('ipsum.md')
    text = '\n'.join([
        '---',
        'url: /ipsum/',
        '---',
        'lorem',
    ])
    fn.write(text)
    return Content(src=str(fn))
