"""A lightweight book theme based on the pydata sphinx theme."""
from pathlib import Path
import docutils
from myst_nb.parser import CellNode
from docutils.parsers.rst import directives
from sphinx.util import logging
from sphinx.directives.other import TocTree
from sphinx.util.nodes import explicit_title_re
import sass

__version__ = "0.0.1dev0"
SPHINX_LOGGER = logging.getLogger(__name__)
EXTRA_TOC_OPTIONS = {
    "expand_sections": directives.flag,
    "caption": directives.unchanged_required,
    "divider": directives.flag,
}


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
    def shrink_if_sidebar():
        out = ""
        if doctree is not None:
            sidebar_elements = doctree.traverse(docutils.nodes.sidebar)
            cell_containers = list(doctree.traverse(CellNode))
            popout_tags = [
                cl
                for cell in cell_containers
                for cl in cell.attributes["classes"]
                if "tag_popout" == cl
            ]
            if any(len(ii) > 0 for ii in [sidebar_elements, popout_tags]):
                out = "col-xl-9"
        return out

    def nav_to_html_list(nav, level=1, include_item_names=False):
        if len(nav) == 0:
            return ""
        # Lists of pages where we want to trigger extra TOC behavior
        extra_toc = app.env.jb_extra_toc_info
        # And a function we'll use to parse it
        def lookup_extra_toc(pagename, extra_toc_list, kind="parent"):
            for first_child_page, parent_page, val in extra_toc_list:
                lookup_page = first_child_page if kind == "child" else parent_page
                # Check whether we have an explicit title given and pull the path if so
                explicit = explicit_title_re.match(lookup_page)
                if explicit:
                    lookup_page = explicit.group(2)
                if str(pagename) == lookup_page:
                    return val

        ul = [f'<ul class="nav sidenav_l{level}">']
        # If we don't include parents, next `ul` should be the same level
        next_level = level + 1 if include_item_names else level
        for child in nav:
            # If we're not rendering title names and have no children, skip
            if (child is None) or not (include_item_names or child["children"]):
                continue

            # Add captions and dividers if so-given
            page_rel_root = find_url_relative_to_root(
                pagename, child["url"], app.srcdir
            )
            divider = lookup_extra_toc(page_rel_root, extra_toc["divider"], "child")
            caption = lookup_extra_toc(page_rel_root, extra_toc["caption"], "child")
            if any((divider, caption)):
                ul.append('<li class="sidebar-special">')
                if divider:
                    ul.append("<hr />")
                if caption:
                    # TODO: whenever pydata-sphinx-theme gets support for captions, we should just use that and remove this
                    ul.append(f'<p class="sidebar-caption">{caption}</p>')
                ul.append("</li>")

            # Now begin rendering the links
            active = "active" if child["active"] else ""
            ul.append("  " + f'<li class="{active}">')
            # Render links for the top-level names if we wish
            if include_item_names:
                ul.append(
                    "  " * 2 + f'<a href="{ child["url"] }">{ child["title"] }</a>'
                )

            # Check whether we should expand children if it was given in the toctree
            if child["children"]:
                is_expanded = lookup_extra_toc(
                    page_rel_root, extra_toc["expand_sections"], kind="parent"
                )
                if is_expanded:
                    active = True

            # Render HTML lists for children if we're on an active section
            if active and child["children"]:
                # Always include the names of the children
                child_list = nav_to_html_list(
                    child["children"], level=next_level, include_item_names=True
                )
                ul.append(child_list)
            ul.append("  " + "</li>")
        ul.append("</ul>")

        # Now add indentation for our level
        base_indent = "  " * (level - 1)
        ul = [base_indent + line for line in ul]
        ul = "\n".join(ul)
        return ul

    context["shrink_if_sidebar"] = shrink_if_sidebar
    context["nav_to_html_list"] = nav_to_html_list


def add_binder_url(app, pagename, templatename, context, doctree):
    """Builds a binder link and inserts it in HTML context for use in templating."""

    NTBK_EXTENSIONS = [".ipynb"]

    config = app.config["html_theme_options"].get("binder_config", {})

    if not config.get("use_binder_button"):
        return

    for key in ["binderhub_url", "repository_url"]:
        if not config.get(key):
            raise ValueError(f"You must provide the key: {key} to add Binder buttons.")

    hub_url = config["binderhub_url"]
    book_relpath = config["path_to_docs"].strip("/")
    repo_url = config["repository_url"]

    if "github.com" in repo_url:
        end = repo_url.split("github.com/")[-1]
        org, repo = end.split("/")[:2]
    else:
        SPHINX_LOGGER.warning(f"Repo URL will not work with Binder links: {repo_url}")

    path = app.env.doc2path(pagename)
    extension = Path(path).suffix

    if hub_url and extension in NTBK_EXTENSIONS:
        url = f"{hub_url}/v2/gh/{org}/{repo}/master?filepath={book_relpath}/{pagename}{extension}"
        context["binder_url"] = url


def compile_scss():
    path_css_folder = Path(__file__).parent.joinpath("static")
    scss = path_css_folder.joinpath("jupyterbook.scss")
    css = sass.compile(filename=str(scss))
    path_css_folder.joinpath("jupyterbook.css").write_text(css)


class NewTocTree(TocTree):
    newtoctree_spec = TocTree.option_spec.copy()
    newtoctree_spec.update(EXTRA_TOC_OPTIONS)
    option_spec = newtoctree_spec

    def run(self):
        # Check for special TocTree options that we'll use but must be removed
        for key in EXTRA_TOC_OPTIONS:
            if key in self.options:
                val = self.options.pop(key)
                if val is None:
                    val = True
                first_toc_page = str(Path(self.content[0]).with_suffix(""))
                parent_page = self.env.docname
                self.env.jb_extra_toc_info[key].append(
                    (first_toc_page, parent_page, val)
                )
        msg_nodes = super().run()
        return msg_nodes


def setup(app):
    compile_scss()

    # Configuration for Juypter Book
    app.connect("html-page-context", add_binder_url)

    app.connect("builder-inited", add_static_path)
    app.add_html_theme("sphinx_book_theme", get_html_theme_path())
    app.connect("html-page-context", add_to_context)
    directives.register_directive("toctree", NewTocTree)
    app.env.jb_extra_toc_info = {key: [] for key in EXTRA_TOC_OPTIONS.keys()}

    # Printing libraries
    app.add_css_file("bootstrap.min.css")
    app.add_js_file("https://printjs-4de6.kxcdn.com/print.min.js")
    app.add_js_file("print.js")