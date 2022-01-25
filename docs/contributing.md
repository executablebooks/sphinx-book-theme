# Contributing Guide

Thank you for being interested in contributing to the `sphinx-book-theme`! You
are awesome ✨.

This project follows the Executable Books Project [contribution guidelines](https://executablebooks.org/en/latest/contributing.html).
It contains information about our conventions around coding style, pull request workflow, commit messages and more.

This page contains information to help you get started with development on this
project.

## Repository structure

This theme uses `sphinx-theme-builder` as its backend, and follows the [filesystem layout](https://sphinx-theme-builder.readthedocs.io/en/latest/reference/filesystem-layout/) recommended by it.
On top of that, it has the following additional critical files/folders:

`webpack.config.js`
: Contains the compilation code to convert source files like SCSS and JS in `src/sphinx_book_theme/assets/*` into the production assets in `src/sphinx_book_theme/theme/sphinx_book_theme/static/` .
: This compilation is called by default, during development commands (see below).

`docs/`
: The documentation for the theme, which aims to include all of the core Sphinx "components" (lists, admonitions, etc), to check/show how they are represented in this theme.
: The build configuration is contained in `conf.py`.

`docs/reference`
: The reference section of the documentation contains reference material for the look and feel of the theme.
  The "kitchen sink" is pulled directly [from the `sphinx-themes` website](https://github.com/sphinx-themes/sphinx-themes.org/tree/master/sample-docs/kitchen-sink).
  There are also other sections for theme-specific elements.

`tests/`
: Testing infrastructure that uses `pytest` along with `beautifulsoup` to validate
  that the generated HTML is what we expect it to be.
: Much of these tests also use `pytest-regressions`, to check whether newly-generated HTML differs from previously-generated HTML.

`.github/workflows/`
: Contains Continuous-integration (CI) workflows, run on commits/PRs to the GitHub repository.


## Set up your development environment

1. Get the source code of this project using git:

   ```bash
   git clone https://github.com/executablebooks/sphinx-book-theme
   cd sphinx-book-theme
   ```

2. Ensure you have Python 3.7 or newer!
3. Install `tox`.
   `tox` is a tool for managing virtual environments for test suites or common jobs that are run with a repository.
   It ensures that your environment is consistent each time you build the docs.

   ```console
   $ pip install tox
   ```

   You can list all of the `tox` environments like so:

   ```console
   $ tox -a
   ```

   Each one corresponds to a test environment or a task to build the documentation, and has its own virtual environment.

   See the `sphinx-book-theme/tox.ini` for details of all available development environments.
4. Install `pre-commit`.
   We use pre-commit to ensure that the code meets certain standards any time a commit is made.
   First, [follow the `pre-commit` installation instructions](https://pre-commit.com/#install).
   Then, run the following command in the same folder as the repository:

   ```console
   $ pre-commit install
   ```

   :::{note}
   You can also run pre-commit via `tox`:
   ```console
   $ tox -e py38-pre-commit -- --all
   ```
   or manually run all `pre-commit` jobs for this repository:

   ```console
   $ pre-commit run --all-files
   ```
   :::


## Preview changes you make to the theme

The easiest way to preview the changes you make to this theme is by building the documentation of this theme locally using `tox`.

To do so, follow these steps:

1. **Make your changes in `src/`**. This folder contains all of the SCSS and Javascript that are used in this site. You should edit the files here, and they will be built and included with the site in the `sphinx_book_theme/` folder at build time.
2. **Install `tox`**.

   ```console
   $ pip install tox
   ```
3. **Compile the assets**. For compiling static assets, use the following `tox` command:

   ```console
   $ tox -e compile
   ```
4. **Build the documentation**. You can use the following `tox` command:

   ```console
   $ tox -e docs-update
   ```

This will build the documentation using the latest version of the theme (including any changes you've made to the `src/sphinx_book_theme/assets/*` folder) and put the outputs in `docs/_build/html`.
You may then preview them by opening one of the HTML files.

### Auto-build the docs when you make changes

You can also use a live server to watch the theme's folders, and automatically build/update the local documentation so that you can quickly preview changes.
This uses the `sphinx-autobuild` package.
To do so, use this `tox` command:

```console
$ tox -e docs-live
```

This will do the following:

- Generate the theme's documentation (similar to running `tox -e docs-update`)
- Start a development server on an available port `127.0.0.1:xxxx`
- Open it in your default browser
- Watch for changes and automagically regenerate the documentation and auto-reload your browser when a change is made.

With this, you can modify the theme in an editor, and see how those modifications render on the browser.

## Run Tests

This theme has a test suite to ensure that all the relevant user content is
correctly handled. The tests can be run using:

```console
$ tox
```

You can also run against different Python and sphinx versions, and supply arguments to pytest:

```console
$ tox -e py38-sphinx3 -- -x
```

:::{tip}
To "re-build" an environment, wih updated dependancy versions, use:

```console
$ tox -r -e py38-sphinx3
```

:::


## Update or add translations for new languages

This theme has support for translating several theme phrases into multiple languages.
For more information about this workflow, see [the translations README](https://github.com/executablebooks/sphinx-book-theme/tree/HEAD/sphinx_book_theme/translations).


## Test audits with lighthouse

This theme uses the [`treosh/lighthouse-ci-action`](https://github.com/treosh/lighthouse-ci-action) to run some basic audits on our performance, accessibility, etc.

To preview the output of these tests:

- Click on the `docs-audit` GitHub Action job from a Pull Request.
- Scroll to the "Audit with Lighthouse" section
- If there are errors, you should see them along with the link to preview the report at `report: <URL TO PAGE>`.
- If there are not errors, you can list them by clicking the `uploading` section, which will reveal links to the report for each page
