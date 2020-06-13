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
