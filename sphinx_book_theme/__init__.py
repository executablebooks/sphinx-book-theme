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

__version__ = "0.1.9"
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

    # Ensure that the max TOC level is an integer
    context["theme_show_toc_level"] = int(context.get("theme_show_toc_level", 1))

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


def add_toctree_functions(app, pagename, templatename, context, doctree):
    """Add functions so Jinja templates can add toctree objects."""

    def generate_toc_html(kind="html"):
        """Return the within-page TOC links in HTML."""

        if "toc" not in context:
            return ""

        soup = bs(context["toc"], "html.parser")

        # Add toc-hN + visible classes
        def add_header_level_recursive(ul, level):
            if ul is None:
                return
            if level <= (context["theme_show_toc_level"] + 1):
                ul["class"] = ul.get("class", []) + ["visible"]
            for li in ul("li", recursive=False):
                li["class"] = li.get("class", []) + [f"toc-h{level}"]
                add_header_level_recursive(li.find("ul", recursive=False), level + 1)

        add_header_level_recursive(soup.find("ul"), 1)

        # Add in CSS classes for bootstrap
        for ul in soup("ul"):
            ul["class"] = ul.get("class", []) + ["nav", "section-nav", "flex-column"]

        for li in soup("li"):
            li["class"] = li.get("class", []) + ["nav-item", "toc-entry"]
            if li.find("a"):
                a = li.find("a")
                a["class"] = a.get("class", []) + ["nav-link"]

        # If we only have one h1 header, assume it's a title
        h1_headers = soup.select(".toc-h1")
        if len(h1_headers) == 1:
            title = h1_headers[0]
            # If we have no sub-headers of a title then we won't have a TOC
            if not title.select(".toc-h2"):
                out = ""
            else:
                out = title.find("ul").prettify()
        # Else treat the h1 headers as sections
        else:
            out = soup.prettify()

        # Return the toctree object
        if kind == "html":
            return out
        else:
            return soup

    def navbar_align_class():
        """Return the class that aligns the navbar based on config."""
        align = context.get("theme_navbar_align", "content")
        align_options = {
            "content": ("col-lg-9", "mr-auto"),
            "left": ("", "mr-auto"),
            "right": ("", "ml-auto"),
        }
        if align not in align_options:
            raise ValueError(
                (
                    "Theme optione navbar_align must be one of"
                    f"{align_options.keys()}, got: {align}"
                )
            )
        return align_options[align]

    def generate_google_analytics_script(id):
        """Handle the two types of google analytics id."""
        if id:
            if "G-" in id:
                script = f"""
                <script
                    async
                    src='https://www.googletagmanager.com/gtag/js?id={id}'
                ></script>
                <script>
                    window.dataLayer = window.dataLayer || [];
                    function gtag(){{ dataLayer.push(arguments); }}
                    gtag('js', new Date());
                    gtag('config', '{id}');
                </script>
                """
            else:
                script = f"""
                    <script
                        async
                        src='https://www.google-analytics.com/analytics.js'
                    ></script>
                    <script>
                        window.ga = window.ga || function () {{
                            (ga.q = ga.q || []).push(arguments) }};
                        ga.l = +new Date;
                        ga('create', '{id}', 'auto');
                        ga('set', 'anonymizeIp', true);
                        ga('send', 'pageview');
                    </script>
                """
            soup = bs(script, "html.parser")
            return soup
        else:
            return ""

    context["generate_toc_html"] = generate_toc_html
    context["navbar_align_class"] = navbar_align_class
    context["generate_google_analytics_script"] = generate_google_analytics_script


def _add_collapse_checkboxes(soup):
    # based on https://github.com/pradyunsg/furo

    toctree_checkbox_count = 0

    for element in soup.find_all("li", recursive=True):
        # We check all "li" elements, to add a "current-page" to the correct li.
        classes = element.get("class", [])

        # Nothing more to do, unless this has "children"
        if not element.find("ul"):
            continue

        # Add a class to indicate that this has children.
        element["class"] = classes + ["has-children"]

        # We're gonna add a checkbox.
        toctree_checkbox_count += 1
        checkbox_name = f"toctree-checkbox-{toctree_checkbox_count}"

        # Add the "label" for the checkbox which will get filled.
        if soup.new_tag is None:
            continue
        label = soup.new_tag("label", attrs={"for": checkbox_name})
        label.append(soup.new_tag("i", attrs={"class": "fas fa-chevron-down"}))
        element.insert(1, label)

        # Add the checkbox that's used to store expanded/collapsed state.
        checkbox = soup.new_tag(
            "input",
            attrs={
                "type": "checkbox",
                "class": ["toctree-checkbox"],
                "id": checkbox_name,
                "name": checkbox_name,
            },
        )
        # if this has a "current" class, be expanded by default
        # (by checking the checkbox)
        if "current" in classes:
            checkbox.attrs["checked"] = ""

        element.insert(1, checkbox)


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
    # app.setup_extension("sphinx_design")
    app.connect("env-before-read-docs", update_thebe_config)

    # Configuration for Juypter Book
    app.connect("html-page-context", add_hub_urls)
    app.connect("html-page-context", add_toctree_functions)
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
