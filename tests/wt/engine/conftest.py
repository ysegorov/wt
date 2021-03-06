# -*- coding: utf-8 -*-

import datetime

import yaml
import pytest

from wt.engine import WT
from wt.utils import init


@pytest.fixture(scope='session')
def wt_factory():

    def factory(config, **kwargs):
        return WT(str(config), **kwargs)

    return factory


EMPTY_CONF = """\
---
title: Empty title
...
"""


@pytest.fixture(scope='function')
def empty_blog(tmpdir, wt_factory):
    fn = tmpdir.join('empty.yaml')
    fn.write_text(EMPTY_CONF, 'utf-8')
    return wt_factory(fn)


@pytest.fixture(scope='function')
def blog(wt_factory, tmpdir):
    init(str(tmpdir))
    return wt_factory(tmpdir.join('wt.yaml'))


@pytest.fixture(scope='function')
def baseurl_factory():

    def factory(url):
        return '/base-url{}'.format(url)

    return factory


@pytest.fixture(scope='function')
def blog_with_baseurl(wt_factory, baseurl_factory, tmpdir):
    init(str(tmpdir))
    fn = str(tmpdir.join('wt.yaml'))
    with open(fn, encoding='utf-8') as f:
        conf = yaml.load(f)
    conf['baseurl'] = baseurl_factory('')
    with open(fn, 'w') as f:
        yaml.dump(conf, f)
    return wt_factory(tmpdir.join('wt.yaml'), is_prod=True)


@pytest.fixture(scope='function')
def blog_without_static(wt_factory, tmpdir):
    init(str(tmpdir))
    fn = str(tmpdir.join('wt.yaml'))
    with open(fn, encoding='utf-8') as f:
        conf = yaml.load(f)
    conf['build']['static'] = False
    with open(fn, 'w') as f:
        yaml.dump(conf, f)
    return wt_factory(tmpdir.join('wt.yaml'))


@pytest.fixture(scope='function')
def blog_with_bad_link_factory(wt_factory, tmpdir):

    def factory(is_prod=False):
        init(str(tmpdir))
        foo = tmpdir.join('content', 'pages', 'foo.md')
        foo.write('---\nurl: /foo/\n---\n[bar](/bz/)')
        return wt_factory(tmpdir.join('wt.yaml'), is_prod=is_prod)

    return factory


@pytest.fixture(scope='function')
def blog_with_missed_config(wt_factory, tmpdir):
    fn = tmpdir.join('missed.yaml')
    return wt_factory(fn)


@pytest.fixture(scope='function')
def blog_with_pages_without_url(wt_factory, tmpdir):
    init(str(tmpdir))
    foo = tmpdir.join('content', 'pages', 'foo.md')
    foo.write('foo page content')
    foo1 = tmpdir.join('content', 'pages', 'foo1.md')
    foo1.write('---\nurl: ""\n---\nfoo1 page content')

    return wt_factory(tmpdir.join('wt.yaml'))


MAINPAGE_PAGED = """\
{% extends "base.html" %}
{% block content %}
{% for item in paginator.items %}
{{ item.title }}<br>
{% endfor %}
{% endblock %}
"""


@pytest.fixture(scope='function')
def paged_blog_factory(wt_factory, tmpdir):

    def factory(**paginate):
        init(str(tmpdir))
        tmpdir.join('content', 'posts').remove(ignore_errors=True)
        fn = str(tmpdir.join('wt.yaml'))
        with open(fn, encoding='utf-8') as f:
            conf = yaml.load(f)
        conf['paginate'] = paginate
        with open(fn, 'w') as f:
            yaml.dump(conf, f)
        now = datetime.datetime.now() - datetime.timedelta(days=24)
        for x in range(23, 0, -1):
            modified = (now + datetime.timedelta(days=x)).isoformat()
            src = tmpdir.join('content', 'posts', 'post-%02d.md' % x)
            text = [
                '---',
                'url: /post%02d/' % x,
                'title: Post %02d' % x,
                'modified: %s' % modified,
                '---',
                'bar' if x % 2 == 0 else 'baz',
            ]
            src.write('\n'.join(text), ensure=True)

        mainpage = tmpdir.join('templates', 'mainpage.html')
        mainpage.write(MAINPAGE_PAGED)
        return wt_factory(fn)

    return factory
