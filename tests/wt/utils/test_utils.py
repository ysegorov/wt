# -*- coding: utf-8 -*-

import os


def describe_init():

    def must_create_wt_yaml(wt_inited_path):
        assert os.path.isfile(os.path.join(wt_inited_path, 'wt.yaml'))

    def must_create_templates(wt_inited_path):
        templates = ['mainpage.html', 'content.html', 'atom.xml']

        for filename in templates:
            assert os.path.isfile(
                os.path.join(wt_inited_path, 'templates', filename))
