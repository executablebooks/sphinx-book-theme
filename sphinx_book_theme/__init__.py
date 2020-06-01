"""A lightweight book theme based on the pydata sphinx theme."""
from pathlib import Path
from docutils.parsers.rst import directives
from docutils import nodes
from sphinx.util import logging
from sphinx import addnodes
import sass

from .launch import update_thebelab_context, init_thebelab_core, add_hub_urls

__version__ = "0.0.20"
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
    def nav_to_html_list(
        nav,
        level=1,
        include_item_names=False,
        with_home_page=False,
        number_sections=False,
        prev_section_numbers=None,
    ):
        # In case users give a string configuration
        if isinstance(number_sections, str):
            number_sections = number_sections.lower() == "true"
        if isinstance(with_home_page, str):
            with_home_page = with_home_page.lower() == "true"
        if prev_section_numbers is None:
            prev_section_numbers = []
        if len(nav) == 0:
            return ""

        config = app.env.config

        # Figure out the top-lever pages that need a TOC in front of them
        master_toctrees = app.env.tocs[config["master_doc"]]
        toc_captions = []
        for master_toctree in master_toctrees.traverse(addnodes.toctree):
            if master_toctree.attributes.get("caption"):
                caption = master_toctree.attributes.get("caption")
                toctree_first_page = master_toctree.attributes["entries"][0][
                    1
                ]  # Entries are (title, ref) pairs
                toc_captions.append((toctree_first_page, caption))

        # Add the master_doc page as the first item if specified
        if with_home_page:
            master_doc = config["master_doc"]
            master_doctree = app.env.get_doctree(master_doc)
            master_url = context["pathto"](master_doc)
            master_title = list(master_doctree.traverse(nodes.title))[0].astext()
            nav.insert(
                0,
                {
                    "title": master_title,
                    "url": master_url,
                    "active": pagename == master_doc,
                    "children": [],
                },
            )

        ul = [f'<ul class="nav sidenav_l{level}">']
        # If we don't include parents, next `ul` should be the same level
        ii_num = 1
        next_level = level + 1 if include_item_names else level
        for child in nav:
            # If we're not rendering title names and have no children, skip
            if (child is None) or not (include_item_names or child["children"]):
                continue

            # Add captions if so-given
            page_rel_root = find_url_relative_to_root(
                pagename, child["url"], app.srcdir
            )
            for caption_page, caption_text in toc_captions:
                if caption_page == str(page_rel_root):
                    ul.append('<li class="navbar-special">')
                    if caption:
                        # TODO: whenever pydata-sphinx-theme gets support for captions
                        #       we should just use that and remove this
                        ul.append(f'<p class="margin-caption">{caption_text}</p>')
                    ul.append("</li>")

            # Now begin rendering the links
            active = "active" if child["active"] else ""
            ul.append("  " + f'<li class="{active}">')

            # Render links for the top-level names if we wish
            if include_item_names:
                item_title = child["title"]
                if number_sections and not child["url"].startswith("http"):
                    this_section_numbers = prev_section_numbers + [ii_num]
                    number_title = ".".join(str(ii) for ii in this_section_numbers)
                    # Handle the case of top-level section numbers
                    if "." not in number_title:
                        number_title += "."
                    item_title = f"{number_title} {item_title}"
                    ii_num += 1
                else:
                    this_section_numbers = None

                if child["url"].startswith("http"):
                    # Add an external icon for external navbar links
                    item_title += '<i class="fas fa-external-link-alt"></i>'
                ul.append("  " * 2 + f'<a href="{child["url"]}">{item_title}</a>')

            # Check whether we should expand children
            if child["children"]:
                expand_sections = config.html_theme_options.get("expand_sections", [])
                if isinstance(expand_sections, str):
                    expand_sections = []
                if str(page_rel_root) in expand_sections:
                    active = True

            # Render HTML lists for children if we're on an active section
            if active and child["children"]:
                # Always include the names of the children
                child_list = nav_to_html_list(
                    child["children"],
                    level=next_level,
                    include_item_names=True,
                    number_sections=number_sections,
                    prev_section_numbers=this_section_numbers,
                )
                ul.append(child_list)
            ul.append("  " + "</li>")
        ul.append("</ul>")

        # Now add indentation for our level
        base_indent = "  " * (level - 1)
        ul = [base_indent + line for line in ul]
        ul = "\n".join(ul)
        return ul

    context["nav_to_html_list"] = nav_to_html_list

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
            branch = config_theme.get("repository_branch", "master")
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
    for key in ["theme_use_edit_page_button"]:
        if key in context:
            context[key] = _string_or_bool(context[key])


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

    # Configuration for Juypter Book
    app.connect("html-page-context", add_hub_urls)

    app.connect("builder-inited", add_static_path)

    app.add_html_theme("sphinx_book_theme", get_html_theme_path())
    app.connect("html-page-context", add_to_context)
    app.add_js_file("sphinx-book-theme.js")
    app.add_directive("margin", Margin)

    # Include Thebelab for interactive code if it's enabled
    app.connect("env-before-read-docs", init_thebelab_core)
    app.connect("doctree-resolved", update_thebelab_context)
