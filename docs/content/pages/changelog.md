---
url: /changelog/
title: Changelog
modified: 2018-11-01T08:25:00+04:00
order: 8
---

# Changelog


## 2.0.0 (in development)

### Breaking changes

- dropped support for configurable `python-markdown` extensions (#32)
- switched from `{{ text|markdown }}` filter to `{{ markdown(text) }}` function
  in `jinja` templates (#37)
- dropped support for passing `WT` engine instance to rendering context (#40)
- dropped support for `feed_domain` rendering context variable in favour of
  `host` variable (#41)

### Changes

- pages without or empty `url` definition in front matter are skipped (#34)
- slightly optimized `WT.render` method (build `posts` list only once per
    requested url or per url to be built)


## 1.0.0 (2018-09-04)

### Breaking changes

- dropped support for hardcoded posts/pages configuration in `wt.yaml`
  in favor of post/page front matter (#31)

### Features added

- added support for baseurl (#28)
- added support for yaml-formatted content front matter (#30)


## 0.5.2 (2018-08-02)

### Changes

- package rebuild using latest wheel and twine to use readme in markdown
  format on pypi.org


## 0.5.1 (2018-08-02)

### Changes

- minor fix for pypi targeted readme in markdown format


## 0.5.0 (2018-08-02)

### Features added

- allow class-based filters and function for jinja customization (#27)
- wt documentation is [online](https://ysegorov.github.io/wt-docs/) (#1)

### Changes

- switch to `http.server.HTTPServer` as a development http server (#29)


## 0.4.0 (2017-03-28)

### Breaking changes

- `wt.base` module refactored, module api breakage (#25)

### Features added

- yaml configuration can be splitted into multiple files (#23)
- wt logo

### Changes

- tests rewritten using pytest-describe plugin (#24)


## 0.3.1 (2017-03-21)

### Changes

- minor fix for pypi targeted readme translation from md to rst
  (`pypandoc` was not installed in virtualenv during build)


## 0.3.0 (2017-03-21)

### Features added

- added wt instance to rendering context (#21)
- allow jinja filters and globals to be extended using `jinja_helpers`
  module (#20)
- page and post configuration can have custom template for rendering (#18)
- wt.yaml values can have placeholders like `${URL}` to be replaced by
  environment variables, missed variables will be skipped (#17)
- added local links validation (#4, #16, #22)
- added option to skip feed rendering (#7)
- added pagination for posts (mainpage) list (#2)

### Changes

- render mainpage only once in case mainpage content is in pages (#8)


## 0.2.0 (2016-10-05)

### Features added

- added `wt init` command to bootstrap project (#6)
- use travis ci for testing (#5)


## 0.1.0 (2016-09-22)

- initial release
