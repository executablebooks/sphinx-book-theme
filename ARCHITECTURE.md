# Architecture of the repository

This is a short overview of the general architecture and structure of the repository, to help you orient yourself.

This theme uses [sphinx-theme-builder](https://sphinx-theme-builder.readthedocs.io/en/latest/) as its build backend, and follows the [filesystem layout](https://sphinx-theme-builder.readthedocs.io/en/latest/filesystem-layout/) recommended by it.
See below for some more specific sections

```{contents}
```

## `src/sphinx_book_theme/` - Theme source files

This folder contains all of the source files for this theme, and most changes to the theme are made somewhere inside this folder.

`__init__.py`
: The theme's Python module, which runs several configuration and set-up steps.
  This module does things like load in Sphinx's default HTML for the sidebar, and modify it in order to have dropdown nested lists.
  It also inserts several variables into the Jinja template context that are then used in our HTML templates.

`header_buttons/`
: Scripts to generate metadata for buttons in the header. We use [Jinja Macros](https://jinja.palletsprojects.com/en/3.0.x/templates/) (in the `macros/` folder) to generate the HTML for header buttons. The scripts in `header_buttons/` generate the data structure that is used to generate buttons with these macros (in the `header-article.html` template).

`header_buttons/launch.py`
: Logic to create the correct URLs for our launch buttons. This basically means building the URL for a given launch service in a proper fashion.

The other folders in this section are described in the next few sections.

### `/theme/sphinx_book_theme/` - HTML templates

This is the actual theme source that is packaged and distributed via PyPI.
It contains HTML templates that make up the theme structure.

These follow the [`sphinx-basic-ng` template structure](https://sphinx-basic-ng.readthedocs.io/en/latest).

- `layout.html` inherits from the [pydata sphinx theme](https://pydata-sphinx-theme.readthedocs.io/) and modifies several sections.
- `theme.conf` contains the Sphinx configuration file for this theme.
- `macros/` contains HTML templates that define Jinja macros
- `sections/` contains HTML templates for major sections of the page.
- `components/` contains HTML templates for smaller, self-contained parts of the page.

### `/assets/scripts` - JavaScript assets

Contains JavaScript files for this theme. They are automatically compiled and inserted into the theme when new releases are made (or, via the command `stb compile`). They are **not checked in to `git` history**.

### `/assets/styles` - SCSS assets

Contains SCSS files for this theme.
These are compiled and bundled with the theme at build time.
See the [Style and Design section](contributing/style) for more information.

### `/translations/` - Translations and internationalization

This folder contains all of the translations that we use in this theme, so that it may be used in many different base languages.
For more information about our translation infrastructure, see `/translations/README.md`.

## `docs/` - Site documentation

The documentation for the theme, written as a Sphinx documentation site.
The documentation tries to follow [the Diataxis.fr documentation framework](https://diataxis.fr/).

Here is a brief overview:

- `docs/*.md`: Contains several topic sections for the documentation (e.g. `content-blocks.md` covers special content blocks for this theme)
- `docs/tutorials/`: Step-by-step tutorials that cover how to do a particular thing from beginning to end.
- `docs/reference/`: Reference sections of the documentation, to demonstrate the look and feel of the theme.
  The "kitchen sink" is pulled directly [from the `sphinx-themes` website](https://github.com/sphinx-themes/sphinx-themes.org/tree/master/sample-docs/kitchen-sink).
  There are also other sections for theme-specific elements.


## `webpack.config.js` and `package.json` - Webpack and dependencies

`webpack.config.js` contains the compilation code to convert source files like SCSS and JS in `src/sphinx_book_theme/assets/*` into the production assets in `src/sphinx_book_theme/theme/sphinx_book_theme/static/` .
This compilation is called by default, during development commands (see below).

## `tests/` - Testing infrastructure

Testing infrastructure that uses `pytest` along with `beautifulsoup` to validate
that the generated HTML is what we expect it to be.
Much of these tests also use `pytest-regressions`, to check whether newly-generated HTML differs from previously-generated HTML.

## `.github/workflows/` - Continuous Integration and Deployment

Contains Continuous-integration (CI) workflows, run on commits/PRs to the GitHub repository.

## Parent theme - `pydata-sphinx-theme`

This theme inherits a lot of functionality and design rules from its parent theme, the [PyData Sphinx Theme](https://github.com/pydata/pydata-sphinx-theme).
This is a theme designed for the PyData community, with a similar look and feel to the book theme.
Over time, we try to upstream any improvements made here into the parent theme, as long as the look and feel is the same between the two.

If you come across something in the codebase and you're not sure where it comes from (an example is the `generate_nav_html` function), you should [check the PyData Theme source files](https://github.com/pydata/pydata-sphinx-theme/tree/master/src/pydata_sphinx_theme) to see if it is defined there.
