# -*- coding: utf-8 -*-

import os
from pathlib import Path

from wt import server


dn = os.path.dirname
root = dn(__file__)
config = str(Path(root, 'fixtures', 'custom', 'wt.yaml'))
broken_config = str(Path(root, 'fixtures', 'broken_template', 'wt.yaml'))


def create_app(loop):
    return server.aiohttp_app(config, loop=loop)


async def test_mainpage(test_client, loop):
    client = await test_client(create_app)
    resp = await client.get('/')
    assert resp.status == 200


async def test_static(test_client, loop):
    client = await test_client(create_app)
    resp = await client.get('/style.css')
    assert resp.status == 200
    text = await resp.text()
    assert 'custom blog style ' in text.strip().lower()


async def test_posts_pages(test_client, loop):
    client = await test_client(create_app)
    for slug in ('foo', 'bar', 'baz'):
        resp = await client.get('/{}/'.format(slug))
        assert resp.status == 200
        text = await resp.text()
        text = text.strip().lower()
        assert '{} content'.format(slug) in text


async def test_feed(test_client, loop):
    client = await test_client(create_app)
    resp = await client.get('/atom.xml')
    assert resp.status == 200


async def test_404(test_client, loop):
    client = await test_client(create_app)
    resp = await client.get('/something/')
    assert resp.status == 404


async def test_500(test_client, loop):

    def app(loop):
        return server.aiohttp_app(broken_config, loop=loop)

    client = await test_client(app)
    resp = await client.get('/foo/')
    assert resp.status == 500
