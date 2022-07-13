(customize:launch)=
# Launch buttons for interactivity

Launch buttons are a way to connect pages have computational content with environments that let readers execute and edit code interactively.
These use a variety of services that connect the user with a live kernel.

## Common configuration

There is some configuration that will be applied to almost all launch buttons.
To **over-ride these global values for each button**, you can manually specify different values within each launch button's configuration.

Here are the global configuration variables:

```python
html_theme_options = {
    ...
    # The location of your documentation relative to the repository root
    "path_to_docs": "docs/",
    # The URL where your documentation's content exists
    "repository_url": "https://github.com/{your-docs-url}",
    # The branch where your documentation's content exists
    "repository_branch": "{your-branch}",
    ...
}
```

```{margin} Paired ipynb files

If you're using [Jupytext](https://jupytext.readthedocs.io/en/latest/) to
pair an ipynb file with your text files, and that ipynb file is in the same
folder as your content, then Binder/JupyterHub links will point to the ipynb
file instead of the text file.
```

## Launch button configuration structure

Add launch buttons added by providing a **list of launch button configuration dictionaries** to the `html_theme_options.launch_buttons` configuration.

For example, the following configuration specifies two different kinds of JupyterHub buttons:

```python
html_theme_options = {
    "launch_buttons": [
        {
            "type": "jupyterhubhub",
            "hub_url": "https://myjupyterhub.org",
        },
        {
            "type": "jupyterhub",
            "hub_url": "https://myotherjupyterhub.org",,
        },
    ]
}
```

There is some configuration that is specific to a given launch button, described below.
The remaining sections of this page describe how to add various launch buttons.

## Binder / BinderHub

To add Binder links your page, add the following configuration:

```python
html_theme_options = {
    "launch_buttons": [
        ...,
        {
            # Specifies a binderhub launch button
            "type": "binderhub",
            # The URL of the binderhub where a session is launched
            "hub_url": "https://{your-binderhub-url}",
            # The notebook interface used when somebody clicks on a launch button.
            # Must be one of `jupyterlab` or `classic`
            "notebook_interface": "jupyterlab",
        },
        ...
    ]
}
```

## JupyterHub

To add JupyterHub links to your page, add the following configuration:

```python
html_theme_options = {
    "launch_buttons": [
        ...,
        {
            # Specifies a jupyterhub launch button
            "type": "jupyterhub",
            # The URL of the hub where a session is launched
            "hub_url": "https://{your-jupyterhub-url}",
            # The notebook interface used when somebody clicks on a launch button.
            # Must be one of `jupyterlab` or `classic`
            "notebook_interface": "jupyterlab",
        },
        ...
    ]
}
```


## Interactive code cells with Thebe

[Thebe](http://thebe.readthedocs.org/) converts your static code blocks into
*interactive* code blocks powered by a Jupyter kernel.
It does this by asking for a BinderHub kernel *under the hood* and converts all of your code cells into *interactive* code cells.
This allows users to run the code on your page without leaving the page.

To use interactive code cells, first ensure that [`sphinx-thebe`](https://sphinx-thebe.readthedocs.io/en/latest/) is installed:

```console
$ pip install sphinx-thebe
```

To add a {guilabel}`Interactive Code` button to your launch buttons, use the following configuration:

```python
html_theme_options = {
    "launch_buttons": [
        ...,
        {
            # Specifies a jupyterhub launch button
            "type": "thebe",
            # The URL of the binderhub that will serve your kernel
            "hub_url": "https://{your-jupyterhub-url}",
        },
        ...
    ]
}
```

```{tip}
You can also manually customize Thebe with the `thebe_config` dictionary.
This will over-ride any configuration that is pulled from your `html_theme_options`
configuration. See the [`sphinx-thebe`](https://sphinx-thebe.readthedocs.io/en/latest/)
documentation for what you can configure.
```


## Google Colab

To add Google Colab links to your page, add the following configuration:

```python
html_theme_options = {
    "launch_buttons": [
        ...,
        {
            "type": "colab",
        },
        ...
    ]
}
```

## Deepnote

To add [Deepnote](https://deepnote.com) links to your page, add the following configuration:

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "type": "deepnote",
    },
    ...
}
```

```{warning}
This will create a new Deepnote project every time you click the launch button.
```
