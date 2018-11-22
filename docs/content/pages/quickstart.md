---
url: /quickstart/
title: Getting Started
modified: 2018-11-05T09:50:00+04:00
order: 2
next:
  url: /configuration/
  title: Configuration
---

# Getting Started

## Bootstrap your project

Once you have `wt` [installed][wt-installation] you can quickly bootstrap your
project by running the following command in the terminal:

```shell

$ wt init .

```

You will have directory tree like this one (excluding **virtual environment**
directory):

```shell

$ tree -I env
.
├── content
│   ├── pages
│   │   └── foo.md
│   └── posts
│       ├── bar.md
│       └── baz.md
├── static
│   └── css
│       └── style.css
│   └── img
│       └── logo96.png
├── templates
│   ├── atom.xml
│   ├── content.html
│   └── mainpage.html
└── wt.yaml

7 directories, 9 files

```

## Start development server

You can start simple `HTTPServer` server suitable for development by running
the following command in the terminal:

```shell

$ wt develop
[D 2017-03-31 19:02:55,825 wt.server] Server started at 127.0.0.1:9000...

```

and navigate to your [newly created project][devserver] in browser.
You will see something like this:

[![mainpage after init](/img/quickstart-mainpage.jpg)][quickstart-mainpage]

For demo purposes there are [foo][foo], [bar][bar] and [baz][baz] pages
available.
To stop development server just hit `Ctrl-C` in the terminal.

That's it - you can start authoring your content straight away.


## What's next

Let's continue with [Configuration][wt-configuration] topic.

Navigate to [Command-line interface][wt-cli] to become familiar with available
commands.

[devserver]: http://127.0.0.1:9000
[foo]: http://127.0.0.1:9000/foo/
[bar]: http://127.0.0.1:9000/bar/
[baz]: http://127.0.0.1:9000/baz/
[quickstart-mainpage]: /img/quickstart-mainpage.jpg
[wt-installation]: /installation/
[wt-cli]: /cli/
[wt-configuration]: /configuration/
