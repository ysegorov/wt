# -*- coding: utf-8 -*-

import os
import time

from wt.decorators import reloadable


def test_reloadable(tmpdir):

    buf = []

    @reloadable('foo')
    def load(filename):
        buf.append(1)
        try:
            with open(filename, 'rt') as f:
                return f.read()
        except FileNotFoundError:
            return -1

    p1 = tmpdir.join('test1.txt')
    p2 = tmpdir.join('test2.txt')
    fn1 = str(p1)
    fn2 = str(p2)
    assert not os.path.isfile(fn1)
    assert not os.path.isfile(fn2)
    assert len(buf) == 0

    assert load(fn1) == -1
    assert len(buf) == 1
    assert load(fn1) == -1
    assert load(fn1) == -1
    assert len(buf) == 1

    p1.write('foo')
    assert load(fn1) == 'foo'
    assert load(fn1) == 'foo'
    assert load(fn1) == 'foo'
    assert len(buf) == 2

    time.sleep(0.1)  # intentional delay
    p1.write('bar')
    assert load(fn1) == 'bar'
    assert load(fn1) == 'bar'
    assert load(fn1) == 'bar'
    assert len(buf) == 3

    assert load(fn2) == -1
    assert len(buf) == 4

    p2.write('baz')
    assert load(fn2) == 'baz'
    assert load(fn2) == 'baz'
    assert load(fn2) == 'baz'
    assert len(buf) == 5

    time.sleep(0.1)  # intentional delay
    p1.write('foo')
    assert load(fn1) == 'foo'
    assert len(buf) == 6
