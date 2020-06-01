# Configuration

A few configuration options for this theme

```{note}
This documentation and the examples below are written with MyST Markdown, a form
of markdown that works with Sphinx. For more information about MyST markdown, and
to use MyST markdown with your Sphinx website,
see [the MyST-parser documentation](https://myst-parser.readthedocs.io/)
```

## Add an Edit this Page button

You can add a button to each page that will allow users to edit the page text
directly and submit a pull request to update the documentation. To include this
button in the right sidebar of each page, add the following configuration to
your `conf.py` file:

```python
html_theme_options = {
    ...
    "use_edit_page_button": True
    ...
}
```

and configure your documentations repository information:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    "path_to_docs": "{path-relative-to-site-root},
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
