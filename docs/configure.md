# Configuration

A few configuration options for this theme

```{note}
This documentation and the examples below are written with MyST Markdown, a form
of markdown that works with Sphinx. For more information about MyST markdown, and
to use MyST markdown with your Sphinx website,
see [the MyST-parser documentation](https://myst-parser.readthedocs.io/)
```

## Source repository buttons

There are a collection of buttons that you can use to link back to your source
repository. This lets users browse the repository, or take actions like suggest
an edit or open an issue. In each case, they require the following configuration
to exist:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    ...
}
```

### Add a link to your repository

To add a link to your repository, add the following configuration:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    "use_repository_button": True,
    ...
}
```

### Add a button to open issues

To add a button to open an issue about the current page, use the following
configuration:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    "use_issues_button": True,
    ...
}
```

### Add a button to suggest edits

You can add a button to each page that will allow users to edit the page text
directly and submit a pull request to update the documentation. To include this
button, use the following configuration:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    "use_edit_page_button": True,
    ...
}
```

By default, the edit button will point to the `master` branch, but if you'd like
to change this, use the following configuration:

```python
html_theme_options = {
    ...
    "repository_branch": "{your-branch}",
    ...
}
```

By default, the edit button will point to the root of the repository. If your
documentation is hosted in a sub-folder, use the following configuration:

```python
html_theme_options = {
    ...
    "path_to_docs": "{path-relative-to-site-root}",
    ...
}
```
## Download page button

You can add a button allowing users to download the currently viewed page in several formats: raw, pdf or ipynb if available. To include this button, use the following configuration:

```python
html_theme_options = {
    ...
    "use_download_button": True,
    ...
}
```

## Use a single-page version of this theme

If your documentation only has a single page, and you don't need the left
navigation bar, then you may configure `sphinx-book-theme` to run in **single page mode**
with the following configuration:

```python
html_theme_options = {
    ...
    "single_page": True
    ...
}
```

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

## Control the right sidebar items

You can rename the title of the in-page table of contents, in the right sidebar:

```python
html_theme_options = {
    "toc_title": "{your-title}"
}
```

The default value of the title is `Contents`.

## Control the left sidebar items

You can control what kind of content goes underneath the logo and name of your website in the top left.

To do so, use the `html_sidebars` variable in your `conf.py` file. This takes a dictionary of filename patterns as keys, and a list of sidebar elements as values. Any files that match a key will have the corresponding sidebar elements placed in that page's sidebar.

For example, the following configuration would include *only the footer* on pages under the `posts/` folder:

```python
html_sidebars = {
    "posts/*": ["sbt-sidebar-footer.html"]
}
```

You can also use `**` to apply a set of sidebars to **all** pages of your book. For example:

```python
html_sidebars = {
    "**": ["sbt-sidebar-nav.html", "sbt-sidebar-footer.html"]
}
```

See the [Sphinx HTML sidebars documentation](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_sidebars) for more information.

### Default sidebar elements

By default, this theme comes with these three theme-specific sidebar elements enabled on all pages:

- `sidebar-search-bs.html`: A bootstrap-based search bar (from the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/))
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


## Customize the logo, title, and favicon

You can customize the logo, title, and favicon of your site with the following Sphinx configuration in `conf.py`:

```python
html_title = "Your title"
html_logo = "path/to/logo.png"
html_favicon = "path/to/favicon.ico"
```

These will be placed in the top-left of your page.


## Control the depth of the left sidebar lists to expand

You can control the level of toc items in the left sidebar to remain expanded,
using the following configuration in `conf.py`:

```python
show_navbar_depth = <level>
```

The default value is 1, which is used in this documentation.
Value of 0 will collapse all the sections and sub-sections by default.

## Customize CSS

To customize the look of your site further, you can customize your CSS stylesheets,
as described in the [ReadTheDocs Docs](https://docs.readthedocs.io/en/stable/guides/adding-custom-css.html#adding-custom-css-or-javascript-to-sphinx-documentation).

First, create a CSS file and place it in `_static/custom.css`.
An example CSS file to change the color of the top-level headers might look like this.

```css
h1 {
    color: #003B71 !important;
}
```

You also need these two lines in your `conf.py` file
```python
html_static_path = ["_static"]
html_css_files = ["custom.css"]
```
