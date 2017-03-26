# -*- coding: utf-8 -*-

import pytest

from wt.utils import init


@pytest.fixture(scope='function')
def wt_inited_path(tmpdir):
    p = str(tmpdir)
    init(p)
    return p
