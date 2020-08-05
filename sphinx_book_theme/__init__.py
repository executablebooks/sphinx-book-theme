"""A lightweight book theme based on the pydata sphinx theme."""
from pathlib import Path
from docutils.parsers.rst import directives
from docutils import nodes
from sphinx.util import logging
import sass
from bs4 import BeautifulSoup as bs


from .launch import add_hub_urls

__version__ = "0.0.34"
SPHINX_LOGGER = logging.getLogger(__name__)


def get_html_theme_path():
    """Return list of HTML theme paths."""
    theme_path = str(Path(__file__).parent.absolute())
    return theme_path


def add_static_path(app):
    static_path = Path(__file__).parent.joinpath("static").absolute()
    app.config.html_static_path.append(str(static_path))


def find_url_relative_to_root(pagename, relative_page, path_docs_source):
    """Given the current page (pagename), a relative page to it (relative_page),
    and a path to the docs source, return the path to `relative_page`, but now relative
    to the docs source (since this is what keys in Sphinx tend to use).
    """
    # In this case, the relative_page is the same as the pagename
    if relative_page == "":
        relative_page = Path(Path(pagename).name)

    # Convert everything to paths for use later
    path_rel = Path(relative_page).with_suffix("")
    path_parent = Path(pagename)  # pagename is relative to docs root
    source_dir = Path(path_docs_source)
    # This should be the path to `relative_page`, relative to `pagename`
    path_rel_from_page_dir = source_dir.joinpath(
        path_parent.parent.joinpath(path_rel.parent)
    )
    path_from_page_dir = path_rel_from_page_dir.resolve()
    page_rel_root = path_from_page_dir.relative_to(source_dir).joinpath(path_rel.name)
    return page_rel_root


def add_to_context(app, pagename, templatename, context, doctree):
    def generate_nav_html(
        level=1,
        include_item_names=False,
        with_home_page=False,
        prev_section_numbers=None,
    ):
        # Config stuff
        config = app.env.config
        if isinstance(with_home_page, str):
            with_home_page = with_home_page.lower() == "true"

        # Grab the raw toctree object and structure it so we can manipulate it
        toc_sphinx = context["toctree"](
            maxdepth=-1, collapse=False, titles_only=True, includehidden=True
        )
        toctree = bs(toc_sphinx, "html.parser")

        # pair "current" with "active" since that's what we use w/ bootstrap
        for li in toctree("li", {"class": "current"}):
            li["class"].append("active")

        # Add the master_doc page as the first item if specified
        if with_home_page:
            # Pull metadata about the master doc
            master_doc = config["master_doc"]
            master_doctree = app.env.get_doctree(master_doc)
            master_url = context["pathto"](master_doc)
            master_title = list(master_doctree.traverse(nodes.title))[0].astext()

            # Insert it into our toctree
            ul_home = bs(
                f"""
            <ul>
                <li class="toctree-l1">
                    <a href="{master_url}" class="reference internal">{master_title}</a>
                </li>
            </ul>""",
                "html.parser",
            )
            toctree.insert(0, ul_home("ul")[0])

        # Add an icon for external links
        for a_ext in toctree("a", attrs={"class": ["external"]}):
            a_ext.append(
                toctree.new_tag("i", attrs={"class": ["fas", "fa-external-link-alt"]})
            )

        # Remove children of all top-level pages unless config says to expand them
        expand_sections = config.html_theme_options.get("expand_sections", [])
        if isinstance(expand_sections, str):
            expand_sections = []

        for li in toctree("li", attrs={"class": "toctree-l1"}):
            page_rel_root = find_url_relative_to_root(
                pagename, li.find("a").attrs["href"], app.srcdir
            )
            if li.find("ul"):
                do_collapse = (
                    "active" not in li.attrs["class"]
                    and str(page_rel_root) not in expand_sections
                )
                if do_collapse:
                    li.find("ul").decompose()

        # Add bootstrap classes for first `ul` items
        for ul in toctree("ul", recursive=False):
            ul.attrs["class"] = ul.attrs.get("class", []) + ["nav", "sidenav_l1"]

        return toctree.prettify()

    context["generate_nav_html"] = generate_nav_html

    def generate_toc_html():
        """Return the within-page TOC links in HTML."""

        if not context.get("toc"):
            return ""

        soup = bs(context["toc"], "html.parser")

        # Add toc-hN classes
        def add_header_level_recursive(ul, level):
            for li in ul("li", recursive=False):
                li["class"] = li.get("class", []) + [f"toc-h{level}"]
                ul = li.find("ul", recursive=False)
                if ul:
                    add_header_level_recursive(ul, level + 1)

        add_header_level_recursive(soup.find("ul"), 1)

        # Add in CSS classes for bootstrap
        for ul in soup("ul"):
            ul["class"] = ul.get("class", []) + ["nav", "section-nav", "flex-column"]
        for li in soup("li"):
            li["class"] = li.get("class", []) + ["nav-item", "toc-entry"]
            if li.find("a"):
                a = li.find("a")
                a["class"] = a.get("class", []) + ["nav-link"]

        # Keep only the sub-sections of the title (so no title is shown)
        title = soup.find("a", attrs={"href": "#"})
        if title:
            title = title.parent
            # Only show if children of the title item exist
            if title.select("ul li"):
                out = title.find("ul").prettify()
            else:
                out = ""
        else:
            out = ""
        return out

    context["generate_toc_html"] = generate_toc_html

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

    # Absolute URLs for logo if `html_baseurl` is given
    # pageurl will already be set by Sphinx if so
    if app.config.html_baseurl and app.config.html_logo:
        context["logourl"] = "/".join(
            (app.config.html_baseurl.rstrip("/"), "_static/" + context["logo"])
        )

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
    ]
    for key in btns:
        if key in context:
            context[key] = _string_or_bool(context[key])


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


def compile_scss():
    path_css_folder = Path(__file__).parent.joinpath("static")
    scss = path_css_folder.joinpath("sphinx-book-theme.scss")
    css = sass.compile(filename=str(scss))
    path_css_folder.joinpath("sphinx-book-theme.css").write_text(css)


class Margin(directives.body.Sidebar):
    """Goes in the margin to the right of the page."""

    optional_arguments = 1
    required_arguments = 0

    def run(self):
        if not self.arguments:
            self.arguments = [""]
        nodes = super().run()
        nodes[0].attributes["classes"].append("margin")

        # Remove the "title" node if it is empty
        if not self.arguments:
            nodes[0].children.pop(0)
        return nodes


def setup(app):
    compile_scss()
    app.connect("env-before-read-docs", update_thebe_config)

    # Configuration for Juypter Book
    app.connect("html-page-context", add_hub_urls)

    app.connect("builder-inited", add_static_path)

    app.add_html_theme("sphinx_book_theme", get_html_theme_path())
    app.connect("html-page-context", add_to_context)

    app.add_js_file("sphinx-book-theme.js")
    app.add_directive("margin", Margin)
