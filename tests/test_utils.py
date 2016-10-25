# -*- coding: utf-8 -*-

import os


def wt_utils__init__creates_wt_yaml(sample_wt_path):
    assert os.path.isfile(os.path.join(sample_wt_path, 'wt.yaml'))


def wt_utils__init__creates_mainpage_template(sample_wt_path):
    assert os.path.isfile(
        os.path.join(sample_wt_path, 'templates', 'mainpage.html'))


def wt_utils__init__creates_content_template(sample_wt_path):
    assert os.path.isfile(
        os.path.join(sample_wt_path, 'templates', 'content.html'))


def wt_utils__init__creates_feed_template(sample_wt_path):
    assert os.path.isfile(
        os.path.join(sample_wt_path, 'templates', 'atom.xml'))
