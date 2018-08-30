# -*- coding: utf-8 -*-

import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

from .html import parse_link, is_local_link


class BaseurlTreeprocessor(Treeprocessor):

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def run(self, root):
        if not self.baseurl:
            return
        attrs = ['href', 'src']
        for attr in attrs:
            for tag in root.findall('.//*[@%s]' % attr):
                link = tag.get(attr)
                parsed = parse_link(link)
                if is_local_link(parsed):
                    tag.set(attr, '{}{}'.format(self.baseurl, link))


class BaseurlExtension(Extension):

    def __init__(self, *args, **kwargs):
        self.config = {
            'baseurl': ['', 'baseurl wt configuration value']
        }
        super(BaseurlExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        proc = BaseurlTreeprocessor(self.getConfig('baseurl'))
        md.treeprocessors.add('baseurl', proc, '_end')


def make_jinja_filter(baseurl, extensions):
    assert isinstance(extensions, list)

    extensions.append(BaseurlExtension(baseurl=baseurl))

    def md(text):
        return markdown.markdown(text,
                                 extensions=extensions,
                                 output_format='html5')

    return md
