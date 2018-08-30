# -*- coding: utf-8 -*-


def describe_make_jinja_filter():

    def must_return_callable(markdown_filter_factory):

        fltr = markdown_filter_factory('')

        assert callable(fltr)


def describe_BaseurlTreeprocessor():

    def must_not_prepend_baseurl_if_it_is_empty(markdown_filter_factory,
                                                markdown_content):
        fltr = markdown_filter_factory('')

        html = fltr(markdown_content)

        assert 'href="/bar/"' in html
        assert 'src="/logo96.png"' in html

    def must_prepend_baseurl_if_it_is_not_empty(markdown_filter_factory,
                                                markdown_content):
        fltr = markdown_filter_factory('/base-url')

        html = fltr(markdown_content)

        assert 'href="/base-url/bar/"' in html
        assert 'src="/base-url/logo96.png"' in html
