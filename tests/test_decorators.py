# -*- coding: utf-8 -*-

import time


def reloadable__missing_file__returns_minus_one(reloadable_factory, tmpdir):
    buf, load = reloadable_factory()
    fn = str(tmpdir.join('test1.txt'))
    assert load(fn) == -1


def reloadable__missing_file__calls_load_once(reloadable_factory, tmpdir):
    buf, load = reloadable_factory()
    fn = str(tmpdir.join('test1.txt'))
    for x in range(1, 5):
        load(fn)
    assert len(buf) == 1


def reloadable__existing_file__returns_foo(reloadable_factory, tmpdir):
    buf, load = reloadable_factory()
    p = tmpdir.join('test1.txt')
    p.write('foo')
    fn = str(p)
    for x in range(1, 5):
        assert load(fn) == 'foo'


def reloadable__existing_file__calls_load_once(reloadable_factory, tmpdir):
    buf, load = reloadable_factory()
    p = tmpdir.join('test1.txt')
    fn = str(p)
    p.write('foo')
    for x in range(1, 5):
        load(fn)
        assert len(buf) == 1


def reloadable__updating_file__returns_bar(reloadable_factory, tmpdir):
    buf, load = reloadable_factory()
    p = tmpdir.join('test1.txt')
    fn = str(p)
    p.write('foo')
    for x in range(1, 5):
        load(fn)
    time.sleep(0.1)  # intentional delay
    p.write('bar')
    for x in range(1, 5):
        assert load(fn) == 'bar'


def reloadable__updating_file__calls_load_twice(reloadable_factory, tmpdir):
    buf, load = reloadable_factory()
    p = tmpdir.join('test1.txt')
    fn = str(p)
    p.write('foo')
    for x in range(1, 5):
        load(fn)
    time.sleep(0.1)  # intentional delay
    p.write('bar')
    for x in range(1, 5):
        load(fn)
    assert len(buf) == 2
