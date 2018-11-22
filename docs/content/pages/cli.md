---
url: /cli/
title: Command-line Interface
modified: 2017-04-01T13:50:00+04:00
order: 7
next:
  url: /changelog/
  title: Changelog
---

# Command-line Interface

Command-line interface of the library is simple and contains just three
commands:

- **init** - to initialize your project,
- **develop** - for authoring (*development* mode),
- **build** - to build your project (*production* mode).

You can get help by running **`wt -h`** in terminal:

```bash

$ wt -h
usage: wt [-h] [-c wt.yaml] {init,develop,build} ...

Command-line interface to static site generator

optional arguments:
  -h, --help            show this help message and exit
  -c wt.yaml, --conf wt.yaml
                        configuration file (defaults to wt.yaml in current
                        directory)

commands:
  {init,develop,build}
    init                bootstrap project structure
    develop             start simple http server for development
    build               build site

```


## wt init

**`wt init`** command requires one positional argument - `path` to folder to
bootstrap project in:

```bash

$ wt init -h
usage: wt init [-h] path

positional arguments:
  path        path to folder to bootstrap in

optional arguments:
  -h, --help  show this help message and exit

```


## wt develop

**`wt develop`** command has two optional parameters
**`--host`** and **`--port`**:

```bash

$ wt develop -h
usage: wt develop [-h] [--host HOST] [--port PORT]

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  address to run server at (defaults to 127.0.0.1)
  --port PORT  port to bind server to (defaults to 9000)

```

Development server will serve pages generating response on the fly (without
writing any html file). Internally before serving the request it will check if
your project's [configuration][configuration] file has been changed and will
automatically reload it if needed.

Static files are served by development server too.


## wt build

**`wt build`** command doesn't have any optional arguments:

```bash

$ wt build -h
usage: wt build [-h]

optional arguments:
  -h, --help  show this help message and exit

```


## What's next

That's it for command-line interface and for `wt`.

Happy authoring!


[configuration]: /configuration/
