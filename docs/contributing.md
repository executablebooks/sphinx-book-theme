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

To work on this project, you need Python 3.6 or newer. Most of this project's
development workflow commands use `nox`, which can be installed with pip:

```bash
pip install nox
```

### Building documentation

You can now build documentation with your local copy of this theme! Try it
out on the theme's documentation like so:

```bash
nox -s docs
```

This will generate the HTML documentation and compile the relevant stylesheets.
The generated documentation which can be viewed by opening
`docs/_build/html/index.html` in your browser.

### Running Tests

This theme has a test suite to ensure that all the relevant user content is
correctly handled. The tests can be run using:

```bash
nox -s tests
```

This will run tests against all supported version of Python that are installed.

If you want to run tests for a specific version of Python (say, 3.8), you can
do so using:

```bash
nox -s tests-3.8
```

### Running Linters

The code style in this project is enforced with multiple automated linters. You
can run them using:

```bash
nox -s lint
```

### Working on the theme "live"

If you're making changes to your local copy of this theme, there is a helper
command :

```bash
nox -s docs-live
```

This will start a development server at localhost:8000, which generates this
theme's documentation, and open it in your default browser. The development
server will watch for changes. When a change occurs, it will automagically
regenerate the documentation and auto-reload your browser.

With this, you can modify the theme in an editor, and (after a small delay) see
how those modifications render on the browser.

### Pre-commit

To ensure a commit will pass the linting and compilation CI checks, it is recommended that you also install the [pre-commit](https://pre-commit.com) hooks.

```console
$ pre-commit install
```

## Repository structure

This repository is a combination of a few parts:

* **HTML/SCSS/JS assets** that define the theme's structure.

  The HTML files are Jinja templates that are located in
  [the `sphinx-book-theme/` folder](https://github.com/executablebooks/sphinx-book-theme/tree/master/sphinx_book_theme). These are used to generate the HTML page for every file
  in your site whenever the site is built.

  The SCSS/JS files are located in [the theme's `static/` folder](https://github.com/executablebooks/sphinx-book-theme/tree/master/sphinx_book_theme/static).
  The SCSS files will be compiled to CSS whenever your documentation is built.

* **A python Sphinx extension** that integrates these assets with a Sphinx build.
  These are the Python files [in the `sphinx_book_theme/` folder](https://github.com/executablebooks/sphinx-book-theme/tree/master/sphinx_book_theme).

* **Testing infrastructure** that uses `pytest/` along with `beautifulsoup` to validate
  that the generated HTML is what we expect it to be. You can find all of this
  [in the `tests/` folder](https://github.com/executablebooks/sphinx-book-theme/tree/master/tests).
  Much of these tests uses `pytest-regressions/` to check whether newly-generated
  HTML differs from previously-generated HTML.
