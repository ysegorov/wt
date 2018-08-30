# -*- coding: utf-8 -*-


def describe_HTMLParser():

    def must_properly_find_local_links(parser_factory, parser_fixture):

        for html, expected in parser_fixture:
            parser = parser_factory()
            links = parser.get_links(html)
            assert links == expected
