# wt - static blog generator

![Logo](misc/logo96.png)

[![Build Status](https://travis-ci.org/ysegorov/wt.svg?branch=master)](https://travis-ci.org/ysegorov/wt)


## What

Pretty small and simplified static blog generator with following features:

- [markdown][markdown] for content
- [yaml][yaml] for configuration
- [jinja2][jinja2] for templating
- [atom][atom] for feed
- [aiohttp][aiohttp] for development server
- only two types of content - **page** and **post**
- content metadata lives in configuration file, configuration file can be
  splitted into multiple nested files
- have sensible defaults for content sources
- no python coding needed to work with


## Why

While [pelican][pelican] is great and is full of features and [grow][grow] is
another one and looks very interesting in this field and there are a lot more
static site generators I wanted to create something easy to work with.

Hope someday somebody will find this library pretty usefull.


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

- [ ] documentation
- [x] ~~posts list pagination~~
- [ ] support for tags


## License

MIT


[markdown]: http://daringfireball.net/projects/markdown/
[yaml]: http://yaml.org/
[jinja2]: http://jinja.pocoo.org/
[atom]: https://en.wikipedia.org/wiki/Atom_(standard)
[aiohttp]: http://aiohttp.readthedocs.io/en/stable/
[pelican]: http://docs.getpelican.com/
[grow]: https://grow.io/
