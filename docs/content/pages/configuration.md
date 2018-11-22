---
url: /configuration/
title: Configuration
modified: 2018-11-05T10:50:00+04:00
order: 3
next:
  url: /content/
  title: Content
---

# Configuration

Configuration file `wt.yaml` is the core of your project. It contains your
project's metadata but it's not limited to - it can contain any data you like.

Your configuration file should live in the root of your project as **wt**
engine will search for content files in subdirectories.

The reason to use [yaml][yaml] for configuration is quite simple - the format
is human readable and human writable.

Here are excerpts from `wt.yaml` file you will find in your project's root
after running `wt init .` command with some comments attached.


## Generic information

```yaml
---                                 # start marker of yaml document
title: Title                        # Title of your project
subtitle: Subtitle                  # Subtitle of your project
url: "https://www.example.com"      # Url of your site
author: John Smith                  # Author

```

These properties are not required in general and you can skip them. They can be
referenced in [templates][wt-templates] for page titles or meta tags content.

In business environments it's pretty common to have a staging server to check
the project before deploying the code to production.
This means it would be nice to have a way to dynamically specify some values
in `wt.yaml` and you have it. You can reference environment variables in values
and the value will be updated accordingly.

Here is an example for `url`:

```yaml
url: "https://${DOMAIN}/"
```

and here is how you can specify the value in terminal:

```bash
$ DOMAIN=www.example.com wt develop
```

and **`config.url`** variable will have **`https://www.example.com/`**
value within your templates.


### Baseurl

```yaml
baseurl: /repository
```

Sometimes your project might be served under prefixed url (think of
[GitHub Pages for projects][ghp-for-projects]), something like
`https://username.github.io/repository`.

We have several problems here:

- there is no need to use such prefixed url while authoring,
- static assets should have proper prefixed urls on build,
- **pages** and **posts** written in `markdown` should have properly prefixed
    urls on build (including all local urls within content too).

To address these problems you should:

- provide `baseurl` setting in your `wt.yaml` configuration (like in the
    example above),
- use `baseurl(/path/to/some/assets.css)` function within your templates to
    create proper urls for static assets,
- keep urls within **page** or **post** content written in `markdown` WITHOUT
    baseurl prefix (in case you will be using provided by `wt` engine
    `markdown()` function to convert your content to html - it will update urls
    automaticcaly).

This documentation is written using `wt` and hosted using [GitHub Pages for
projects][ghp-for-projects] so you can check `docs` folder of the [wt
repository][wt] as a real-life example.


## Feed

You will probably want to have a feed for a blog or news site.
Please check default [atom.xml][atom-xml] template for a reference.

Property to control feed building is named **`build.feed`** (see below).


## Verification

```yaml
verify:
    links: true                # Turn local links verification on
```

Verification is a simple measure to prevent type errors in local urls
references. The rendered page will be parsed for urls and local urls will be
checked for existance.

In case local url is not found according to `wt.yaml` configuration:

- you will have a notice in terminal in *development mode*
  (started by **`wt develop`**)
- you will have an error and build will stop in *build mode*
  (started by **`wt build`**)


## Build

```yaml
build:
    output: output/     # Output directory for generated content
    static: true        # Enable static files to be copied to output directory
    feed: true          # Build feed
```

- **`build.output`**: specifies directory for generated content (content
  built using **`wt build`** command)
- **`build.static`**: boolean option to tell **`wt`** engine to copy
  static files to output directory
  (directory for static files sources is specified using
  **`directories.static`** value, see below)
- **`build.feed`**: boolean option to tell **`wt`** engine to build feed


## Pagination

```yaml
paginate:
    by: 10                          # Page size for posts
    orphans: 2                      # Number of orphans
    mainpage: true                  # Mainpage will contain paged content
    url: /page{page_number}.html    # Template for paginated page url
```

Pagination is meant for use by **posts** only. You can control page size,
number of orphans (to be included on previous page thus avoiding last page
having too few posts) and url for paginated pages.

Mainpage of the project (served under **`/`** url) can be included in
pagination too - you will have to set **`paginate.mainpage`** option to
**true** for proper pagination numbering in this case.

- **`paginate.by`** or **`paginate.page_size`**: page size for posts
- **`paginate.orphans`**: number of orphans to be moved to previous page if
  needed
- **`paginate.mainpage`**: boolean option saying mainpage will contain paged
  content (for proper pagination)
- **`paginate.url`**: template for paginated pages url, must have
  **`{page_number}`** placeholder, can point to **html** file or to directory
  (in the latter case target directory will have **`index.html`** with content)

For pagination example please check [objects][wt-objects] page.


## Templates

```yaml
templates:
    mainpage: mainpage.html             # Mainpage template name
    post: content.html                  # Template for posts
    page: content.html                  # Template for pages
    feed: atom.xml                      # Template for feed
```

Templates are searched in two directories - in `templates` directory within
your project's root folder and in `templates` directory of **`wt`**.

After running **`wt init .`** command you will have three templates copied from
**`wt`** sources: **atom.xml**, **content.html** and **mainpage.html**.
Base template **base.html** is not copied by default but you can grab it from
[here][base.html] or simply create it according to your needs.

Please check [Templates][wt-templates] for details.


## Directories

```yaml
directories:
    static: static/
```

- **`directories.static`**: specifies directory with assets
  (css/js/images/fonts/etc.) to be served by development server while authoring
  content and to be copied to output directory on build


## Jinja

```yaml
jinja:
    extensions:                              # List of Jinja extensions
      - jinja2.ext.i18n
      - jinja2.ext.do
      - jinja2.ext.loopcontrols
      - jinja2.ext.with_
      - jinja2.ext.autoescape
...                                          # End marker of yaml document
```

Jinja supports [extensions][jinja-extensions] so we can extend it when needed.
Besides extensions you can register custom filters or functions providing
importable **`jinja_helpers.py`** module.

Please check [Templates][wt-templates] page for information about jinja
extensions, added to templates context by `wt` engine.


## What's next


Let's continue with [Content][wt-content] topic.


[wt]: https://github.com/ysegorov/wt
[yaml]: http://yaml.org
[atom-xml]: https://github.com/ysegorov/wt/blob/master/wt/templates/atom.xml
[wt-templates]: /templates/
[wt-content]: /content/
[wt-objects]: /objects/
[base.html]: https://github.com/ysegorov/wt/blob/master/wt/templates/base.html
[jinja-extensions]: http://jinja.pocoo.org/docs/2.9/extensions/
[ghp-for-projects]: https://help.github.com/articles/user-organization-and-project-pages/#building-project-pages-sites
