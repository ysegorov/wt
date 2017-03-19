# -*- coding: utf-8 -*-

from wt.parser import HTMLParser


def parser__get_links__returns_dict():
    p = HTMLParser()
    links = p.get_links('')
    assert isinstance(links, dict)


def parser__get_links__returns_link_for_href_attr():
    p = HTMLParser()
    links = p.get_links('<a href="/foo">foo</a>')
    assert len(links) == 1 and '/foo' in links


def parser__get_links__returns_link_for_src_attr():
    p = HTMLParser()
    links = p.get_links('<img src="/foo/a.png">')
    assert len(links) == 1 and '/foo/a.png' in links


def parser__get_links__returns_lines_numbers__for_links():
    p = HTMLParser()
    links = p.get_links('<a href="/foo">foo</a>\nBar\n<a href="/foo">foo</a>')
    assert len(links) == 1 and links['/foo'] == [(1, 0), (3, 0)]


def parser__get_links__ignores_links_within_code_tag():
    p = HTMLParser()
    links = p.get_links('<code><a href="/foo">foo</a></code>')
    assert len(links) == 0


def parser__get_links__properly_skips_code_tag():
    p = HTMLParser()
    links = p.get_links(
        '<a href="/foo">foo</a>\n'
        '<code><a href="/bar">bar</a></code>\n'
        '<a href="/baz">baz</a>\n')
    assert len(links) == 2 and '/foo' in links and '/baz' in links
