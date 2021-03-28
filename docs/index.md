# The Sphinx Book Theme

[![badge-url](https://img.shields.io/github/stars/executablebooks/sphinx-book-theme?label=github&style=social)](https://github.com/executablebooks/sphinx-book-theme)
[![PyPI][pypi-badge]][pypi-link]

<br />

**An interactive book theme for Sphinx**.

This is a lightweight Sphinx theme designed to mimic the look-and-feel of an
interactive book. It has the following primary features:

[Bootstrap 4](https://getbootstrap.com/docs/4.0/getting-started/introduction/)
: To style visual elements and add functionality.

[Flexible content layout](layout)
: Inspired by beautiful online books, such as [the Edward Tufte CSS guide](https://edwardtufte.github.io/tufte-css/)

[Visual classes designed for Jupyter Notebooks](notebooks)
: Cell inputs, outputs, and interactive functionality are all supported.

[Launch buttons for online interactivity](launch)
: For pages that are built with computational material, connect your site to an online BinderHub for interactive content.

International
: All text integrated in the theme is translated to the specified [Sphinx language](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language).

:::{seealso}
This is the default theme in [Jupyter Book](https://jupyterbook.org).
:::

## Site contents

```{toctree}
:maxdepth: 1
:caption: Tutorials

tutorials/get-started
```


```{toctree}
:maxdepth: 1
:caption: Topic Areas

configure
Controlling page elements <layout>
notebooks
launch
```

## Reference pages

```{toctree}
:caption: Reference
:maxdepth: 2

reference/index
api/index
```


```{toctree}
:caption: About the theme
:maxdepth: 2

contributing
```

## Acknowledgements

This theme is heavily inspired by (and dependent on)
[PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/) for its base
structure and configuration.

[pypi-badge]: https://img.shields.io/pypi/v/sphinx-book-theme.svg
[pypi-link]: https://pypi.org/project/sphinx-book-theme
