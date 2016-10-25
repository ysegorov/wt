# -*- coding: utf-8 -*-

import os

import pytest


def object_dict__getattr__works(object_dict):
    assert object_dict.foo == object_dict['foo']


def object_dict__setattr__works(object_dict):
    object_dict.bar = 'bar'
    assert object_dict.bar == 'bar' and object_dict.bar == object_dict['bar']


def object_dict__path__works(object_dict):
    assert object_dict.path('foo') == object_dict['foo']


def nested_object_dict__path__works(nested_object_dict):
    assert nested_object_dict.path('foo.bar.baz') == 12


def nested_object_dict__path_with_missed_part__works(nested_object_dict):
    assert nested_object_dict.path('foo.baz.zy') is None


def nested_object_dict__path_with_default_value__works(nested_object_dict):
    assert nested_object_dict.path('foo.bar.zy', 'missed') == 'missed'


def nested_object_dict__path_returns_object_dict__works(nested_object_dict):
    assert type(nested_object_dict.path('foo.bar')) is type(nested_object_dict)


def nested_object_dict__bad_path__raises(nested_object_dict):
    with pytest.raises(ValueError):
        nested_object_dict.path('foo.bar.baz.zap')


def ordered_object_dict__keys_order__ok(ordered_object_dict):
    assert list(ordered_object_dict.keys()) == ['foo', 'bar', 'baz']


def ordered_object_dict__values_order__ok(ordered_object_dict):
    assert list(ordered_object_dict.values()) == [12, 'yes', True]


def ordered_object_dict__path__works(ordered_object_dict):
    assert ordered_object_dict.path('bar') == 'yes'


def ordered_object_dict__path_with_missed_part__works(ordered_object_dict):
    assert ordered_object_dict.path('zap.zy') is None


def ordered_object_dict__path_with_default_value__works(ordered_object_dict):
    assert ordered_object_dict.path('zap.zy', 'missed') == 'missed'


def ordered_object_dict__bad_path__raises(ordered_object_dict):
    with pytest.raises(ValueError):
        ordered_object_dict.path('foo.bar')


def content__src_attr_expands_to_abspath__ok(content):
    assert os.path.isabs(content.src)


def content_without_src__works(content_without_src):
    assert content_without_src.src is None


def content__text_attr_loaded_from_file__ok(content):
    assert content.text == 'bar'


def content_without_src__text_attr__is_empty(content_without_src):
    assert content_without_src.text == ''


def post__text_attr_loaded_from_file__ok(post):
    assert post.text == 'ipsum'


def page__text_attr_loaded_from_file__ok(page):
    assert page.text == 'lorem'
