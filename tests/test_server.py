# -*- coding: utf-8 -*-


async def server_app__get_mainpage_status__is_ok(server_app_factory,
                                                 test_client, loop):
    client = await test_client(server_app_factory)
    resp = await client.get('/')
    assert resp.status == 200


async def server_app__get_static_status__is_ok(server_app_factory,
                                               test_client, loop):
    client = await test_client(server_app_factory)
    resp = await client.get('/css/style.css')
    assert resp.status == 200


async def server_app__get_static_content__contains_text(server_app_factory,
                                                        test_client, loop):
    client = await test_client(server_app_factory)
    resp = await client.get('/css/style.css')
    text = await resp.text()
    assert '/*styles*/' in text.strip().lower()


async def server_app__get_content_status__is_ok(server_app_factory,
                                                test_client, loop):
    client = await test_client(server_app_factory)
    for slug in ('foo', 'bar', 'baz'):
        resp = await client.get('/{}/'.format(slug))
        assert resp.status == 200


async def server_app__get_content_html__contains_text(server_app_factory,
                                                      test_client, loop):
    client = await test_client(server_app_factory)
    for slug in ('foo', 'bar', 'baz'):
        resp = await client.get('/{}/'.format(slug))
        text = await resp.text()
        text = text.strip().lower()
        assert '{} page title'.format(slug) in text


async def server_app__get_feed_status__is_ok(server_app_factory,
                                             test_client, loop):
    client = await test_client(server_app_factory)
    resp = await client.get('/atom.xml')
    assert resp.status == 200


async def server_app__get_wrong_url_status__is_404(server_app_factory,
                                                   test_client, loop):
    client = await test_client(server_app_factory)
    resp = await client.get('/something/')
    assert resp.status == 404


async def broken_server_app_get_foo_status__500(broken_server_app_factory,
                                                test_client, loop):

    client = await test_client(broken_server_app_factory)
    resp = await client.get('/foo/')
    assert resp.status == 500
