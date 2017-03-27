# -*- coding: utf-8 -*-

import os

import pytest

from wt.exceptions import UrlNotFoundError, InvalidLocalLinkError


def describe_WT():

    def must_properly_handle_empty_blog(empty_blog):
        assert len(empty_blog.pages) == 0
        assert len(empty_blog.posts) == 0
        assert hasattr(empty_blog, 'conf')
        assert hasattr(empty_blog.conf, 'title')
        assert empty_blog.conf.title == 'Empty title'
        assert 'empty title' in empty_blog.render('/').lower()
        assert 'empty title' in empty_blog.render('/atom.xml').lower()
        with pytest.raises(UrlNotFoundError):
            empty_blog.render('/foo/')

    def must_properly_handle_blog(blog):
        assert len(blog.pages) == 1
        assert len(blog.posts) == 2
        assert '/foo/' in blog.pages and '/foo/' not in blog.posts
        assert '/bar/' in blog.posts and '/bar/' not in blog.pages
        assert '/baz/' in blog.posts and '/baz/' not in blog.pages

        for url, content in [('/foo/', 'foo page title'),
                             ('/bar/', 'bar page title'),
                             ('/baz/', 'baz page title')]:
            html = blog.render(url)
            assert html is not None and content in html.lower()

        assert os.path.isfile(
            os.path.join(blog.static_root, 'css', 'style.css'))

        blog.build()

        for parts in [('index.html', ),
                      ('atom.xml', ),
                      ('foo', 'index.html'),
                      ('bar', 'index.html'),
                      ('baz', 'index.html'),
                      ('css', 'style.css')]:
            assert os.path.exists(os.path.join(blog.output_path, *parts))

    def must_properly_handle_blog_rebuild(blog):
        blog.build()
        output = str(blog.output_path)
        prev_ctime = os.stat(output).st_ctime
        blog.build()
        next_ctime = os.stat(output).st_ctime
        # TODO find better assert
        assert next_ctime > prev_ctime

    def must_properly_handle_blog_without_static_build(blog_without_static):
        blog_without_static.build()
        assert not os.path.exists(
            os.path.join(blog_without_static.output_path, 'css', 'style.css'))

    def must_properly_handle_blog_with_bad_link(blog_with_bad_link_factory,
                                                caplog):
        blog = blog_with_bad_link_factory()
        blog.render('/foo/')
        assert 'bad local link "/bz/"' in caplog.text.lower()

        blog = blog_with_bad_link_factory(is_prod=True)
        with pytest.raises(InvalidLocalLinkError):
            blog.build()

    def must_properly_handle_paged_blog(paged_blog_factory):
        blog = paged_blog_factory(by=10, orphans=2)

        assert len(blog.posts) == 23

        with pytest.raises(UrlNotFoundError):
            blog.render('/page4.html')

        for url, first, last in (('/', 14, 23),
                                 ('/page2.html', 4, 13),
                                 ('/page3.html', 1, 3)):
            content = blog.render(url)
            assert content is not None

            content = content.lower()
            for x in range(1, 24):
                title = 'post %02d' % x
                if x >= first and x <= last:
                    assert title in content
                else:
                    assert title not in content

    def must_properly_handle_paged_blog_orphans(paged_blog_factory):
        blog = paged_blog_factory(by=7, orphans=2)

        with pytest.raises(UrlNotFoundError):
            blog.render('/page4.html')

        content = blog.render('/page3.html').lower()

        for x in range(1, 10):
            title = 'post %02d' % x
            assert title in content

    def must_provide_log_message_if_missing_config(wt_factory, tmpdir, caplog):
        wt_factory(tmpdir.join('missed.yaml'))
        assert 'missing config' in caplog.text.lower()

    def must_provide_log_message_if_bad_config(wt_factory, tmpdir, caplog):

        fn = tmpdir.join('broken.yaml')
        fn.write(':foo": "broken config"}')
        wt_factory(fn)
        assert 'error parsing' in caplog.text.lower()

        fn = tmpdir.join('arr.yaml')
        fn.write('- item 1\n')
        fn.write('- item 2\n')
        wt_factory(fn)
        assert 'expected to be a dict, got "list"' in caplog.text.lower()
