# -*- coding: utf-8 -*-

import pytest

from wt.parser import HTMLParser


@pytest.fixture(scope='function')
def parser_factory():

    def factory():
        return HTMLParser()

    return factory


@pytest.fixture(scope='function')
def parser_fixture():
    d = [
        ('<a href="/foo">foo</a>',
         {'/foo': [(1, 0)]}),
        ('<img src="/foo/a.png">',
         {'/foo/a.png': [(1, 0)]}),
        ('<span><img src="/foo/a.png"></span>',
         {'/foo/a.png': [(1, 6)]}),
        ('<a href="/foo">foo</a>\nBar\n<a href="/foo">foo</a>',
         {'/foo': [(1, 0), (3, 0)]}),
        ('<code><a href="/foo">foo</a></code>',
         {}),
        ('<a href="/foo">foo</a>\n'
         '<code><a href="/bar">bar</a></code>\n'
         '<a href="/baz">baz</a>\n',
         {'/foo': [(1, 0)], '/baz': [(3, 0)]}),
    ]
    return d
