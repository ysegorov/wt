# -*- coding: utf-8 -*-

import logging
from pathlib import Path
from shutil import copyfile

from .decorators import reloadable
from .engine import WT


FOO_CONTENT = """
---
url: /foo/
title: Foo page title
modified: 2016-09-18T11:31:00+04:00
---
# Foo page title
[bar](/bar/)"""

BAR_CONTENT = """
---
url: /bar/
title: Bar page title
modified: 2016-09-18T20:10:00+04:00
---
# Bar post title
[baz](/baz/)"""

BAZ_CONTENT = """
---
url: /baz/
title: Baz page title
modified: 2016-09-20T20:10:00+04:00
---
# Baz post title
[foo](/foo/)"""


@reloadable('(re)loading configuration...')
def engine(fn):  # pragma: no cover
    return WT(fn)


def build(fn):  # pragma: no cover
    b = WT(fn, is_prod=True)
    try:
        b.build()
    except Exception as exc:
        logger = logging.getLogger('wt.build')
        logger.error('Error while building', exc_info=exc)
        return 1
    else:
        return 0


def init(path):
    src = Path(__file__).parent
    dst = Path(path)

    logger = logging.getLogger('wt.init')

    to_copy = (
        (['templates', 'wt.yaml'], ['wt.yaml']),
        (['templates', 'atom.xml'], ['templates', 'atom.xml']),
        (['templates', 'content.html'], ['templates', 'content.html']),
        (['templates', 'mainpage.html'], ['templates', 'mainpage.html']),
    )

    for from_, to_ in to_copy:
        left = src.joinpath(*from_)
        right = dst.joinpath(*to_)
        if not left.exists():  # pragma: no cover
            logger.warn('[!] missing file "%s", skipping', str(left))
            continue
        if right.exists():  # pragma: no cover
            logger.warn('[!] target file "%s" exists, skipping', str(right))
            continue
        if not right.parent.exists():
            right.parent.mkdir(parents=True)
        copyfile(str(left), str(right))
        logger.info('[+] "%s" created', str(right))

    to_create = (
        (['content', 'pages', 'foo.md'], FOO_CONTENT),
        (['content', 'posts', 'bar.md'], BAR_CONTENT),
        (['content', 'posts', 'baz.md'], BAZ_CONTENT),
        (['static', 'css', 'style.css'], '/*styles*/\nbody {color: coral}'),
    )
    for parts, text in to_create:
        p = dst.joinpath(*parts)
        if p.exists():  # pragma: no cover
            logger.warn('[!] target file "%s" exists, skipping', str(p))
            continue
        if not p.parent.exists():
            p.parent.mkdir(parents=True)
        p.write_text(text, encoding='utf-8')
        logger.info('[+] "%s" created', str(p))

    logger.info('[+] done')

    return 0
