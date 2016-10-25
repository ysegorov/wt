# -*- coding: utf-8 -*-

import os
import datetime
import itertools
import logging
from collections import OrderedDict
from pathlib import Path
from shutil import copytree, rmtree

import jinja2
import markdown
import yaml
from cached_property import cached_property

from .base import Config, Page, Post
from .exceptions import UrlNotFoundError
from .paginator import Paginator


class WT(object):

    def __init__(self, filename):
        self.config_filename = filename
        self.workdir = os.path.dirname(filename)
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
        else:
            self.logger.warn('Missing config file "%s"', filename)

        self.conf = Config(conf or {})

    @cached_property
    def static_root(self):
        static_root = self.conf.path('directories.static', 'static')
        return os.path.join(self.workdir, static_root)

    @cached_property
    def with_feed(self):
        return self.conf.path('build.feed', True)

    @cached_property
    def pages(self):
        pages = self.conf.pages or []
        return {x['url']: Page.from_dict(self.workdir, x) for x in pages}

    @cached_property
    def posts(self):
        posts = self.conf.posts or []
        posts.sort(key=lambda x: x['modified'], reverse=True)
        dst = OrderedDict()
        _prev = None
        for idx, post in enumerate(posts):
            p = Post.from_dict(self.workdir, post)
            if idx > 0:
                p.next = _prev
                _prev.prev = p
            dst[p['url']] = _prev = p
        return dst

    @cached_property
    def env(self):
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
        return env

    def render_html(self, template, **context):
        tmpl = self.env.get_template(template)
        return tmpl.render(**context)

    def render(self, path, headers=None):
        headers = headers or {}
        host = headers.get('Host')
        now = datetime.datetime.utcnow()
        if path.endswith('atom.xml') and self.with_feed:
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

        tmpl = self.conf.path('templates.mainpage', 'mainpage.html')
        posts = list(self.posts.values())
        paginator = Paginator(posts, path, **self.conf.path('paginate', {}))
        if path == '/' or path in paginator.pages:
            return self.render_html(tmpl,
                                    config=self.conf,
                                    paginator=paginator,
                                    posts=posts,
                                    pages=self.pages,
                                    host=host,
                                    now=now)

        raise UrlNotFoundError

    @cached_property
    def output_path(self):
        output = Path(self.conf.path('build.output', 'output'))
        if not output.is_absolute():
            output = Path(self.workdir).joinpath(output)
        return output.expanduser()

    def build(self):
        build_static = bool(self.conf.path('build.static', False))
        output = self.output_path
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
        paginator = Paginator(
            list(self.posts.values()), '/', **self.conf.path('paginate', {}))
        pages = [x for x in paginator.pages.keys() if x != '/']
        for path in itertools.chain(mainpage,
                                    feed,
                                    pages,
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
