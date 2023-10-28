(contributing/style)=
# Style and design

This describes the principles and infrastructure behind the style and design aspects of this theme.

## Design principles and inspiration

Here are a few guiding principles for the design of this theme:

- **Use minimalistic visual elements.** This theme should not have "strong visual opinions" beyond a clean and minimal design.
  For example, use whitespace instead of color blocks to separate content, use unintrusive visual elements where possible, use color sparingly, etc.
- **Focus on a single book use-case.** This theme is designed for the use-case where a person has documentation for a single reader archetype, where all aspects of the documentation may be exposed to the reader. This means we follow a two-column layout with a single navigation bar across all pages. Header navigation should require more customization.
- **Add design elements from the Tufte theme**. The [Edward Tufte CSS theme](https://edwardtufte.github.io/tufte-css/) defines several styles and elements that are unique for communicating ideas with data. We give a few of these (like margin content) special treatment, and generally assume Tufte knows what he's doing.

This theme draws inspiration and borrows design elements from the following themes:

- The [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/)
- The [Furo theme](https://pradyunsg.me/furo/)
- The [Edward Tufte CSS theme](https://edwardtufte.github.io/tufte-css/)
- [GitBook](https://docs.gitbook.com/)
- The [Tailwind CSS docs](https://tailwindcss.com/docs/installation)

## SCSS build process

Our SCSS source files at in `src/sphinx_book_theme/assets/styles`.
We use the [Sphinx Theme Builder](https://github.com/pradyunsg/sphinx-theme-builder) to compile these assets and bundle them with the theme at `src/sphinx_book_theme/theme/sphinx_book_theme/static/styles`.

These compiled files are **not checked in to `git` history**.

You can run the compilation process with `tox` like so:

```console
$ tox -e compile
```

or you may manually run this if you have installed the `sphinx-theme-builder` with this command:

```console
$ stb compile
```

## CSS/SCSS naming conventions

We try to follow the [`block__element--modifier` naming convention for CSS](https://cssguidelin.es/#bem-like-naming).

This is aspirational!
Many of our HTML elements do not quite follow this naming, and over time we hope to continue making adjustments to get closer to this frameowrk.

## SCSS folder structure

Our SCSS files follow the structured described in [the sass-guidelines guide](https://sass-guidelin.es/#architecture).
For a high-level overview, see the file `/assets/styles/index.scss`.

```{note}
We also inherit a lot of SCSS rules from [the PyData Sphinx Theme styles](https://github.com/pydata/pydata-sphinx-theme/tree/master/src/pydata_sphinx_theme/assets/styles).
```
