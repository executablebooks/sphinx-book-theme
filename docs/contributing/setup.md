# Set up your development workflow

The following instructions will help you set up a basic development environment so that you can begin experimenting with changes.
This covers the basics, and see the other sections of the Contributing Guide for more details.

## Set up your development environment

First we'll install the necessary tools that you can use to begin making changes.
Follow these steps:

1. Get the source code of this project using git:

   ```bash
   git clone https://github.com/executablebooks/sphinx-book-theme
   cd sphinx-book-theme
   ```

2. Ensure you have Python 3.7 or newer!
3. Install `tox`.
   `tox` is a tool for managing virtual environments for test suites or common jobs that are run with a repository.
   It ensures that your environment is consistent each time you build the docs or run tests.

   ```console
   $ pip install tox
   ```
4. Install `pre-commit`.
   We use [pre-commit](https://pre-commit.com) to ensure that the code meets certain standards any time a commit is made.

   ```console
   $ pip install pre-commit
   ```

   Next, [follow the `pre-commit` installation instructions](https://pre-commit.com/#install).

   Finally, install the local dependencies for pre-commit.
   Run the following command in the same folder as the repository:

   ```console
   $ pre-commit install
   ```

   :::{margin}
   You can also run pre-commit via `tox`:
   ```console
   $ tox -e py38-pre-commit -- --all
   ```
   or manually run all `pre-commit` jobs for this repository:

   ```console
   $ pre-commit run --all-files
   ```
   :::

The rest of these instructions use `tox` to automate the installation and commands necessary to do many common things.

## Build the documentation

Now that you've installed the necessary tools, try building the documentation for this theme locally.
To do so, run the following `tox` command:

```console
$ tox -e docs-update
```

This will build the documentation using the latest version of the theme and put the outputs in `docs/_build/html`.
You may then preview them by opening one of the HTML files.

## Update the theme's assets (CSS/JS)

Now that you've previewed the documentation, try making changes to this theme's assets and see how they affect the documentation builds.
This is an easy way to preview the effect that your changes will make.

First, **make your changes in `src/sphinx_book_theme/assets/`**.
This folder contains all of the SCSS and Javascript that are used in this site.
For example, edit one of the `scss` files to add or modify a rule.

Next, **compile the changes**.
Run the following command:

```console
$ tox -e compile
```

This uses the [Sphinx Theme Builder](https://sphinx-theme-builder.readthedocs.io/) to compile our SCSS/JS files and bundle them with our theme at `src/sphinx_book_theme/theme/sphinx_book_theme/static`.
These compiled assets are **not included** in our git repository, but they **are included** in distributions of the theme.

Finally, **re-build the documentation** to preview your changes:

```console
$ rm -rf docs/_build/html
$ tox -e docs-update
```

When you open the HTML files for the documentation, your changes should be reflected.

## Auto-build the docs when you make changes

You can bundle both of the steps above into a single command, which also opens a live server that watches for changes to the theme's assets and documentation, and automatically compiles changes + re-builds the theme.

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

## Run the tests

Once you've made a change to the theme, you should confirm that the tests still pass, and potentially add or modify a test for your changes.

To run the test suite with the default `tox` environment, simply run this command:

```console
$ tox
```

This will run `pytest` against all of the files in `tests/` and display the result.
You can pass arguments to the `pytest` command like so:

```console
$ tox -- -k test_match
```

Anything passed after `--` will be passed directly to `pytest`.

:::{seealso}
See [](contribute/testing) for more information.
:::
