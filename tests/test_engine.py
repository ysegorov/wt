# -*- coding: utf-8 -*-

import os

import pytest

from wt.base import Config
from wt.exceptions import UrlNotFoundError, InvalidLocalLinkError


def missed_config__init__emits_error_in_log(missed_config_factory, caplog):
    missed_config_factory()
    assert 'missing config' in caplog.text.lower()


def broken_config__init__emits_error_in_log(broken_config_factory, caplog):
    broken_config_factory()
    assert 'error parsing' in caplog.text.lower()


def config_is_array__init__emits_error_in_log(config_is_array_factory, caplog):
    config_is_array_factory()
    assert 'error parsing' in caplog.text.lower()


def empty_blog__conf__is_config_instance(empty_blog):
    assert isinstance(empty_blog.conf, Config)


def empty_blog__pages_attr__has_zero_length(empty_blog):
    assert len(empty_blog.pages) == 0


def empty_blog__posts_attr__has_zero_length(empty_blog):
    assert len(empty_blog.posts) == 0


def empty_blog__render_non_mainpage_url__raises(empty_blog):
    with pytest.raises(UrlNotFoundError):
        empty_blog.render('/foo/')


def empty_blog__conf_title__equals_empty_title(empty_blog):
    assert empty_blog.conf.title == 'Empty title'


def empty_blog__render_mainpage__contains_config_title(empty_blog):
    assert 'empty title' in empty_blog.render('/').lower()


def empty_blog__render_feed__contains_config_title(empty_blog):
    assert 'empty title' in empty_blog.render('/atom.xml').lower()


def sample_blog__pages_length__equals_to_one(sample_blog):
    assert len(sample_blog.pages) == 1


def sample_blog__pages_attr__has_foo_url(sample_blog):
    assert '/foo/' in sample_blog.pages


def sample_blog__pages_attr__doesnt_have_bar_url(sample_blog):
    assert '/bar/' not in sample_blog.pages


def sample_blog__render_foo__has_output(sample_blog):
    assert sample_blog.render('/foo/') is not None


def sample_blog__render_foo__has_foo_title_in_body(sample_blog):
    assert 'foo page title' in sample_blog.render('/foo/').lower()


def sample_blog__render_foo__has_foo_page_title_in_page(sample_blog):
    assert 'foo page title' in sample_blog.render('/foo/').lower()


def sample_blog__posts_length__equals_to_two(sample_blog):
    assert len(sample_blog.posts) == 2


def sample_blog__posts_attr__has_bar_url(sample_blog):
    assert '/bar/' in sample_blog.posts


def sample_blog__posts_attr__has_baz_url(sample_blog):
    assert '/baz/' in sample_blog.posts


def sample_blog__posts_attr__doesnt_have_foo_url(sample_blog):
    assert '/foo/' not in sample_blog.posts


def sample_blog__render_bar__has_output(sample_blog):
    assert sample_blog.render('/bar/') is not None


def sample_blog__render_bar__has_bar_title_in_body(sample_blog):
    assert 'bar post title' in sample_blog.render('/bar/').lower()


def sample_blog__render_bar__has_bar_page_title_in_page(sample_blog):
    assert 'bar page title' in sample_blog.render('/bar/').lower()


def sample_blog__static_root_dir__contains_style_css(sample_blog):
    assert os.path.isfile(
        os.path.join(sample_blog.static_root, 'css', 'style.css'))


def broken_link_blog__render_foo__emits_warning_in_log(broken_link_factory,
                                                       caplog):
    broken_link_blog = broken_link_factory()
    broken_link_blog.render('/foo/')
    assert 'bad local link "/bz/"' in caplog.text.lower()


def broken_link_blog__build__raises_invalidlocalinkerror(broken_link_factory):
    broken_link_blog = broken_link_factory(is_prod=True)
    with pytest.raises(InvalidLocalLinkError):
        broken_link_blog.build()


