# -*- coding: utf -*-

import string

import pytest

from wt.paginator import Paginator


L = string.ascii_lowercase


@pytest.fixture
def paged_letters():
    return Paginator(L, '/', page_size=5, orphans=2)


@pytest.fixture
def paged_letters_no_orphans():
    return Paginator(L, '/', page_size=5)


@pytest.fixture
def non_paged_letters():
    return Paginator(L, '/')


def test_paged_num_pages(paged_letters):
    assert paged_letters.num_pages == 5


def test_paged_num_pages_using_by_in_kwargs():
    p = Paginator(L, '/page2.html', by=10, orphans=2)
    assert p.num_pages == 3


def test_paged_no_orphans_num_pages(paged_letters_no_orphans):
    assert paged_letters_no_orphans.num_pages == 6


def test_non_paged_num_pages(non_paged_letters):
    assert non_paged_letters.num_pages == 1


def test_non_paged_posts(non_paged_letters):
    assert non_paged_letters.posts == L


def test_paged_posts(paged_letters):
    assert paged_letters.posts == L[:5]


def test_paged_posts_orphans():
    p = Paginator(L, '/page5.html', page_size=5, orphans=2)
    assert p.posts == L[-6:]


def test_paged_has_next_true():
    p = Paginator(L, '/page4.html', page_size=5, orphans=2)
    assert p.has_next is True


def test_paged_has_next_false():
    p = Paginator(L, '/page5.html', page_size=5, orphans=2)
    assert p.has_next is False


def test_paged_has_prev_true():
    p = Paginator(L, '/page4.html', page_size=5, orphans=2)
    assert p.has_prev is True


def test_paged_has_prev_false():
    p = Paginator(L, '/', page_size=5, orphans=2)
    assert p.has_prev is False


def test_paged_next_page():
    p = Paginator(L, '/', page_size=5, orphans=2)
    assert p.next_page == ('/page2.html', 2)


def test_paged_prev_page_mainpage():
    p = Paginator(L, '/page2.html', page_size=5, orphans=2)
    assert p.prev_page == ('/', 1)


def test_paged_prev_page_no_mainpage():
    p = Paginator(L, '/page2.html', mainpage=False, page_size=5, orphans=2)
    assert p.prev_page == ('/page1.html', 1)


def test_paged_first_page_with_mainpage():
    p = Paginator(L, '/page2.html', page_size=5, orphans=2)
    assert p.first_page == ('/', 1)


def test_paged_first_page_without_mainpage():
    p = Paginator(L, '/page2.html', mainpage=False, page_size=5, orphans=2)
    assert p.first_page == ('/page1.html', 1)


def test_paged_last_page(paged_letters):
    assert paged_letters.last_page == ('/page5.html', 5)


def test_bad_page():
    p = Paginator(list(range(10)), '/page4.html', page_size=5)
    with pytest.raises(Paginator.BadPageError):
        p.page_num


def test_url_is_not_absolute():
    with pytest.raises(Paginator.BadUrlError):
        Paginator([1, 2, 3], '/', url='page')


def test_url_has_no_placeholder():
    with pytest.raises(Paginator.BadUrlError):
        Paginator([1, 2, 3], '/', url='/page')


def test_url_is_not_dir_not_html():
    with pytest.raises(Paginator.BadUrlError):
        Paginator([1, 2, 3], '/', url='/page/{page_number}')
