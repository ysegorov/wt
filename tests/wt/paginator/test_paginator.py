# -*- coding: utf-8 -*-

import pytest

from wt.paginator import BadPaginatorUrlError, BadPaginatorPageError


def describe_Paginator():

    def must_raise_bad_url_error(paginator_factory):
        urls = ['page', '/page', '/page/{page_number}']

        for url in urls:
            with pytest.raises(BadPaginatorUrlError):
                paginator_factory([1, 2, 3], '/', url=url)

    def must_raise_bad_page_error(letters_factory):
        p = letters_factory('/page4.html', page_size=15)
        with pytest.raises(BadPaginatorPageError):
            p.page_num

    def must_properly_paginate_non_paged_data(letters_factory, ascii):
        p = letters_factory(page_size=None)
        assert p.items == ascii
        assert p.num_pages == 1

    def must_properly_handle_num_pages(letters_factory):
        assert letters_factory(orphans=None).num_pages == 6
        assert letters_factory().num_pages == 5
        assert letters_factory('/page2.html',
                               page_size=None,
                               by=10).num_pages == 3

    def must_have_proper_prev_next(letters_factory, ascii):
        pages = [
            '/', '/page2.html', '/page3.html', '/page4.html', '/page5.html']

        for idx, url in enumerate(pages):
            p = letters_factory(url)
            if idx == 0:
                assert p.has_prev is False
                assert p.has_next is True
                assert p.items == ascii[:5]
                assert p.next_page == ('/page2.html', 2)
            elif idx == len(pages) - 1:
                assert p.has_prev is True
                assert p.has_next is False
                assert p.items == ascii[-6:]
                assert p.prev_page == ('/page4.html', 4)
            else:
                assert p.has_prev is True
                assert p.has_next is True
                assert p.prev_page == (pages[idx - 1], idx)
                assert p.next_page == (pages[idx + 1], idx + 2)

    def must_have_proper_first_last(letters_factory):
        assert letters_factory('/page2.html').first_page == ('/', 1)
        assert letters_factory().last_page == ('/page5.html', 5)

    def must_properly_handle_mainpage_is_False(letters_factory):
        p = letters_factory('/page2.html', mainpage=False)
        assert p.prev_page == ('/page1.html', 1)
        assert p.first_page == ('/page1.html', 1)
