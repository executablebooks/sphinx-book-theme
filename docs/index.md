# The Sphinx Book Theme

[![badge-url](https://img.shields.io/github/stars/executablebooks/sphinx-book-theme?label=github&style=social)](https://github.com/executablebooks/sphinx-book-theme)

**An interactive book theme for Sphinx**.

This is a lightweight Sphinx theme designed to mimic the look-and-feel of an
interactive book. It has the following primary features:

* **[Bootstrap 4](https://getbootstrap.com/docs/4.0/getting-started/introduction/)**
  for visual elements and functionality.
* **[Flexible content layout](layout)** that is inspired by beautiful online books,
  such as [the Edward Tufte CSS guide](https://edwardtufte.github.io/tufte-css/)
* **[Visual classes designed for Jupyter Notebooks](notebooks)**. Cell inputs, outputs,
  and interactive functionality are all supported.
* **[Launch buttons for online interactivity](launch)**. For pages that are built with
  computational material, connect your site to an online BinderHub for interactive content.

## Site contents

```{toctree}
:maxdepth: 1
:caption: Main docs
configure
Controlling page elements <layout>
notebooks
launch
contributing
GitHub repository <https://github.com/executablebookproject/sphinx-book-theme>
```

## Reference pages

```{toctree}
:caption: Reference items
:maxdepth: 2
reference/index
```

## Acknowledgements

This theme is heavily inspired by (and dependent on)
[PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/) for its base
structure and configuration.
