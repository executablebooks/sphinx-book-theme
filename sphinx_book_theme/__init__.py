"""A lightweight book theme based on the pydata sphinx theme."""
import os
from pathlib import Path

try:
    import importlib.resources as resources
except ImportError:
    # python < 3.7
    import importlib_resources as resources

from bs4 import BeautifulSoup as bs
from docutils.parsers.rst.directives.body import Sidebar
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.locale import get_translation
from sphinx.util import logging

from .launch import add_hub_urls
from . import static as theme_static

__version__ = "0.2.0"
"""sphinx-book-theme version"""

SPHINX_LOGGER = logging.getLogger(__name__)
MESSAGE_CATALOG_NAME = "booktheme"


def get_html_theme_path():
    """Return list of HTML theme paths."""
    theme_path = os.path.abspath(Path(__file__).parent)
    return theme_path


def add_static_paths(app):
    """Ensure CSS/JS is loaded."""
    app.env.book_theme_resources_changed = False

    output_static_folder = Path(app.outdir) / "_static"
    theme_static_files = resources.contents(theme_static)

    if (
        app.config.html_theme_options.get("theme_dev_mode", False)
        and output_static_folder.exists()
    ):
        # during development, the JS/CSS may change, if this is the case,
        # we want to remove the old files and ensure that the new files are loaded
        for path in output_static_folder.glob("sphinx-book-theme*"):
            if path.name not in theme_static_files:
                app.env.book_theme_resources_changed = True
                path.unlink()
        # note sphinx treats theme css different to regular css
        # (it is specified in theme.conf), so we don't directly use app.add_css_file
        for fname in resources.contents(theme_static):
            if fname.endswith(".css"):
                if not (output_static_folder / fname).exists():
                    (output_static_folder / fname).write_bytes(
                        resources.read_binary(theme_static, fname)
                    )
                    app.env.book_theme_resources_changed = True

    # add javascript
    for fname in resources.contents(theme_static):
        if fname.endswith(".js"):
            app.add_js_file(fname)


def update_all(app, env):
    """During development, if CSS/JS has changed, all files should be re-written,
    to load the correct resources.
    """
    if (
        app.config.html_theme_options.get("theme_dev_mode", False)
        and env.book_theme_resources_changed
    ):
        return list(env.all_docs.keys())


def add_to_context(app, pagename, templatename, context, doctree):

    # TODO: remove this whenever the nav collapsing functionality is in the PST
    def sbt_generate_nav_html(
        level=1,
        include_item_names=False,
        with_home_page=False,
        prev_section_numbers=None,
        show_depth=1,
    ):
        # Config stuff
        config = app.env.config
        if isinstance(with_home_page, str):
            with_home_page = with_home_page.lower() == "true"

        # Convert the pydata toctree html to beautifulsoup
        toctree = context["generate_nav_html"](
            startdepth=level - 1,
            kind="sidebar",
            maxdepth=4,
            collapse=False,
            includehidden=True,
            titles_only=True,
        )
        toctree = bs(toctree, "html.parser")

        # Add the master_doc page as the first item if specified
        if with_home_page:
            # Pull metadata about the master doc
            master_doc = config["master_doc"]
            master_doctree = app.env.get_doctree(master_doc)
            master_url = context["pathto"](master_doc)
            master_title = list(master_doctree.traverse(nodes.title))
            if len(master_title) == 0:
                raise ValueError(f"Landing page missing a title: {master_doc}")
            master_title = master_title[0].astext()
            li_class = "toctree-l1"
            if context["pagename"] == master_doc:
                li_class += " current"
            # Insert it into our toctree
            ul_home = bs(
                f"""
            <ul class="nav bd-sidenav">
                <li class="{li_class}">
                    <a href="{master_url}" class="reference internal">{master_title}</a>
                </li>
            </ul>""",
                "html.parser",
            )
            toctree.insert(0, ul_home("ul")[0])

        # Open the navbar to the proper depth
        for ii in range(int(show_depth)):
            for checkbox in toctree.select(
                f"li.toctree-l{ii} > input.toctree-checkbox"
            ):
                checkbox.attrs["checked"] = None

        return toctree.prettify()

    context["sbt_generate_nav_html"] = sbt_generate_nav_html

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


def update_thebe_config(app, env, docnames):
    """Update thebe configuration with SBT-specific values"""
    theme_options = env.config.html_theme_options
    if theme_options.get("launch_buttons", {}).get("thebe") is True:
        if not hasattr(env.config, "thebe_config"):
            SPHINX_LOGGER.warning(
                (
                    "Thebe is activated but not added to extensions list. "
                    "Add `sphinx_thebe` to your site's extensions list."
                )
            )
            return
        # Will be empty if it doesn't exist
        thebe_config = env.config.thebe_config
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

    # Update the selectors to find thebe-enabled cells
    selector = thebe_config.get("selector", "") + ",.cell"
    thebe_config["selector"] = selector.lstrip(",")

    selector_input = (
        thebe_config.get("selector_input", "") + ",.cell_input div.highlight"
    )
    thebe_config["selector_input"] = selector_input.lstrip(",")

    selector_output = thebe_config.get("selector_output", "") + ",.cell_output"
    thebe_config["selector_output"] = selector_output.lstrip(",")

    env.config.thebe_config = thebe_config


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
    app.connect("env-before-read-docs", update_thebe_config)

    # Configuration for Juypter Book
    app.connect("html-page-context", add_hub_urls)

    app.connect("builder-inited", add_static_paths)
    app.connect("env-updated", update_all)

    # add translations
    package_dir = os.path.abspath(os.path.dirname(__file__))
    locale_dir = os.path.join(package_dir, "translations", "locales")
    app.add_message_catalog(MESSAGE_CATALOG_NAME, locale_dir)

    app.add_html_theme("sphinx_book_theme", get_html_theme_path())
    app.connect("html-page-context", add_to_context)

    app.add_directive("margin", Margin)

    # Update templates for sidebar
    app.config.templates_path.append(os.path.join(package_dir, "_templates"))

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
