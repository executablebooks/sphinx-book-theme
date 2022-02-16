"""A lightweight book theme based on the pydata sphinx theme."""
import os
from pathlib import Path

from docutils.parsers.rst.directives.body import Sidebar
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.locale import get_translation
from sphinx.util import logging

from .launch import add_hub_urls

__version__ = "0.2.0"
"""sphinx-book-theme version"""

SPHINX_LOGGER = logging.getLogger(__name__)
MESSAGE_CATALOG_NAME = "booktheme"


def get_html_theme_path():
    """Return list of HTML theme paths."""
    parent = Path(__file__).parent.resolve()
    theme_path = parent / "theme" / "sphinx_book_theme"
    return theme_path


def add_to_context(app, pagename, templatename, context, doctree):

    # Add the site title to our context so it can be inserted into the navbar
    if not context.get("root_doc"):
        # TODO: Sphinx renamed master to root in 4.x, deprecate when we drop 3.x
        context["root_doc"] = context.get("master_doc")
    context["root_title"] = app.env.titles[context["root_doc"]].astext()

    # Update the page title because HTML makes it into the page title occasionally
    if pagename in app.env.titles:
        title = app.env.titles[pagename]
        context["pagetitle"] = title.astext()

    # Add a shortened page text to the context using the sections text
    if doctree:
        description = ""
        for section in doctree.traverse(nodes.section):
            description += section.astext().replace("\n", " ")
        description = description[:160]
        context["page_description"] = description

    # Add the author if it exists
    if app.config.author != "unknown":
        context["author"] = app.config.author

    # Add HTML context variables that the pydata theme uses that we configure elsewhere
    # For some reason the source_suffix sometimes isn't there even when doctree is
    if doctree and context.get("page_source_suffix"):
        config_theme = app.config.html_theme_options
        repo_url = config_theme.get("repository_url", "")
        # Only add the edit button if `repository_url` is given
        if repo_url:
            branch = config_theme.get("repository_branch")
            if not branch:
                # Explicitly check in cae branch is ""
                branch = "master"
            relpath = config_theme.get("path_to_docs", "")
            org, repo = repo_url.strip("/").split("/")[-2:]
            context.update(
                {
                    "github_user": org,
                    "github_repo": repo,
                    "github_version": branch,
                    "doc_path": relpath,
                }
            )
    else:
        # Disable using the button so we don't get errors
        context["theme_use_edit_page_button"] = False

    # Make sure the context values are bool
    btns = [
        "theme_use_edit_page_button",
        "theme_use_repository_button",
        "theme_use_issues_button",
        "theme_use_download_button",
        "theme_use_fullscreen_button",
    ]
    for key in btns:
        if key in context:
            context[key] = _string_or_bool(context[key])

    translation = get_translation(MESSAGE_CATALOG_NAME)
    context["translate"] = translation
    # this is set in the html_theme
    context["theme_search_bar_text"] = translation(
        context.get("theme_search_bar_text", "Search the docs ...")
    )


def update_thebe_config(app):
    """Update thebe configuration with SBT-specific values"""
    theme_options = app.env.config.html_theme_options
    if theme_options.get("launch_buttons", {}).get("thebe") is True:
        if not hasattr(app.env.config, "thebe_config"):
            SPHINX_LOGGER.warning(
                (
                    "Thebe is activated but not added to extensions list. "
                    "Add `sphinx_thebe` to your site's extensions list."
                )
            )
            return
        # Will be empty if it doesn't exist
        thebe_config = app.env.config.thebe_config
    else:
        return

    if not theme_options.get("launch_buttons", {}).get("thebe"):
        return

    # Update the repository branch and URL
    # Assume that if there's already a thebe_config, then we don't want to over-ride
    if "repository_url" not in thebe_config:
        thebe_config["repository_url"] = theme_options.get("repository_url")
    if "repository_branch" not in thebe_config:
        branch = theme_options.get("repository_branch")
        if not branch:
            # Explicitly check in case branch is ""
            branch = "master"
        thebe_config["repository_branch"] = branch

    app.env.config.thebe_config = thebe_config


def _string_or_bool(var):
    if isinstance(var, str):
        return var.lower() == "true"
    elif isinstance(var, bool):
        return var
    else:
        return var is None


class Margin(Sidebar):
    """Goes in the margin to the right of the page."""

    optional_arguments = 1
    required_arguments = 0

    def run(self):
        """Run the directive."""
        if not self.arguments:
            self.arguments = [""]
        nodes = super().run()
        nodes[0].attributes["classes"].append("margin")

        # Remove the "title" node if it is empty
        if not self.arguments:
            nodes[0].children.pop(0)
        return nodes


def setup(app: Sphinx):
    app.connect("builder-inited", update_thebe_config)

    # Configuration for Juypter Book
    app.connect("html-page-context", add_hub_urls)

    # add translations
    theme_dir = get_html_theme_path()
    locale_dir = os.path.join(theme_dir, "static", "locales")
    app.add_message_catalog(MESSAGE_CATALOG_NAME, locale_dir)

    app.add_html_theme("sphinx_book_theme", theme_dir)
    app.connect("html-page-context", add_to_context)

    app.add_directive("margin", Margin)

    # Update templates for sidebar
    app.config.templates_path.append(os.path.join(theme_dir, "components"))

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