def mailto_link_blog__build__is_ok(mailto_link_factory):
    mailto_link_blog = mailto_link_factory(is_prod=True)
    mailto_link_blog.build()
    output = str(mailto_link_blog.output_path)
    assert os.path.exists(os.path.join(output, 'foo', 'index.html'))


def custom_template_blog__render__uses_foo_template(custom_template_blog):
    content = custom_template_blog.render('/foo/')
    assert 'FOO TEMPLATE' in content


def paged_blog__posts_length__equals_to_23(paged_blog_factory):
    b = paged_blog_factory()
    assert len(b.posts) == 23


def paged_blog__wrong_page__raises_not_found_error(paged_blog_factory):
    b = paged_blog_factory(by=10, orphans=2)
    with pytest.raises(UrlNotFoundError):
        b.render('/page4.html')


def paged_blog__correct_page__has_content_rendered(paged_blog_factory):
    b = paged_blog_factory(by=10, orphans=2)
    for url, first, last in (('/', 21, 23),
                             ('/page2.html', 11, 20),
                             ('/page3.html', 1, 10)):
        assert b.render(url) is not None


def paged_blog__page_render__has_proper_items(paged_blog_factory):
    b = paged_blog_factory(by=10, orphans=2)
    for url, first, last in (('/', 14, 23),
                             ('/page2.html', 4, 13),
                             ('/page3.html', 1, 3)):
        content = b.render(url).lower()
        for x in range(first, last + 1):
            title = 'post %02d' % x
            assert title in content


def paged_blog__page_render__doesnt_have_wrong_items(paged_blog_factory):
    b = paged_blog_factory(by=10, orphans=2)
    for url, first, last in (('/', 14, 23),
                             ('/page2.html', 4, 13),
                             ('/page3.html', 1, 3)):
        content = b.render(url).lower()
        for x in range(1, 24):
            if x >= first and x <= last:
                continue
            title = 'post %02d' % x
            assert title not in content


def paged_blog__orphans_page__raises_url_not_found_error(paged_blog_factory):
    b = paged_blog_factory(by=7, orphans=2)
    with pytest.raises(UrlNotFoundError):
        b.render('/page4.html')


def paged_blog__last_page__has_orphans_in_content(paged_blog_factory):
    b = paged_blog_factory(by=7, orphans=2)
    content = b.render('/page3.html').lower()

    for x in range(1, 10):
        title = 'post %02d' % x
        assert title in content


def sample_blog__build__has_pages_rendered(sample_blog):
    sample_blog.build()
    output = str(sample_blog.output_path)
    assert os.path.exists(os.path.join(output, 'foo', 'index.html'))


def sample_blog__build__has_posts_rendered(sample_blog):
    sample_blog.build()
    output = str(sample_blog.output_path)
    for p in ('bar', 'baz'):
        assert os.path.exists(os.path.join(output, p, 'index.html'))


def sample_blog__build__has_mainpage_rendered(sample_blog):
    sample_blog.build()
    output = str(sample_blog.output_path)
    assert os.path.exists(os.path.join(output, 'index.html'))


def sample_blog__build__has_feed_rendered(sample_blog):
    sample_blog.build()
    output = str(sample_blog.output_path)
    assert os.path.exists(os.path.join(output, 'atom.xml'))


def sample_blog__build__has_static_copied(sample_blog):
    sample_blog.build()
    output = str(sample_blog.output_path)
    assert os.path.exists(os.path.join(output, 'css', 'style.css'))


def sample_blog__build_without_static__doesnt_have_static_copied(sample_blog):
    sample_blog.conf.build['static'] = False
    sample_blog.build()
    output = str(sample_blog.output_path)
    assert not os.path.exists(os.path.join(output, 'css', 'style.css'))


def sample_blog__repeatable_build__cleans_output(sample_blog):
    sample_blog.build()
    output = str(sample_blog.output_path)
    prev_ctime = os.stat(output).st_ctime
    sample_blog.build()
    next_ctime = os.stat(output).st_ctime
    # TODO find better assert
    assert next_ctime > prev_ctime
