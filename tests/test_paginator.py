# -*- coding: utf -*-

import pytest

from wt.exceptions import BadPaginatorUrlError, BadPaginatorPageError
from wt.paginator import Paginator


def letters__num_pages__equals_5(letters):
    assert letters().num_pages == 5


def letters__num_pages_using_by_10_in_kwargs__equals_3(letters):
    p = letters('/page2.html', page_size=None, by=10)
    assert p.num_pages == 3


def letters__no_orphans_num_pages__equals_6(letters):
    assert letters(orphans=None).num_pages == 6


def letters__non_paged_num_pages__equals_1(letters):
    assert letters(page_size=None).num_pages == 1


def letters__non_paged_items__equals_original_list(letters, ascii):
    p = letters(page_size=None)
    assert p.items == ascii


def letters__paged_items_first_page__equals_first_five_ascii(letters, ascii):
    assert letters().items == ascii[:5]


def letters__paged_items_orphans__moved_to_previous_page(letters, ascii):
    p = letters('/page5.html')
    assert p.items == ascii[-6:]


def letters__non_last_page_has_next__is_true(letters):
    p = letters('/page4.html')
    assert p.has_next is True


def letters__last_page_has_next__is_false(letters):
    p = letters('/page5.html')
    assert p.has_next is False


def letters__non_first_page_has_prev__is_true(letters):
    p = letters('/page4.html')
    assert p.has_prev is True


def letters__first_page_has_prev__is_false(letters):
    assert letters().has_prev is False


def letters__first_page_next_page__is_second_page(letters):
    assert letters().next_page == ('/page2.html', 2)


def letters__second_page_prev_page__is_mainpage(letters):
    assert letters('/page2.html').prev_page == ('/', 1)


def letters_with_no_mainpage__second_page_prev_page__is_first_page(letters):
    p = letters('/page2.html', mainpage=False)
    assert p.prev_page == ('/page1.html', 1)


def letters__second_page_first_page__is_mainpage(letters):
    assert letters('/page2.html').first_page == ('/', 1)


def letters_with_no_mainpage__second_page_first_page__is_first_page(letters):
    p = letters('/page2.html', mainpage=False)
    assert p.first_page == ('/page1.html', 1)


def letters__last_page__is_fifth_page(letters):
    assert letters().last_page == ('/page5.html', 5)


def letters__wrong_page__raises_bad_page_error(letters):
    p = letters('/page4.html', page_size=15)
    with pytest.raises(BadPaginatorPageError):
        p.page_num


def paginator_with_not_absolute_url__raises_bad_url_error():
    with pytest.raises(BadPaginatorUrlError):
        Paginator([1, 2, 3], '/', url='page')


def paginator_with_url_without_placeholder__raises_bad_url_error():
    with pytest.raises(BadPaginatorUrlError):
        Paginator([1, 2, 3], '/', url='/page')


def paginator_with_url_which_is_neither_dir_nor_html__raises_bad_url_error():
    with pytest.raises(BadPaginatorUrlError):
        Paginator([1, 2, 3], '/', url='/page/{page_number}')
