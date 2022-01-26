## Architecture of the repository

This is a short overview of the general architecture and structure of the repository, to help you orient yourself.

This theme uses [sphinx-theme-builder](https://sphinx-theme-builder.readthedocs.io/en/latest/) as its build backend, and follows the [filesystem layout](https://sphinx-theme-builder.readthedocs.io/en/latest/reference/filesystem-layout/) recommended by it.
See below for some more specific sections

### `src/sphinx_book_theme/` - Theme source files

This folder contains all of the source files for this theme, and most changes to the theme are made somewhere inside this folder.
The following sections describe where various functionality lives.

#### `/theme/sphinx_book_theme/` - HTML templates

This is the actual theme source that is packaged and distributed via PyPI.
It contains HTML templates that make up the theme structure.

These follow the [`sphinx-basic-ng` template structure](https://sphinx-basic-ng.readthedocs.io/en/latest).

- `layout.html` inherits from the [pydata sphinx theme](https://pydata-sphinx-theme.readthedocs.io/) and modifies several sections.
- `theme.conf` contains the Sphinx configuration file for this theme.

#### `/assets/scripts` - JavaScript assets

Contains JavaScript files for this theme. They are automatically compiled and inserted into the theme when new releases are made (or, via the command `stb compile`). They are **not checked in to `git` history**.

#### `/assets/styles` - SCSS assets

Contains SCSS files for this theme. They are automatically compiled and inserted into the theme when new releases are made (or, via the command `stb compile`). They are **not checked in to `git` history**.

Our SCSS files follow the structured described in [the sass-guidelines guide](https://sass-guidelin.es/#architecture).

### `docs/` - Site documentation

The documentation for the theme, which aims to include all of the core Sphinx "components" (lists, admonitions, etc), to check/show how they are represented in this theme.
- `docs/reference`: The reference section of the documentation contains reference material for the look and feel of the theme.
  The "kitchen sink" is pulled directly [from the `sphinx-themes` website](https://github.com/sphinx-themes/sphinx-themes.org/tree/master/sample-docs/kitchen-sink).
  There are also other sections for theme-specific elements.


### `webpack.config.js` and `package.json` - Webpack and dependencies

`webpack.config.js` contains the compilation code to convert source files like SCSS and JS in `src/sphinx_book_theme/assets/*` into the production assets in `src/sphinx_book_theme/theme/sphinx_book_theme/static/` .
This compilation is called by default, during development commands (see below).

### `tests/` - Testing infrastructure

Testing infrastructure that uses `pytest` along with `beautifulsoup` to validate
that the generated HTML is what we expect it to be.
Much of these tests also use `pytest-regressions`, to check whether newly-generated HTML differs from previously-generated HTML.

### `.github/workflows/` - Continuous Integration and Deployment

Contains Continuous-integration (CI) workflows, run on commits/PRs to the GitHub repository.
