# Get started with the theme

This is a short step-by-step tutorial to get started with the Sphinx Book Theme.

:::{note}
This documentation and the examples below are written with MyST Markdown, a form
of markdown that works with Sphinx. For more information about MyST markdown, and
to use MyST markdown with your Sphinx website,
see [the MyST-parser documentation](https://myst-parser.readthedocs.io/)
:::

## Prerequisites

You should be relatively familiar with [the Sphinx ecosystem](http://www.sphinx-doc.org/), and have it installed locally on your computer.

:::{note}
If you don't already have a Sphinx site ready to customize, you can create one with:

```bash
sphinx-quickstart
```
:::

## Install and activate the theme

First install `sphinx-book-theme` with `pip`:

```
pip install sphinx-book-theme
```

then, activate the theme in your Sphinx configuration (`conf.py`):

```
...
html_theme = "sphinx_book_theme"
...
```

This will activate the Sphinx Book Theme for your documentation.

:::{note}
You may need to comment-out your `html_theme_options` configuration depending on your previous theme.
:::

## Customize your topbar

There are several ways that you can customize the Sphinx Book Theme.
For this tutorial, we'll add a pointer to a GitHub repository for our theme.

To add
