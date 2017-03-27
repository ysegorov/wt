# -*- coding: utf-8 -*-

import time


def describe_reloadable():

    def must_properly_handle_missing_file(reloadable_factory, tmpdir):
        buf, load = reloadable_factory()
        fn = str(tmpdir.join('test1.txt'))
        for x in range(1, 5):
            assert load(fn) == -1
            assert len(buf) == 1

    def must_properly_handle_existing_file(reloadable_factory, tmpdir):
        buf, load = reloadable_factory()
        p = tmpdir.join('test1.txt')
        p.write('foo')
        fn = str(p)
        for x in range(1, 5):
            assert load(fn) == 'foo'
            assert len(buf) == 1

    def must_properly_handle_updated_file(reloadable_factory, tmpdir):
        buf, load = reloadable_factory()
        p = tmpdir.join('test1.txt')
        fn = str(p)
        p.write('foo')
        for x in range(1, 5):
            assert load(fn) == 'foo'
            assert len(buf) == 1
        time.sleep(0.1)  # intentional delay
        p.write('bar')
        for x in range(1, 5):
            assert load(fn) == 'bar'
            assert len(buf) == 2
