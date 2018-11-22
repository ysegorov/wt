# -*- coding: utf-8 -*-

from wt import html


def describe_is_local_link():

    def must_return_proper_value():

        pairs = [
            ('https://goo.gl', False),
            ('http://goo.gl', False),
            ('//goo.gl', False),
            ('/', True),
            ('/foo', True),
            ('http://127.0.0.1:9000/', False),
            ('/img/logo.jpg', True),
            ('https://localhost/baz', False),
            ('#hdr', False),
            ('?foo=baz', False),
            ('/foo#hdr', True),
            ('/foo?baz=bar', True),
        ]

        for url, expected in pairs:
            parsed_link = html.parse_link(url)
            assert html.is_local_link(parsed_link) is expected


def describe_HTMLParser():

    def must_properly_find_local_links(parser_factory, parser_fixture):

        for text, expected in parser_fixture:
            parser = parser_factory()
            links = parser.get_links(text)
            assert links == expected
