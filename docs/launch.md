# Launch buttons for interactivity

You can automatically add buttons that allow users to interact with your
book's content. This is either by directing them to a BinderHub or JupyterHub
that runs in the cloud, or by making your page interactive using Thebelab.

To use either Binder or JupyterHub links, you'll first need to configure your
documentation's repository url:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    "repository_branch": "{your-branch}",
    "path_to_docs": "{path-relative-to-site-root},
    ...
}
```

```{margin} Paired ipynb files

If you're using [Jupytext](https://jupytext.readthedocs.io/en/latest/) to
pair an ipynb file with your text files, and that ipynb file is in the same
folder as your content, then Binder/JupyterHub links will point to the ipynb
file instead of the text file.
```

## Types of Launch Buttons

### Binder / BinderHub

To add Binder links your page, add the following configuration:

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "binderhub_url": "https://{your-binderhub-url}"
    },
    ...
}
```

### JupyterHub

To add JupyterHub links to your page, add the following configuration:

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "jupyterhub_url": "https://{your-binderhub-url}"
    },
    ...
}
```

### Google Colab

To add Google Colab links to your page, add the following configuration:

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "colab_url": "https://{your-colab-url}"
    },
    ...
}
```

### Thebelab

Thebelab asks for a BinderHub kernele *under the hood* and converts all of your
code cells into *interactive* code cells. This allows users to run the code on
your page without leaving the page.

To add Thebelab links to your page, first configure your page as you would for
a BinderHub launch button, then add the following configuration:

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "binderhub_url": "https://{your-binderhub-url}",
        "thebelab": True,
    },
    ...
}
```

```{tip}
You can also manually customize Thebelab with the `thebelab_config` dictionary.
This will over-ride any configuration that is pulled from your `html_theme_options`
configuration. See the [`sphinx-thebelab`](https://sphinx-thebelab.readthedocs.io/en/latest/)
documentation for what you can configure.
```

## Configuration

**To configure a relative path to your documentation**, add the following configuration:

```python
html_theme_options = {
    ...
    "path_to_docs" = "{path-relative-to-repo-root}"
    ...
}
```

**To control the user interface that is opened with links**, add the following configuration:

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "notebook_interface": "jupyterlab",
    },
    ...
}
```
