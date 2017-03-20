# -*- coding: utf-8 -*-

import datetime
import string

import pytest
import yaml

from wt.base import ObjectDict, OrderedObjectDict, Content, Post, Page
from wt.decorators import reloadable
from wt.engine import WT
from wt.paginator import Paginator
from wt.utils import init
from wt import server


L = string.ascii_lowercase


@pytest.fixture
def ascii():
    return L


@pytest.fixture(scope='function')
def letters():

    def factory(href='/', **kwargs):
        kwargs.setdefault('page_size', 5)
        kwargs.setdefault('orphans', 2)
        return Paginator(L, href, **kwargs)

    return factory


@pytest.fixture(scope='function',
                params=[{'foo': 12}, {'foo': object()}, {'foo': True}],
                ids=['int', 'object', 'bool'])
def object_dict(request):
    return ObjectDict(**request.param)


@pytest.fixture(scope='function',
                params=[{'foo': {'bar': {'baz': 12}}}],
                ids=['foo-bar-baz'])
def nested_object_dict(request):
    return ObjectDict(**request.param)


@pytest.fixture(scope='function')
def ordered_object_dict():
    return OrderedObjectDict((('foo', 12), ('bar', 'yes'), ('baz', True)))


@pytest.fixture(scope='function')
def object_dict_with_env():
    return ObjectDict({
        'foo': '${URL1}',
        'bar': {
            'baz': '${URL2}'
        },
        'boo': '${HOST}',
    })


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


@pytest.fixture(scope='function')
def missed_config_factory(tmpdir):
    def factory():
        return WT(str(tmpdir.join('missed.yaml')))
    return factory


@pytest.fixture(scope='function')
def broken_config_factory(tmpdir):
    def factory():
        fn = tmpdir.join('broken.yaml')
        fn.write(':foo": "broken config"}')
        return WT(str(fn))
    return factory


@pytest.fixture(scope='function')
def config_is_array_factory(tmpdir):
    def factory():
        fn = tmpdir.join('arr.yaml')
        fn.write('- item 1\n')
        fn.write('- item 2\n')
        return WT(str(fn))
    return factory


EMPTY_CONF = """\
---
title: Empty title
...
"""


@pytest.fixture(scope='function')
def empty_blog(tmpdir):
    fn = tmpdir.join('empty.yaml')
    fn.write_text(EMPTY_CONF, 'utf-8')
    return WT(str(fn))


@pytest.fixture(scope='function')
def sample_wt_path(tmpdir):
    p = str(tmpdir)
    init(p)
    return p


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
def broken_link_factory(tmpdir):

    def factory(**kwargs):
        init(str(tmpdir))
        foo = tmpdir.join('content', 'pages', 'foo.md')
        foo.write('[bar](/bz/)')
        return WT(str(tmpdir.join('wt.yaml')), **kwargs)
    return factory


@pytest.fixture(scope='function')
def mailto_link_factory(tmpdir):

    def factory(**kwargs):
        init(str(tmpdir))
        foo = tmpdir.join('content', 'pages', 'foo.md')
        foo.write('[bar](mailto:bz@bz.co)')
        return WT(str(tmpdir.join('wt.yaml')), **kwargs)
    return factory


FOO_TEMPLATE = """\
{% extends "base.html" %}
{% block content %}
FOO TEMPLATE
{% endblock %}
"""


@pytest.fixture(scope='function')
def custom_template_blog(tmpdir):
    init(str(tmpdir))
    foo_tmpl = tmpdir.join('templates', 'foo.html')
    foo_tmpl.write(FOO_TEMPLATE)
    fn = str(tmpdir.join('wt.yaml'))
    with open(fn, encoding='utf-8') as f:
        conf = yaml.load(f)
    conf['pages'][0]['template'] = 'foo.html'
    with open(fn, 'w') as f:
        yaml.dump(conf, f)
    return WT(fn)


MAINPAGE_PAGED = """\
{% extends "base.html" %}
{% block content %}
{% for item in paginator.items %}
{{ item.title }}<br>
{% endfor %}
{% endblock %}
"""


@pytest.fixture(scope='function')
def paged_blog_factory(tmpdir):

    def factory(**paginate):
        init(str(tmpdir))
        fn = str(tmpdir.join('wt.yaml'))
        with open(fn, encoding='utf-8') as f:
            conf = yaml.load(f)
        conf['posts'] = posts = []
        conf['paginate'] = paginate
        now = datetime.datetime.now() - datetime.timedelta(days=24)
        for x in range(23, 0, -1):
            p = {
                'src': 'bar.md' if x % 2 == 0 else 'baz.md',
                'title': 'Post %02d' % x,
                'url': '/post%02d/' % x,
                'modified': (now + datetime.timedelta(days=x)).isoformat()
            }
            posts.append(p)
        with open(fn, 'w') as f:
            yaml.dump(conf, f)

        mainpage = tmpdir.join('templates', 'mainpage.html')
        mainpage.write(MAINPAGE_PAGED)
        return WT(fn)

    return factory


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
