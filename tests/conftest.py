# -*- coding: utf-8 -*-

import datetime

import pytest
import yaml

from wt.engine import WT
from wt.utils import init


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
def sample_blog(tmpdir):
    init(str(tmpdir))
    return WT(str(tmpdir.join('wt.yaml')))


@pytest.fixture(scope='function')
def sample_blog_without_static(tmpdir):
    init(str(tmpdir))
    fn = str(tmpdir.join('wt.yaml'))
    with open(fn, encoding='utf-8') as f:
        conf = yaml.load(f)
    conf['build']['static'] = False
    with open(fn, 'w') as f:
        yaml.dump(conf, f)
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
