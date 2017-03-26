# -*- coding: utf-8 -*-

import os

from wt import cli


def describe_parse_args():

    def develop_command_defaults():
        args = cli.parse_args(['develop'])
        assert args.command == 'develop'
        assert args.port == 9000
        assert args.host == '127.0.0.1'
        assert args.config.endswith('wt.yaml')

    def develop_command_custom_config():
        args = cli.parse_args(['-c', 'conf.yaml', 'develop'])
        assert args.config.endswith('conf.yaml')
        args = cli.parse_args(['-c', '/tmp/conf.yaml', 'develop'])
        assert args.config == '/tmp/conf.yaml'

    def develop_command_custom_host_port():
        args = cli.parse_args(['develop',
                               '--host', '0.0.0.0',
                               '--port', '5000'])
        assert args.host == '0.0.0.0'
        assert args.port == 5000

    def build_command():
        args = cli.parse_args(['build'])
        assert args.command == 'build'

    def init_command_for_current_dir():
        args = cli.parse_args(['init', '.'])
        assert args.command == 'init'
        assert args.path == os.path.abspath(os.curdir)

    def init_command_for_absolute_path():
        args = cli.parse_args(['init', '/some/absolute/path'])
        assert args.path == '/some/absolute/path'

    def init_command_for_relative_path():
        args = cli.parse_args(['init', 'some/relative/path'])
        assert args.path == os.path.join(os.path.abspath(os.curdir),
                                         'some/relative/path')
