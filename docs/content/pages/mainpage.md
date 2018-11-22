---
url: /
title: Home
modified: 2017-03-28T20:31:00+04:00
template: mainpage.html
---

# Welcome

**wt** is a small library helping to generate static site or blog or whatever
else named *static*. It tries to be invisible for a blogger and have just three
command-line interface commands. At the same time it is not expected to become
a "swiss knife" - authoring still requires some user intervention to templates,
markup, styles and javascript.

This library requires **python 3** and it's recommended to use it within
**virtual environment**. See [Quick start][wt-quickstart] for introduction.

Strictly speaking there is no python coding needed to work with the library but
it's possible to extend `jinja2` templates using selfmade filters and
functions.

And please keep in mind that library offers no default `css` styling or themes.

Happy authoring!


## Features {: .fs-normal-xxl }

- [markdown][markdown] for content
- [yaml][yaml] for configuration
- [jinja2][jinja2] for templates
- [atom][atom] for feed
- two types of content - **page** and **post**
- [yaml][yaml]-formatted front matter for content metadata
- simple `HTTPServer` for development


## Documentation {: .fs-normal-xxl }

- [Quickstart][wt-quickstart]
- [Contents][wt-contents]
- [Changelog][wt-changelog]

Documentation is written using [wt][wt]. You can check documentation sources
[here][wt-docs-sources].


## Code {: .fs-normal-xxl }

The code is hosted on [GitHub][wt] and is available on [PyPi][wt-pypi]. Feel
free to open [an issue][wt-issues].


## License {: .fs-normal-xxl }

The library is licensed under [MIT license][wt-license].


[markdown]: http://daringfireball.net/projects/markdown/
[yaml]: http://yaml.org/
[jinja2]: http://jinja.pocoo.org/
[atom]: https://en.wikipedia.org/wiki/Atom_(standard)
[aiohttp]: http://aiohttp.readthedocs.io/en/stable/
[wt]: https://github.com/ysegorov/wt/
[wt-issues]: https://github.com/ysegorov/wt/issues
[wt-license]: https://github.com/ysegorov/wt/blob/master/LICENSE.txt
[wt-pypi]: https://pypi.python.org/pypi/wt/
[wt-docs-sources]: https://github.com/ysegorov/wt/tree/master/docs/
[wt-contents]: /contents/
[wt-changelog]: /changelog/
[wt-quickstart]: /quickstart/
