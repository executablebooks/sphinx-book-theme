# Contributing Guide

Thank you for being interested in contributing to the `sphinx-book-theme`! You
are awesome ✨.

This project follows the Executable Books Project [contribution guidelines](https://executablebooks.org/en/latest/contributing.html).
It contains information about our conventions around coding style, pull request workflow, commit messages and more.

This page contains information to help you get started with development on this
project.

## Development

### Set-up

Get the source code of this project using git:

```bash
git clone https://github.com/executablebooks/sphinx-book-theme
cd sphinx-book-theme
```

To work on this project, you need Python 3.6 or newer.
Although you can create your own development environment,
the recommended way to work on development is *via* [tox](https://tox.readthedocs.io), which can be installed with pip:

```console
$ pip install tox
# list all environments
$ tox -a
```

If you have Conda installed you may also consider installing the plugin:

```console
$ pip install tox-conda
```

See the `sphinx-book-theme/tox.ini` for details of all available development environments.

### Running Tests

This theme has a test suite to ensure that all the relevant user content is
correctly handled. The tests can be run using:

```console
$ tox
```

You can also run against different Python and sphinx versions, and supply arguments to pytest:

```console
$ tox -e py38-sphinx2 -- -x
```

:::{tip}
To "re-build" an environment, wih updated dependancy versions, use:

```console
$ tox -r -e py38-sphinx2
```

:::

### Running Pre-commit

The consistency and code style in this project is enforced with multiple automated [pre-commit](https://pre-commit.com) hooks.
You can run them using:

```console
$ tox -e py38-pre-commit -- --all
```

or directly (after installing pre-commit):

```console
$ pre-commit run --all
$ pre-commit install
```

### Working on the theme

If you're making changes to your local copy of this theme, you can get feedback on the rendered documentation output,
by either building the documentation "statically":

```console
$ tox -e docs-clean
$ tox -e docs-update
```

This will generate the HTML documentation and compile the relevant stylesheets.
The generated documentation which can be viewed in `docs/_build/`.

Alternatively, you can have the documentation built "live", as you modify files:

This will generate the theme's documentation, start a development server on an available port localhost:xxxx, open it in your default browser,
then watch for changes and automagically regenerate the documentation and auto-reload your browser:

```console
$ tox -e docs-live
```

With this, you can modify the theme in an editor, and (after a small delay) see
how those modifications render on the browser.

You can also try different builders:

```console
$ tox -e docs-update -- singlehtml
$ tox -e docs-live -- singlehtml
```

## Repository structure

This repository is a split into a few critical folders:

sphinx-book-theme/
: The Sphinx extension package, containing the Python code, Jinja templates and (compiled) assets (HTML/CSS/JS etc).
: These are used to generate the HTML page for every file in your site whenever the site is built using Sphinx.
: **NOTE**: Do not alter the compiled CSS/JS directly (alter in `src/`).

src/
: Contains the source SCSS and JS, which will be compiled and written to `sphinx-book-theme/static`, as configured by `web-compile-config.yml` (see [executablebooks/web-compile](https://github.com/executablebooks/web-compile) for details).
: This compilation is called by default, during development commands (see above).

docs/
: The documentation for the theme, which aims to include all of the core Sphinx "components" (lists, admonitions, etc), to check/show how they are represented in this theme.
: The build configuration is contained in `conf.py`.

tests/
: Testing infrastructure that uses `pytest` along with `beautifulsoup` to validate
  that the generated HTML is what we expect it to be.
: Much of these tests also use `pytest-regressions`, to check whether newly-generated HTML differs from previously-generated HTML.

.github/workflows/
: Contains Continuous-integration (CI) workflows, run on commits/PRs to the GitHub repository.
