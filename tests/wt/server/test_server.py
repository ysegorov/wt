# -*- coding: utf-8 -*-


def describe_server_app():

    async def must_properly_serve_pages(server_app_factory, test_client, loop):
        pages = [
            # (url, content)
            ('/', None),
            ('/atom.xml', None),
            ('/foo/', 'foo page title'),
            ('/bar/', 'bar page title'),
            ('/baz/', 'baz page title'),
            ('/css/style.css', '/*styles*/')
        ]
        client = await test_client(server_app_factory)

        for url, content in pages:
            resp = await client.get(url)
            assert resp.status == 200
            if content is not None:
                text = await resp.text()
                assert content in text.strip().lower()

    async def must_return_404_for_unknown_url(server_app_factory,
                                              test_client, loop):
        client = await test_client(server_app_factory)
        resp = await client.get('/something/')
        assert resp.status == 404

    async def must_return_500_if_broken_template(broken_server_app_factory,
                                                 test_client, loop):
        client = await test_client(broken_server_app_factory)
        resp = await client.get('/foo/')
        assert resp.status == 500
