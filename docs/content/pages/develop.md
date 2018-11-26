---
url: /develop/
title: wt development
modified: 2018-11-26T08:10:00Z
---

# wt development

`wt` sources are available on [GitHub][wt]. You can raise issue or feature
request in the [issue tracker][wt-issues].

The recommended way to submit code to `wt` or to update `wt` docs is to fork
the repository on GitHub, commit the changes and submit a pull request.

You can use [wt-dev][wt-dev] repository aimed to ease the development process.


## Prerequisites

You must have **python3** (for `wt`) and **nodejs** alongside with **npm** or
**yarn** (for `wt` docs) installed locally for development.


## Hack wt

These are the basic steps needed to hack `wt`:

1. Create GitHub account (in case you don't have it yet).

2. Fork [wt][wt] repository using GitHub interface.

3. Clone [wt-dev][wt-dev] repository locally:

        $ cd ~/dev
        $ git clone https://github.com/ysegorov/wt-dev.git
        $ cd wt-dev

4. Create and activate virtual environment:

        $ python3 -m venv env
        $ source env/bin/activate

5. Install `wt` from forked repository (replace `USERNAME` with your GitHub
   account username) in *editable* mode:

        $ pip install -e git+https://github.com/USERNAME/wt.git#egg=wt[dev]

6. Change your directory to `wt` sources, get familiar with project structure
   and hack:

        $ cd env/src/wt/

7. Test your changes and add missing tests if needed:

        $ pytest

8. Commit your changes providing useful commit message:

        $ git commit -m "Added new feature: possibility to reach the Moon in
        one step"

9. Push your changes to GitHub:

        $ git push

10. Create a pull request from your forked repository to [wt][wt] repository.


## Hack wt documentation

1. Follow steps 1-5 from [Hack wt](#hack-wt) section.

2. Install `honcho` to automate docs related tasks:

        $ pip install honcho

    `honcho` will help to:

    - run **css** changes watcher to automate docs styles rebuild process,
    - run docs development mode http server.

3. Install `nodejs` packages used to (re)generate `wt` documentation
   **css** styles:

        $ npm install

    or:

        $ yarn install

4. Run `d` helper:

        $ ./d

    and navigate to [http://127.0.0.1:9100/](http://127.0.0.1:9100/) in your
    browser to check generated `wt` docs.
    Hit `Ctrl-C` to stop `d` helper.

5. Edit `wt` documentation as needed (you can do it using editor of your
   choice) and check generated results in browser.

    Documention sources are located in `env/src/wt/docs/` directory.

6. Commit your changes providing useful commit message:

        $ git commit -m "Updated docs: added instruction how to reach the Moon
        in one step"

7. Push your changes to GitHub:

        $ git push

8. Create a pull request from your forked repository to [wt][wt] repository.





[wt]: https://github.com/ysegorov/wt/
[wt-issues]: https://github.com/ysegorov/wt/issues
[wt-dev]: https://github.com/ysegorov/wt-dev/
