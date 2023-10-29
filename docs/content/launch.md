(customize:launch)=
# Launch buttons for interactivity

You can automatically add buttons that allow users to interact with your
book's content. This is either by directing them to a BinderHub or JupyterHub
that runs in the cloud, or by making your page interactive using Thebe.

To use either Binder or JupyterHub links, you'll first need to configure your
documentation's repository url:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    "repository_branch": "{your-branch}",
    "path_to_docs": "{path-relative-to-site-root}",
    ...
}
```

```{margin} Paired ipynb files

If you're using [Jupytext](https://jupytext.readthedocs.io/en/latest/) to
pair an ipynb file with your text files, and that ipynb file is in the same
folder as your content, then Binder/JupyterHub links will point to the ipynb
file instead of the text file.
```

## Binder / BinderHub

To add Binder links to your page, add the following configuration:

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "binderhub_url": "https://{your-binderhub-url}"
    },
    ...
}
```

## JupyterHub

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

## Google Colab

To add Google Colab links to your page, add the following configuration:

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "colab_url": "https://colab.research.google.com"
    },
    ...
}
```
## Deepnote

To add [Deepnote](https://deepnote.com) links to your page, add the following configuration:

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "deepnote_url": "https://deepnote.com"
    },
    ...
}
```

```{warning}
This will create a new Deepnote project every time you click the launch button.
```


## Live code cells with Thebe

[Thebe](http://thebe.readthedocs.org/) converts your static code blocks into
*interactive* code blocks powered by a Jupyter kernel. It does this by asking for a BinderHub kernel
*under the hood* and converts all of your
code cells into *interactive* code cells. This allows users to run the code on
your page without leaving the page.

You can use the Sphinx extension
[`sphinx-thebe`](https://sphinx-thebe.readthedocs.io/en/latest/) to add
live code functionality to your documentation. You can install `sphinx-thebe` from `pip`,
then activate it by putting it in your `conf.py` extensions list:

```python
extensions = [
    ...
    "sphinx_thebe"
    ...
]
```

If you'd like to activate UI elements for `sphinx-thebe` in the `sphinx-book-theme`,
add the following theme configuration:

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "thebe": True,
    },
    ...
}
```

This will add a custom launch button and some UI elements will be added for Thebe.

If you also specify a `repository_url` with your theme configuration, `sphinx-thebe`
will use this repository for its environment:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    ...
}
```

```{tip}
You can also manually customize Thebe with the `thebe_config` dictionary.
This will over-ride any configuration that is pulled from your `html_theme_options`
configuration. See the [`sphinx-thebe`](https://sphinx-thebe.readthedocs.io/en/latest/)
documentation for what you can configure.
```

## Configure a relative path to your source file

To configure a relative path to your documentation, add the following configuration:

```python
html_theme_options = {
    ...
    "path_to_docs" = "{path-relative-to-repo-root}"
    ...
}
```

## Control the user interface that is opened

You can control the interface that is opened when somebody clicks on a launch button.
To do so, add the following configuration:

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "notebook_interface": "jupyterlab",
    },
    ...
}
```
