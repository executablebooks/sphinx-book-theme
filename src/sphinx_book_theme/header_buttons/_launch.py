from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlencode

from docutils.nodes import document
from sphinx.application import Sphinx
from sphinx.util import logging
from shutil import copy2


SPHINX_LOGGER = logging.getLogger(__name__)


def add_launch_buttons(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: Dict[str, Any],
    doctree: Optional[document],
):
    """Builds a binder link and inserts it in HTML context for use in templating.

    This is a ``html-page-context`` sphinx event (see :ref:`sphinx:events`).

    :param pagename: The sphinx docname related to the page
    :param context: A dictionary of values that are given to the template engine,
        to render the page and can be modified to include custom values.
    :param doctree: A doctree when the page is created from a reST documents;
        it will be None when the page is created from an HTML template alone.

    """

    # We only need to run this if the page is a notebook
    config_theme = app.config["html_theme_options"]
    launch_buttons = config_theme.get("launch_buttons", {})
    if not launch_buttons or not _is_notebook(app, pagename):
        return

    # If we have a Jupytext markdown notebook
    # Check whether an .ipynb version exists and add a link if so
    if context["sourcename"].endswith(".md") or context["sourcename"].endswith(
        ".md.txt"
    ):
        # Figure out the folders we want
        out_dir = Path(app.outdir)
        build_dir = out_dir.parent
        ntbk_dir = build_dir.joinpath("jupyter_execute")
        sources_dir = out_dir.joinpath("_sources")
        # Paths to old and new notebooks
        path_ntbk = ntbk_dir.joinpath(pagename).with_suffix(".ipynb")
        path_new_notebook = sources_dir.joinpath(pagename).with_suffix(".ipynb")
        # Copy the notebook to `_sources` dir so it can be downloaded
        path_new_notebook.parent.mkdir(exist_ok=True, parents=True)
        copy2(path_ntbk, path_new_notebook)
        context["ipynb_source"] = pagename + ".ipynb"

    # Check if we have a non-ipynb file, but an ipynb of same name exists
    # If so, we'll use the ipynb extension instead of the text extension
    path = app.env.doc2path(pagename)
    extension = Path(path).suffix
    if extension != ".ipynb" and Path(path).with_suffix(".ipynb").exists():
        extension = ".ipynb"

    # Theme-level configuration for repository location
    repo_parts = _get_repo_parts(config_theme)
    # Check for missing branch and default to main
    if not repo_parts.get("branch"):
        repo_parts["branch"] = "main"

    # Path to the source file relative to the repository root
    book_relpath = config_theme.get("path_to_docs", "").strip("/")
    if book_relpath != "":
        book_relpath += "/"
    path_rel_repo = f"{book_relpath}{pagename}{extension}"

    # Iterate through launch buttons and generate button config for them
    launch_buttons_configs = []
    for button in launch_buttons:
        if button.get("type") == "binderhub":
            hub_url = button.get("hub_url")
            if not hub_url:
                raise ValueError(f"No `hub_url` given: {button}")
            interface = button.get("notebook_interface", "classic")

            # This will only update keys if they've been given
            repo_parts.update(_get_repo_parts(button))
            repo_url, org, repo, branch = _check_repo_parts(repo_parts)

            ui_pre = _get_notebook_interface_prefix(interface)
            url = (
                f"{hub_url}/v2/gh/{org}/{repo}/{branch}?"
                f"urlpath={ui_pre}/{path_rel_repo}"
            )
            launch_buttons_configs.append(
                {
                    "type": "button",
                    "content": button.get("content", "Binder"),
                    "title": button.get("title", "Launch on Binder"),
                    "icon": "_static/images/logo_binder.svg",
                    "url": url,
                }
            )

        if button.get("type") == "jupyterhub":
            hub_url = button.get("hub_url")
            if not hub_url:
                raise ValueError(f"No `hub_url` given: {button}")
            interface = button.get("notebook_interface", "classic")
            ui_pre = _get_notebook_interface_prefix(interface)

            # This will only update keys if they've been given
            repo_parts.update(_get_repo_parts(button))
            repo_url, org, repo, branch = _check_repo_parts(repo_parts)

            url_params = urlencode(
                dict(
                    repo=repo_url,
                    urlpath=f"{ui_pre}/{repo}/{path_rel_repo}",
                    branch=branch,
                ),
                safe="/",
            )
            url = f"{hub_url}/hub/user-redirect/git-pull?{url_params}"
            launch_buttons_configs.append(
                {
                    "type": "button",
                    "content": button.get("content", "JupyterHub"),
                    "title": button.get("title", "Launch on JupyterHub"),
                    "icon": "_static/images/logo_jupyterhub.svg",
                    "url": url,
                }
            )

        if button.get("type") == "colab":
            url = f"https://colab.research.google.com/github/{org}/{repo}/blob/{branch}/{path_rel_repo}"  # noqa
            launch_buttons_configs.append(
                {
                    "type": "button",
                    "content": "Colab",
                    "title": "Launch on Colab",
                    "icon": "_static/images/logo_colab.png",
                    "url": url,
                }
            )

        if button.get("type") == "deepnote":
            github_path = f"%2F{org}%2F{repo}%2Fblob%2F{branch}%2F{path_rel_repo}"
            url = (
                f"https://deepnote.com/launch?url=https%3A%2F%2Fgithub.com{github_path}"
            )
            launch_buttons_configs.append(
                {
                    "type": "button",
                    "content": "Deepnote",
                    "title": "Launch on Deepnote",
                    "icon": "_static/images/logo_deepnote.svg",
                    "url": url,
                }
            )

        if button.get("type") == "thebe":
            # Note that the thebe config will have already been initialized.
            launch_buttons_configs.append(
                {
                    "type": "button",
                    "content": "Interactive code",
                    "title": "Interactive code",
                    "onclick": "initThebeSBT()",
                    "icon": "fas fa-play",
                }
            )
            context["use_thebe"] = True

    # Add the dropdown to our header buttons list
    for lb in launch_buttons_configs:
        lb["tooltip_placement"] = "left"

    context["header_buttons"].append(
        {
            "type": "dropdown",
            "icon": "fas fa-rocket",
            "side": "right",
            "classes": ["launch-buttons"],
            "items": launch_buttons_configs,
        }
    )


