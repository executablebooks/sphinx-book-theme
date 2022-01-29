## Architecture of the repository

This is a short overview of the general architecture and structure of the repository, to help you orient yourself.

This theme uses [sphinx-theme-builder](https://sphinx-theme-builder.readthedocs.io/en/latest/) as its build backend, and follows the [filesystem layout](https://sphinx-theme-builder.readthedocs.io/en/latest/reference/filesystem-layout/) recommended by it.
See below for some more specific sections

### `src/sphinx_book_theme/` - Theme source files

This folder contains all of the source files for this theme, and most changes to the theme are made somewhere inside this folder.

`__init__.py`
: The theme's Python module, which runs several configuration and set-up steps.
  This module does things like load in Sphinx's default HTML for the sidebar, and modify it in order to have dropdown nested lists.
  It also inserts several variables into the Jinja template context that are then used in our HTML templates.

`launch.py`
: Logic to create the correct URLs for our launch buttons. This basically means building the URL for a given launch service in a proper fashion.

The other folders in this section are described in the next few sections.

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
For a high-level overview, see the file `/assets/styles/index.scss`.

```{note}
We also inherit a lot of SCSS rules from [the PyData Sphinx Theme styles](https://github.com/pydata/pydata-sphinx-theme/tree/master/src/pydata_sphinx_theme/assets/styles).
```

#### `/translations/` - Translations and internationalization

This folder contains all of the translations that we use in this theme, so that it may be used in many different base languages.
For more information about our translation infrastructure, see `/translations/README.md`.

### `docs/` - Site documentation

The documentation for the theme, written as a Sphinx documentation site.
The documentation tries to follow [the Diataxis.fr documentation framework](https://diataxis.fr/).

Here is a brief overview:

- `docs/*.md`: Contains several topic sections for the documentation (e.g. `content-blocks.md` covers special content blocks for this theme)
- `docs/tutorials/`: Step-by-step tutorials that cover how to do a particular thing from beginning to end.
- `docs/reference/`: Reference sections of the documentation, to demonstrate the look and feel of the theme.
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
