# Customize the primary sidebar

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

- `sidebar-logo.html`: Displays the logo and site title.
- `search-field.html`: A bootstrap-based search bar (from the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/))
- `sbt-sidebar-nav.html`: A bootstrap-based navigation menu for your book.
- `sbt-sidebar-footer`: A [configurable](custom-footer) snippet of HTML to add to the sidebar (by default it is placed at the bottom).

(custom-footer)=
## Customize the sidebar footer

You may choose your own HTML to include in the footer of your sidebar (or set it to be empty). To do so, set the following option in `conf.py`:

```python
html_theme_options = {
    ...
    "extra_navbar": "<p>Your HTML</p>",
    ...
}
```

This text will be placed at the bottom of the sidebar by default.


## Add a header to your Table of Contents

If you'd like to add a header above a section of TOC links, use `:caption: My header text`
in your `toctree` directive for that section.

(sidebar-primary:logo)=
## Customize the logo, title, and favicon

You can customize the logo, title, and favicon of your site with the following Sphinx configuration in `conf.py`:

```python
html_title = "Your title"
html_logo = "path/to/logo.png"
html_favicon = "path/to/favicon.ico"
```

These will be placed in the top-left of your page.

To **remove the site title** below the logo, add this line in `conf.py`:

```python
html_theme_options = {
  ...
  "logo_only": True,
  ...
}
```

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

(sidebar:navbar-depth)=
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
