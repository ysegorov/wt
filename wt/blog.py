# -*- coding: utf-8 -*-

import datetime
import itertools
import logging
import os
from collections import OrderedDict
from pathlib import Path
from shutil import copytree, copyfile, rmtree

import jinja2
import markdown
import yaml

from .decorators import reloadable


logger = logging.getLogger(__name__)


@reloadable('(re)loading configuration...')
def blog(fn):
    return Blog(fn)


def build(fn):
    b = blog(fn)
    b.build()
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

    for left, right in to_copy:
        l = src.joinpath(*left)
        r = dst.joinpath(*right)
        if not l.exists():  # pragma: no cover
            logger.warn('[!] missing file "%s", skipping', str(l))
            continue
        if r.exists():  # pragma: no cover
            logger.warn('[!] target file "%s" exists, skipping', str(r))
            continue
        if not r.parent.exists():
            r.parent.mkdir(parents=True)
        copyfile(str(l), str(r))
        logger.info('[+] "%s" created', str(r))

    to_create = (
        (['content', 'pages', 'foo.md'], '# Foo page'),
        (['content', 'posts', 'bar.md'], '# Bar post'),
        (['static', 'css', 'style.css'], 'body {color: coral}'),
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


class Config(dict):

    def __getattr__(self, name):
        return self.get(name)

    def path(self, parts, dflt=None):
        parts = parts.split('.')
        src = self
        for idx, p in enumerate(parts[:-1]):
            src = src.get(p)
            if src is None:
                break
            if not isinstance(src, dict):
                msg = ('Expecting config to have value for "%s"'
                       ' but "%s" found at "%s"'
                       % ('.'.join(parts),
                          str(src),
                          '.'.join(parts[:idx + 1])))
                raise ValueError(msg)
        v = src and src.get(parts[-1], dflt)
        return dflt if v is None else v


class Content(dict):
    content_dirname = 'content'
    data_dirname = None

    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        self[name] = value

    @classmethod
    def from_dict(cls, workdir, page_data):
        p = cls(page_data)
        if not os.path.isabs(p.src):
            p.src = os.path.join(workdir,
                                 cls.content_dirname,
                                 cls.data_dirname or '',
                                 p.src)
        return p

    @property
    def text(self):
        t = ''
        if os.path.isfile(self.src):
            with open(self.src, 'rt', encoding='utf-8') as f:
                t = f.read()
        else:
            logger.warn('  ! missing content file "%s"', self.src)
        return t


class Page(Content):
    data_dirname = 'pages'


class Post(Content):
    data_dirname = 'posts'


class Blog(object):

    class NotFound(Exception):
        pass

    class PaginateSlugError(Exception):
        pass

    def __init__(self, filename):
        self.workdir = os.path.dirname(filename)
        self._jinja_env = self._pages = self._posts = self._pagination = None
        self.logger = logging.getLogger('wt.blog')

        conf = None
        if os.path.isfile(filename):
            with open(filename, encoding='utf-8') as f:
                try:
                    conf = yaml.load(f)
                    assert isinstance(conf, dict)
                except (yaml.YAMLError, AssertionError):
                    conf = {}
                    self.logger.error('Error parsing yaml', exc_info=True)

        self.conf = Config(conf or {})

    @property
    def static_root(self):
        static_root = self.conf.path('directories.static', 'static')
        return os.path.join(self.workdir, static_root)

    @property
    def with_feed(self):
        return self.conf.path('build.feed', True)

    @property
    def pages(self):
        if self._pages is None:
            pages = self.conf.pages or []
            pages = {x['url']: Page.from_dict(self.workdir, x) for x in pages}
            self._pages = pages
        return self._pages

    @property
    def posts(self):
        if self._posts is None:
            posts = self.conf.posts or []
            posts.sort(key=lambda x: x['modified'], reverse=True)
            self._posts = dst = OrderedDict()
            _prev = None
            for idx, post in enumerate(posts):
                p = Post.from_dict(self.workdir, post)
                if idx > 0:
                    p.next = _prev
                    _prev.prev = p
                dst[p['url']] = _prev = p
        return self._posts

    @property
    def env(self):
        if self._jinja_env is None:
            loader = jinja2.ChoiceLoader([
                jinja2.FileSystemLoader(
                    os.path.join(self.workdir, 'templates')),
                jinja2.FileSystemLoader(
                    os.path.join(os.path.dirname(__file__), 'templates'))
            ])
            ext = self.conf.jinja_extensions or []
            if 'jinja2.ext.autoescape' not in ext:
                ext.append('jinja2.ext.autoescape')
            env = jinja2.Environment(loader=loader, extensions=ext)

            md_exts = self.conf.markdown_extensions or []

            def md(text):
                return markdown.markdown(text,
                                         extensions=md_exts,
                                         output_format='html5')

            env.filters['markdown'] = md
            self._jinja_env = env

        return self._jinja_env

    @property
    def pagination(self):
        if self._pagination is None:
            self._pagination = dst = OrderedDict()
            paginate_by = self.conf.path('paginate.by')
            if paginate_by:
                orphans = self.conf.path('paginate.orphans')
                paginate_slug = self.conf.path('paginate.slug',
                                               '/page{page_number}.html')
                cnt = len(self.posts)
                num_pages, rem = divmod(cnt, paginate_by)
                if rem > 0:
                    if (orphans and rem > orphans) or not orphans:
                        num_pages += 1
                if num_pages > 1:
                    dst['/'] = 1
                    for x in range(2, num_pages + 1):
                        try:
                            dst[paginate_slug.format(page_number=x)] = x
                        except KeyError as exc:
                            msg = ('Bad paginate slug pattern "%s"'
                                   ' in config (it must have only '
                                   '"{page_number}" placeholder)')
                            err = self.PaginateSlugError(msg % paginate_slug)
                            raise err from exc
        return self._pagination

    def render_html(self, template, **context):
        tmpl = self.env.get_template(template)
        return tmpl.render(**context)

    def render(self, path, headers=None):
        headers = headers or {}
        host = headers.get('Host')
        now = datetime.datetime.utcnow()
        if path == '/' or path in self.pagination:
            return self.render_mainpage(path=path, host=host, now=now)
        elif path.endswith('atom.xml') and self.with_feed:
            tmpl = self.conf.path('templates.feed', 'atom.xml')
            return self.render_html(tmpl, config=self.conf,
                                    host=host,
                                    now=now,
                                    posts=self.posts.values(),
                                    pages=self.pages.values())
        elif path in self.pages:
            tmpl = self.conf.path('templates.page', 'page.html')
            return self.render_html(tmpl,
                                    content=self.pages[path],
                                    config=self.conf)
        elif path in self.posts:
            tmpl = self.conf.path('templates.post', 'post.html')
            return self.render_html(tmpl,
                                    content=self.posts[path],
                                    config=self.conf)

        raise self.NotFound

    def build(self):
        output = Path(self.conf.path('build.output', 'output'))
        build_static = bool(self.conf.path('build.static', False))
        if not output.is_absolute():
            output = Path(self.workdir).joinpath(output)
        output = output.expanduser()
        self.logger.info('Building blog to %s directory', str(output))
        if output.exists():
            self.logger.info('  * output directory exists, cleaning')
            rmtree(str(output))
        if build_static:
            self.logger.info('  + copying static files')
            copytree(self.static_root, str(output))
        else:
            output.mkdir(parents=True)
        feed = ['/atom.xml'] if self.with_feed else []
        mainpage = ['/'] if '/' not in self.pages else []
        pagination = [x for x in self.pagination.keys() if x != '/']
        for path in itertools.chain(mainpage,
                                    feed,
                                    pagination,
                                    self.pages.keys(),
                                    self.posts.keys()):
            self.logger.info('  + building path "%s"', path)
            html = self.render(path)
            if path.endswith('/'):
                path += 'index.html'
            target = output.joinpath(path.lstrip('/'))
            parent = target.parent
            parent.mkdir(parents=True, exist_ok=True)
            target.write_text(html, encoding='utf-8')
        self.logger.info('done')

    def render_mainpage(self, **ctx):
        path = ctx.pop('path')
        tmpl = self.conf.path('templates.mainpage', 'mainpage.html')
        posts = list(self.posts.values())
        num_posts = len(posts)
        pager = current_page = prev_page = next_page = None
        paginate_by = self.conf.path('paginate.by')
        if paginate_by is not None:
            orphans = self.conf.path('paginate.orphans')
            pager = OrderedDict((y, x) for x, y in self.pagination.items())
            current_page = self.pagination.get(path, 1)
            _prev_num, _next_num = current_page + 1, current_page - 1
            if _prev_num in pager:
                prev_page = pager[_prev_num]
            if _next_num in pager:
                next_page = pager[_next_num]
            first = (current_page - 1) * paginate_by
            last = first + paginate_by
            if orphans and last < num_posts and last + orphans >= num_posts:
                last += orphans
                prev_page = None
            posts = posts[first:last]
        return self.render_html(tmpl,
                                config=self.conf,
                                paginate_by=paginate_by,
                                pager=pager,
                                current_page=current_page,
                                next_page=next_page,
                                prev_page=prev_page,
                                posts=posts,
                                pages=self.pages,
                                **ctx)
