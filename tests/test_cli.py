# -*- coding: utf-8 -*-

import os

from wt import cli


def develop_cmd__command__equals_develop():
    args = cli.parse_args(['develop'])
    assert args.command == 'develop'


def develop_cmd__default_port__equals_9000():
    args = cli.parse_args(['develop'])
    assert args.port == 9000


def develop_cmd__default_host__equals_127_0_0_1():
    args = cli.parse_args(['develop'])
    assert args.host == '127.0.0.1'


def develop_cmd__default_config__ends_with_wt_yaml():
    args = cli.parse_args(['develop'])
    assert args.config.endswith('wt.yaml')


def develop_cmd__config_with_relpath___ends_with_relpath():
    args = cli.parse_args(['-c', 'conf.yaml', 'develop'])
    assert args.config.endswith('conf.yaml')


def develop_cmd__config_with_abspath__is_the_same():
    args = cli.parse_args(['-c', '/tmp/conf.yaml', 'develop'])
    assert args.config == '/tmp/conf.yaml'


def develop_cmd__custom_host__equals_0_0_0_0():
    args = cli.parse_args(['develop', '--host', '0.0.0.0'])
    assert args.host == '0.0.0.0'


def develop_cmd__custom_port__equals_5000():
    args = cli.parse_args(['develop', '--port', '5000'])
    assert args.port == 5000


def build_cmd__command__equals_build():
    args = cli.parse_args(['build'])
    assert args.command == 'build'


def init_cmd__command__equals_init():
    args = cli.parse_args(['init', '.'])
    assert args.command == 'init'


def init_cmd__dot_path__equals_current_dir():
    args = cli.parse_args(['init', '.'])
    assert args.path == os.path.abspath(os.curdir)


def init_cmd__abs_path__is_the_same():
    args = cli.parse_args(['init', '/some/absolute/path'])
    assert args.path == '/some/absolute/path'


def init_cmd__rel_path__resolves_from_current_dir():
    args = cli.parse_args(['init', 'some/relative/path'])
    assert args.path == os.path.join(os.path.abspath(os.curdir),
                                     'some/relative/path')
