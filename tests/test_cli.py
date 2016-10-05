# -*- coding: utf-8 -*-

import os

from wt import cli


def test_develop():

    args = cli.parse_args(['develop'])
    assert args.command == 'develop'
    assert args.port == 9000
    assert args.host == '127.0.0.1'
    assert args.config.endswith('wt.yaml')

    args = cli.parse_args(['-c', 'conf.yaml', 'develop'])
    assert args.config.endswith('conf.yaml')

    args = cli.parse_args(['-c', '/tmp/conf.yaml', 'develop'])
    assert args.config == '/tmp/conf.yaml'

    args = cli.parse_args(['develop', '--host', '0.0.0.0'])
    assert args.host == '0.0.0.0'

    args = cli.parse_args(['develop', '--port', '5000'])
    assert args.port == 5000


def test_build():

    args = cli.parse_args(['build'])
    assert args.command == 'build'


def test_init():

    args = cli.parse_args(['init', '.'])
    assert args.command == 'init'
    assert args.path == os.path.abspath(os.curdir)

    args = cli.parse_args(['init', '/some/absolute/path'])
    assert args.path == '/some/absolute/path'

    args = cli.parse_args(['init', 'some/relative/path'])
    assert args.path == os.path.join(os.path.abspath(os.curdir),
                                     'some/relative/path')
