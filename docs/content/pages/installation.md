---
url: /installation/
title: Installation
modified: 2018-11-05T09:20:00+04:00
order: 1
next:
  url: /quickstart/
  title: Quickstart
---

# Installation

`wt` is written in [Python][python] and supports Python 3.5+.


## Create virtual environment

It is recommended to use [virtual environment][python-venv] while working with
`wt`. You can create it using following commands:

```shell

$ pwd
/home/user/work
$ mkdir blog && cd blog
mkdir: created directory 'blog'
$ python3 -m venv env

```

and activate it:

```shell

$ source env/bin/activate

```


## Installation from PyPI

`wt` packages are published on the [Python Package Index][pypi-wt]. Preferred
tool to install it is **pip**, which is provided with all modern versions of
Python.

On Linux or MacOS please open your terminal and run the following command:

```shell

$ pip install -U wt

```

## Installation from source

You can install `wt` directly from sources. This can be done by cloning `wt`
[github repository][github-wt] and installing from local clone or directly
via **git**:

```shell

$ git clone https://github.com/ysegorov/wt
$ cd wt
$ pip install .

```

```shell

$ pip install git+https://github.com/ysegorov/wt

```

## What's next

Let's continue with [Getting Started][wt-quickstart] topic.


[python]: https://www.python.org
[python-venv]: https://docs.python.org/3/library/venv.html
[pypi-wt]: https://pypi.org/project/wt/
[github-wt]: https://github.com/ysegorov/wt
[wt-quickstart]: /quickstart/
