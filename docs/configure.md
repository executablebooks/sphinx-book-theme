# Configuration

A few configuration options for this theme

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
    "repository_branch": "{your-branch}",
    "path_to_docs": "{path-relative-to-site-root},
    ...
}
```
