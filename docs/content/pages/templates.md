---
url: /templates/
title: Templates
modified: 2018-11-05T12:50:00+04:00
order: 5
next:
  url: /objects/
  title: Objects
---

# Templates

Templates are used by [jinja][jinja] to render your content and produce html
files ready to be served by [nginx][nginx], [apache][apache] or another
web-server of your choice.

Templates are searched in two directories - in
`templates` directory within your project's root directory and in `templates`
directory of **`wt`** installation as fallback.


## Configuration

You can [configure][wt-configuration-templates] templates in `wt.yaml` for:

- **mainpage** - this is a root page of your project; this template is used
    to render your project's main page and paginated **posts** pages according
    to your [configuration][wt-configuration-pagination] (see below for
    real-life example); defaults to `mainpage.html`,
- **post** - template to render **post** content from `content/posts/`
    directory of the project; defaults to `post.html`,
- **page** - template to render regular **page** content from `content/pages/`
    directory of the project; defaults to `page.html`,
- **feed** - template to render **atom feed** if configured; defaults to
    `atom.xml`.

Keep in mind that you can use individual template for any **page** or **post**
by specifying value for `template` parameter in **page/post** front matter
(please check [Content][wt-content] topic for examples).


## Jinja environment

[jinja][jinja] allows us to extend it's [environment][jinja-env].

`wt` engine will make two functions available globally within templates:

- `markdown()` function which should be used to convert **page** or **post**
    content written in `markdown` format to html,
- `baseurl()` function which should be used to make proper urls to static
    assets in case your project will be hosted under prefixed url (see
    [configuration][wt-configuration-baseurl] page for configuration details).

Besides, you can extend jinja environment by making
`jinja_helpers.py` module in your project's root directory
(actually, it simply must be importable by **python**).

Suppose you want to provide `custom_markdown` filter within jinja templates. In
this case the module might look something like this:

```python
# -*- coding: utf-8 -*-

import markdown
from markdown.extensions.toc import TocExtension
from markdown.extensions.extra import ExtraExtension

from wt.jinja import filters


class CustomMD(object):
    filter_name = 'custom_markdown'

    def __init__(self):
        extensions = [ExtraExtension(), TocExtension(permalink=False)]
        self.md = markdown.Markdown(extensions=extensions,
                                    output_format='html5')

    def __call__(self, text):
        return self.md.reset().convert(text)


filters.add(CustomMD())
```

And you can use this filter in templates as:

```jinja

<div>{{ content.text|custom_markdown }}</div>

```


## Template context

The most important thing about templates is context used to render content.

Here is an overview of context variables available within templates.

### Mainpage template

- **config** - `Config` object holding configuration loaded from **`wt.yaml`**
- **posts** - ordered list of `Content` objects loaded from
    `content/posts/` directory (list will be ordered by `modified` property
    value in reversed order)
- **pages** - unordered list of `Content` objects loaded from
    `content/pages/` directory
- **now** - current timestamp in UTC (instance of `datetime.datetime`)
- **is_prod** - boolean value indicating *build* (**`True`**) or
  *development* (**`False`**) mode (mode corresponds to running **`wt build`**
  or **`wt develop`** commands in terminal)
- **host** - value of **`Host`** request header in *development* mode
- **paginator** - `Paginator` object configured according to current url
    and [configuration][wt-configuration-pagination]


### Post template

- **config** - `Config` object holding configuration loaded from **`wt.yaml`**
- **posts** - ordered list of `Content` objects loaded from
    `content/posts/` directory (list will be ordered by `modified` property
    value in reversed order)
- **pages** - unordered list of `Content` objects loaded from
    `content/pages/` directory
- **now** - current timestamp in UTC (instance of `datetime.datetime`)
- **is_prod** - boolean value indicating *build* (**`True`**) or
  *development* (**`False`**) mode (mode corresponds to running **`wt build`**
  or **`wt develop`** commands in terminal)
- **host** - value of **`Host`** request header in *development* mode
- **content** - `Content` object holding front matter properties and **post**
    content, available under `text` attribute of the object


### Page template

- **config** - `Config` object holding configuration loaded from **`wt.yaml`**
- **posts** - ordered list of `Content` objects loaded from
    `content/posts/` directory (list will be ordered by `modified` property
    value in reversed order)
- **pages** - unordered list of `Content` objects loaded from
    `content/pages/` directory
- **now** - current timestamp in UTC (instance of `datetime.datetime`)
- **is_prod** - boolean value indicating *build* (**`True`**) or
  *development* (**`False`**) mode (mode corresponds to running **`wt build`**
  or **`wt develop`** commands in terminal)
- **host** - value of **`Host`** request header in *development* mode
- **content** - `Content` object holding front matter properties and **page**
    content, available under `text` attribute of the object


### Feed template

- **config** - `Config` object holding configuration loaded from **`wt.yaml`**
- **posts** - ordered list of `Content` objects loaded from
    `content/posts/` directory (list will be ordered by `modified` property
    value in reversed order)
- **pages** - unordered list of `Content` objects loaded from
    `content/pages/` directory
- **now** - current timestamp in UTC (instance of `datetime.datetime`)
- **is_prod** - boolean value indicating *build* (**`True`**) or
  *development* (**`False`**) mode (mode corresponds to running **`wt build`**
  or **`wt develop`** commands in terminal)
- **host** - value of **`Host`** request header in *development* mode


## What's next

Let's continue with [Objects][wt-objects] topic.


[jinja]: http://jinja.pocoo.org/
[jinja-env]: http://jinja.pocoo.org/docs/api/
[nginx]: https://nginx.org
[apache]: https://apache.org
[wt-templates]: https://github.com/ysegorov/wt/tree/master/wt/templates
[wt-configuration-templates]: /configuration/#templates
[wt-configuration-pagination]: /configuration/#pagination
[wt-configuration-baseurl]: /configuration/#baseurl
[wt-content]: /content/
[wt-objects]: /objects/
