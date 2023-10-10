# Primary sidebar and navigation

The primary sidebar generally contains the site navigation and logo.
By default it is on the left side of the site.
This page describes ways that you can control and customize the primary sidebar.

(sidebar-primary:items)=
## Control the left sidebar items

You can control what kind of content goes underneath the logo and name of your website in the top left.

To do so, use the `html_sidebars` variable in your `conf.py` file. This takes a dictionary of filename patterns as keys, and a list of sidebar elements as values. Any files that match a key will have the corresponding sidebar elements placed in that page's sidebar.

For example, the following configuration would include *only the footer* on pages under the `posts/` folder:

```python
html_sidebars = {
    "posts/*": ["sbt-sidebar-nav.html"]
}
```

You can also use `**` to apply a set of sidebars to **all** pages of your book. For example:

```python
html_sidebars = {
    "**": ["sbt-sidebar-nav.html"]
}
```

See the [Sphinx HTML sidebars documentation](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_sidebars) for more information.

### Default sidebar elements

By default, this theme comes with these three theme-specific sidebar elements enabled on all pages:

- `navbar-logo.html`: Displays the logo and site title.
- `search-field.html`: A bootstrap-based search bar (from the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/))
- `sbt-sidebar-nav.html`: A bootstrap-based navigation menu for your book.

## Add a header to your Table of Contents

If you'd like to add a header above a section of TOC links, use `:caption: My header text`
in your `toctree` directive for that section.


(sidebar-primary:home-page)=
## Add the home page to your table of contents

By default, your table of contents will begin with the first file that you add to a `toctree`. You can also configure the theme to show the **landing page** of the theme in your navigation bar as well.

To add the landing page of your site to the table of contents, use the following configuration:

```python
html_theme_options = {
    ...
    "home_page_in_toc": True
    ...
}
```

(sidebar:show-navbar-depth)=
## Control the depth of the left sidebar lists to expand

You can control the level of toc items in the left sidebar to remain expanded,
using the following configuration in `conf.py`:

```python
html_theme_options = {
    ...
    "show_navbar_depth": <level>,
    ...
}
```

The default value is `1`, which shows only top-level sections of the documentation (and is used in this documentation).

(sidebar:max-navbar-depth)=

## Control the maximum depth of the left sidebar lists

You can control the level of toc items included in the left sidebar,
using the following configuration in `conf.py`:

```python
html_theme_options = {
    ...
    "max_navbar_depth": <level>,
    ...
}
```

The default value is `4`.

(sidebar:collapse-navbar)=
## Turn off expandable left sidebar lists

You can turn off the sidebar expanding,
using the following configuration in `conf.py`:

```python
html_theme_options = {
    ...
    "collapse_navbar": True,
    ...
}
```

The default value is `False`, which allows the navbar to be expanded.
