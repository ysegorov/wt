**This project is archived.**

# wt - static blog generator

![Logo](misc/logo96.png)

[![Current Version](https://img.shields.io/pypi/v/wt.svg?style=flat-square)](https://pypi.org/projects/wt/)
[![Build Status](https://img.shields.io/travis/ysegorov/wt/master.svg?style=flat-square)](https://travis-ci.org/ysegorov/wt)


## What

Yet another static blog generator with following features:

- [markdown][markdown] for content
- [yaml][yaml] for configuration
- [jinja2][jinja2] for templates
- [atom][atom] for feed
- two types of content - **page** and **post**
- [yaml][yaml]-formatted front matter for content metadata
- simple `HTTPServer` for development


## Why

It was curiosity - "how would I do it?" and good intentions - "let's create
something easy to work with".


## Documentation

`wt` documentation is not available online but you can check
`docs/content/pages/` folder for it.


## How

### Requirements

The only hard dependency is **python3**.

### Installation

```shell
$ mkdir blog && cd blog
$ mkdir env && virtualenv -p python3 env && source ./env/bin/activate
$ pip install wt

```

### Bootstrapping

```shell
$ wt init .

```

### Configuration

Your blog must have configuration file written in [yaml][yaml] and named
**wt.yaml** (name can be changed).

### Usage

While writing content (ie in development mode):

```shell
$ wt develop

```

This command will start the development server listening at 127.0.0.1:9000.

When content is ready you will need to build it:

```shell
$ wt build

```


## Roadmap

- [x] ~~documentation~~
- [x] ~~posts list pagination~~
- [ ] support for tags


## License

MIT


[markdown]: http://daringfireball.net/projects/markdown/
[yaml]: http://yaml.org/
[front-matter]: https://jekyllrb.com/docs/front-matter/
[jinja2]: http://jinja.pocoo.org/
[atom]: https://en.wikipedia.org/wiki/Atom_(standard)
[wt-docs]: https://ysegorov.github.io/wt/