def _split_repo_url(url):
    """Split a repository URL into an org / repo combination."""
    if "github.com/" in url:
        end = url.split("github.com/")[-1]
        org, repo = end.split("/")[:2]
    else:
        SPHINX_LOGGER.warning(
            f"Currently Binder/JupyterHub repositories must be on GitHub, got {url}"
        )
        org = repo = None
    return org, repo


def _get_repo_parts(config):
    """Return metadata about a repository based on a configuration file.

    Used to generate launch button URLs.
    """
    # Use an empty config so we only add key/vals if the val exists
    repo_parts = {}

    # Repository URL is used to infer the org/repo
    repo_url = config.get("repository_url")

    # Check to make sure that the URL is properly formed
    if repo_url:
        repo_parts["url"] = repo_url
        org, repo = _split_repo_url(repo_url)
        if org is None or repo is None:
            # Skip the rest because the repo_url isn't right
            SPHINX_LOGGER.warn(f"Repository URL {repo_url} is not properly structured.")
            return
        repo_parts["org"] = org
        repo_parts["repo"] = repo

    # The branch is given separately
    branch = config.get("repository_branch")
    if branch:
        repo_parts["branch"] = branch

    return repo_parts


def _is_notebook(app, pagename):
    return app.env.metadata[pagename].get("kernelspec")


def _check_repo_parts(parts):
    """Check that all parts of a launch button URL are present."""
    if not parts.get("url"):
        raise ValueError(
            "You must provide the key: `repository_url` to use launch buttons."
        )
    elif not parts.get("org") or not parts.get("repo"):
        raise ValueError(
            (
                "Couldn't infer an org / repo from the repo url. "
                f"Check it is correct: {parts}"
            )
        )
    elif not parts.get("branch"):
        raise ValueError("No branch specified for launch buttons.")

    return parts.get("url"), parts.get("org"), parts.get("repo"), parts.get("branch")


def _get_notebook_interface_prefix(interface):
    """Generate the correct URL prefix for a Binder/Hub URL given an interface."""
    # Construct the extra URL parts (app and relative path)
    notebook_interface_prefixes = {"classic": "tree", "jupyterlab": "lab/tree"}
    if interface not in notebook_interface_prefixes:
        raise ValueError(
            (
                "Notebook UI for Binder/JupyterHub links must be one"
                f"of {tuple(notebook_interface_prefixes.keys())},"
                f"not {interface}"
            )
        )
    ui_pre = notebook_interface_prefixes[interface]
    return ui_pre


def update_launch_button_config(app):
    """If a thebe launch button is specified, activate thebe and add configuration."""
    theme_options = app.env.config.html_theme_options
    launch_buttons = theme_options.get("launch_buttons", [])

    # DEPRECATE after 0.5
    # Old versions had people give dictionary to configure launch buttons
    # New versions use a list of launch button configuration
    # So we check for the old-style dictionary and convert it to new style
    if isinstance(launch_buttons, dict):
        SPHINX_LOGGER.warn(
            "Launch buttons are now configured with a list of buttons, rather than a dictionary. Dictionary config will be deprecated in v0.5"  # noqa
        )
        launch_buttons_new = []
        for kind, url in launch_buttons.items():
            if kind == "thebe":
                url = theme_options.get("repository_url")

            # Convert the type:url dict into a generic key:val dict we use later
            launch_buttons_new.append(
                {"type": kind.split("_")[0], "url": url.strip("/")}
            )
        theme_options["launch_buttons"] = launch_buttons = launch_buttons_new

    # If any of our launch buttons adds thebe, configure sphinx-thebe here
    for button in launch_buttons:
        # If the button isn't a thebe type, we have nothing to do
        if not button["type"] == "thebe":
            continue

        # Make sure the sphinx-thebe extension is activated
        app.setup_extension("sphinx_thebe")

        # This is either the default values or will have config if the user defined it
        thebe_config = app.env.config.thebe_config

        # Update the thebe config with values given in theme options or button config
        thebe_config["repository_url"] = theme_options.get("repository_url")
        if button.get("repository_url"):
            thebe_config["repository_url"] = button.get("repository_url")

        branch = theme_options.get("repository_url")
        if button.get("repository_branch"):
            branch = button.get("repository_branch")
        if not branch:
            # Explicitly check in case branch is ""
            SPHINX_LOGGER.warn("No thebe branch specified. Using 'main'.")
            branch = "main"
        thebe_config["repository_branch"] = branch

        # Update the thebe_config with the new values
        app.env.config.thebe_config = thebe_config
