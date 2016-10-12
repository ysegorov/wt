# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
from pathlib import Path
from shutil import copytree, rmtree

import jinja2
import pytest

import wt.cli  # noqa
from wt.blog import Config, Content, Page, Post, Blog, blog, build, init


dn = os.path.dirname
root = dn(__file__)
fixtures_dir = Path(root, 'fixtures')


def test_config():

    o = object()
    c = Config(foo=o)

    assert c.foo is o
    assert c.foo is c['foo']
    assert c.bar is None

    c = Config(foo={'foo': 1, 'x': None, 'y': True, 'z': False},
               baz={'baz': {'baz': 2}},
               bar=3)

    assert c.path('foo.foo') == 1
    assert c.path('baz.baz.baz') == 2
    assert c.path('bar') == 3
    assert c.path('foo.a') is None
    assert c.path('foo.a.b', 'missed') == 'missed'
    assert c.path('foo.x') is None
    assert c.path('foo.x', 1) == 1
    assert c.path('foo.y') is True
    assert c.path('foo.y', 2) is True
    assert c.path('foo.z', True) is False

    with pytest.raises(ValueError):
        c.path('bar.a.b')


def test_content(tmpdir):

    c = Content(src='a.md')

    assert c.src == 'a.md'
    assert c.src == c['src']

    assert c.info is None
    c.info = 'info'
    assert c['info'] == 'info'
    assert c.info == c['info']

    c = Content.from_dict(str(tmpdir), {'src': 'a.md'})
    target = tmpdir.mkdir(Content.content_dirname).join('a.md')
    assert c.src == str(target)
    assert c.text == ''

    target.write('text')

    assert c.text == 'text'


def test_page(tmpdir):
    p = Page.from_dict(str(tmpdir), {'src': 'a.md'})
    target = tmpdir\
        .mkdir(Page.content_dirname).mkdir(Page.data_dirname).join('a.md')
    assert not os.path.isfile(str(target))
    assert p.text == ''

    target.write('page')

    assert p.text == 'page'


def test_post(tmpdir):
    p = Post.from_dict(str(tmpdir), {'src': 'a.md'})
    target = tmpdir\
        .mkdir(Post.content_dirname).mkdir(Post.data_dirname).join('a.md')
    assert not os.path.isfile(str(target))
    assert p.text == ''

    target.write('post')

    assert p.text == 'post'


def missed_blog():
    p = fixtures_dir.joinpath('foo', 'missed.yaml')
    return blog(str(p))


def broken_blog():
    p = fixtures_dir.joinpath('broken_config', 'wt.yaml')
    return blog(str(p))


def empty_blog():
    p = fixtures_dir.joinpath('empty', 'empty.yaml')
    return blog(str(p))


def blog_with_pages():
    p = fixtures_dir.joinpath('with_pages', 'wt.yaml')
    return blog(str(p))


def blog_with_posts():
    p = fixtures_dir.joinpath('with_posts', 'wt.yaml')
    return blog(str(p))


def custom_blog(conf='wt.yaml'):
    p = fixtures_dir.joinpath('custom', conf)
    return blog(str(p))


def test_missed_broken_blog_config(caplog):

    mb = missed_blog()
    bb = broken_blog()
    assert isinstance(mb, Blog)
    assert isinstance(bb, Blog)
    assert 'error parsing yaml' in caplog.text.lower()


def test_empty_blog():

    eb = empty_blog()

    assert isinstance(eb, Blog)
    assert isinstance(eb.conf, Config)
    assert isinstance(eb.env, jinja2.Environment)
    assert isinstance(eb.pages, dict)
    assert len(eb.pages) == 0
    assert isinstance(eb.posts, OrderedDict)
    assert len(eb.posts) == 0
    assert eb.conf.title == 'Empty Title'
    assert eb.workdir == str(fixtures_dir.joinpath('empty'))
    assert eb.static_root == str(fixtures_dir.joinpath('empty', 'static'))

    with pytest.raises(Blog.NotFound):
        eb.render('/baz/')

    mainpage = eb.render('/')
    assert 'empty title' in mainpage.lower()

    feed = eb.render('/atom.xml')
    assert 'empty title' in feed.lower()


def test_blog_with_pages():

    bwp = blog_with_pages()

    assert isinstance(bwp, Blog)
    assert len(bwp.pages) > 0
    assert '/foo/' in bwp.pages

    with pytest.raises(Blog.NotFound):
        bwp.render('/baz/')

    content = bwp.render('/foo/')
    assert content is not None
    assert 'foo page' in content.lower()
    assert 'foo page content' in content.lower()


def test_blog_with_posts():

    bwp = blog_with_posts()

    assert isinstance(bwp, Blog)
    assert len(bwp.posts) > 0
    assert '/foo/' in bwp.posts

    with pytest.raises(Blog.NotFound):
        bwp.render('/baz/')

    assert list(bwp.posts.keys()) == ['/foo/', '/bar/']

    content = bwp.render('/foo/')
    assert content is not None
    assert 'foo page' in content.lower()
    assert 'foo page content' in content.lower()


def test_custom_blog():
    cb = custom_blog()

    assert isinstance(cb, Blog)
    assert len(cb.pages) == 1
    assert len(cb.posts) == 2
    assert '/foo/' in cb.pages
    assert '/bar/' in cb.posts
    assert '/baz/' in cb.posts

    mainpage = cb.render('/')
    mainpage = mainpage.lower()
    assert 'custom fixture' in mainpage
    assert 'bar title' in mainpage
    assert 'baz title' in mainpage

    feed = cb.render('/atom.xml')
    assert 'test: custom fixture' in feed.lower()

    for slug in ('foo', 'bar', 'baz'):
        content = cb.render('/{}/'.format(slug))
        content = content.lower()
        assert '{} title'.format(slug) in content
        assert '{} content'.format(slug) in content


def test_build(tmpdir):
    p = fixtures_dir.joinpath('custom')
    copytree(str(p), str(tmpdir.join('custom')))

    conf = tmpdir.join('custom', 'wt.yaml')
    target = tmpdir.join('custom', 'output')
    assert conf.exists()
    assert not target.exists()

    build(str(conf))

    assert target.exists()

    files = (
        ('index.html',),
        ('foo', 'index.html'),
        ('baz', 'index.html'),
        ('bar', 'index.html'),
        ('atom.xml', )
    )

    for path in files:
        assert target.join(*path).exists()

    assert not target.join('style.css').exists()

    rmtree(str(target))
    target = tmpdir.join('custom', 'build')
    target.mkdir()
    conf = tmpdir.join('custom', 'wt_with_static.yaml')

    build(str(conf))

    for path in files:
        assert target.join(*path).exists()

    assert target.join('style.css').exists()


def test_without_feed(tmpdir):
    p = fixtures_dir.joinpath('custom')
    copytree(str(p), str(tmpdir.join('custom')))

    conf = tmpdir.join('custom', 'wt_without_feed.yaml')
    target = tmpdir.join('custom', 'output')
    assert conf.exists()
    assert not target.exists()

    build(str(conf))

    assert not target.join('atom.xml').exists()


def test_init(tmpdir):

    p = tmpdir
    init(str(p))

    assert p.join('wt.yaml').exists()
    assert p.join('templates', 'mainpage.html').exists()
    assert p.join('templates', 'content.html').exists()
    assert p.join('templates', 'atom.xml').exists()
