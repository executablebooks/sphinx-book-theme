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
        "colab_url": "https://{your-colab-url}"
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

## JupyterLite and RetroLite

```{admonition} Experimental!
:class: warning
Behavior and configuration of JupyterLite may change over time!
```

[JupyterLite](https://jupyterlite.readthedocs.io/) allows you to run a Jupyter environment entirely in the browser via [WebAssembly](https://webassembly.org/) and [Pyodide](https://pyodide.org/en/stable/).

To use JupyterLite in your launch buttons, you'll first need to take these steps:

1. **Install [`jupyterlite-sphinx`](https://jupyterlite-sphinx.readthedocs.io/)** by
    [following the installation instructions](https://jupyterlite-sphinx.readthedocs.io/en/latest/installation.html).
2. **Configure JupyterLite Sphinx to use your site content as a folder**.
   You can configure JupyterLite Sphinx to look for notebooks in a specified directory. 
   Put the notebooks you wish to expose in that directory, and [follow these configuration instructions](https://jupyterlite-sphinx.readthedocs.io/en/latest/configuration.html#jupyterlite-content).


### Retrolite

To add [RetroLite](https://jupyterlite-sphinx.readthedocs.io/en/latest/retrolite.html) links to your page, add the following configuration:

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "retrolite_url": "/lite/retro/notebooks/"
    },
    ...
}
```

There are two different interfaces that you can activate with JupyterLite, each is described below.

### JupyterLab

To add JupyterLab via JupyterLite to your launch buttons, use the following configuration:

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "jupyterlite_url": "/lite/lab/notebooks/"
    },
    ...
}
```

Where `notebooks/` is a folder with a collection of Jupyter Notebooks you'd like to serve with JupyterLite.


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
