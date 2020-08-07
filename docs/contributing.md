# Contributing Guide

Thank you for being interested in contributing to the `sphinx-book-theme`! You
are awesome ✨.

This page contains developer documentation to help you get started.

```{toctree}
:hidden:
contributing-ebp
```

## The EBP Contributing Guide

This repository follows the `executablebooks/` contributors guide, which
you can find at [](contributing-ebp). It contains information

## Set up your dev environment

To set up your developer environment, do the following:

* Clone the repository

  ```bash
  git clone https://github.com/executablebooks/sphinx-book-theme
  cd sphinx-book-theme
  ```
* Install it locally with the developer tools

  ```bash
  pip install -e .[sphinx,testing,code_style]
  ```

* Install `pre-commit` and activate it for this repository

  ```bash
  pre-commit install
  ```

You can now build documentation with your local copy of this theme! Try it
out on the theme's documentation like so:

```bash
cd docs/
make html
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
