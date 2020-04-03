"""A lightweight book theme based on the pydata sphinx theme."""
from pathlib import Path
import docutils
from myst_nb.parser import CellNode
from docutils.parsers.rst import directives
from docutils import nodes
from sphinx.util import logging
from sphinx import addnodes
from sphinx.directives.other import TocTree
from sphinx.util.nodes import explicit_title_re
import sass

__version__ = "0.0.1dev0"
SPHINX_LOGGER = logging.getLogger(__name__)
EXTRA_TOC_OPTIONS = {
    "expand_sections": directives.flag,
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
    def show_if_no_sidebar():
        # By default we'll show, unless there are sidebar items
        out = "show"
        # Check for sidebar items in this doctree
        if doctree is not None:
            sidebar_elements = doctree.traverse(docutils.nodes.sidebar)
            cell_containers = list(doctree.traverse(CellNode))
            popout_tags = [
                cl
                for cell in cell_containers
                for cl in cell.attributes["classes"]
                if any(ii == cl for ii in ["tag_popout", "tag_sidebar"])
            ]
            # If we found sidebar elements, then we won't show
            if any(len(ii) > 0 for ii in [sidebar_elements, popout_tags]):
                out = ""
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

        # Figure out the top-lever pages that need a TOC in front of them
        master_toctrees = app.env.tocs[app.env.config['master_doc']]
        toc_captions = []
        for master_toctree in master_toctrees.traverse(addnodes.toctree):
            if master_toctree.attributes.get("caption"):
                caption = master_toctree.attributes.get("caption")
                toctree_first_page = master_toctree.attributes['entries'][0][1]  # Entries are (title, ref) pairs
                toc_captions.append((toctree_first_page, caption))

        ul = [f'<ul class="nav sidenav_l{level}">']
        # If we don't include parents, next `ul` should be the same level
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
                    ul.append('<li class="sidebar-special">')
                    if caption:
                        # TODO: whenever pydata-sphinx-theme gets support for captions, we should just use that and remove this
                        ul.append(f'<p class="sidebar-caption">{caption_text}</p>')
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

    context["show_if_no_sidebar"] = show_if_no_sidebar
    context["nav_to_html_list"] = nav_to_html_list


def add_hub_urls(app, pagename, templatename, context, doctree):
    """Builds a binder link and inserts it in HTML context for use in templating."""

    NTBK_EXTENSIONS = [".ipynb"]

    # First decide if we'll insert any links
    path = app.env.doc2path(pagename)
    extension = Path(path).suffix

    # If so, insert the URLs depending on the configuration
    config_theme = app.config["html_theme_options"]
    launch_buttons = config_theme.get("launch_buttons", {})
    if not launch_buttons or (extension not in NTBK_EXTENSIONS):
        return

    repo_url = config_theme.get("repository_url")
    if not repo_url:
        raise ValueError(
            f"You must provide the key: `repo_url` to add Binder/JupyterHub buttons."
        )
    if "github.com" in repo_url:
        end = repo_url.split("github.com/")[-1]
        org, repo = end.split("/")[:2]
    else:
        SPHINX_LOGGER.warning(
            f"Currently Binder/JupyterHub repositories must be on GitHub, got {repo_url}"
        )
        return

    # Construct the extra URL parts (app and relative path)
    notebook_interface_prefixes = {"classic": "tree", "jupyterlab": "lab/tree"}
    notebook_interface = launch_buttons.get("notebook_interface", "classic")
    if notebook_interface not in notebook_interface_prefixes:
        raise ValueError(
            (
                "Notebook UI for Binder/JupyterHub links must be one"
                f"of {tuple(notebook_interface_prefixes.keys())}, not {notebook_interface}"
            )
        )
    ui_pre = notebook_interface_prefixes[notebook_interface]

    # Construct a path to the file relative to the repository root
    book_relpath = config_theme.get("path_to_docs", "").strip("/")
    if book_relpath != "":
        book_relpath += "/"
    path_rel_repo = f"{book_relpath}{pagename}{extension}"

    # Now build infrastructure-specific links
    jupyterhub_url = launch_buttons.get("jupyterhub_url")
    binderhub_url = launch_buttons.get("binderhub_url")
    if binderhub_url:
        url = f"{binderhub_url}/v2/gh/{org}/{repo}/master?urlpath={ui_pre}/{path_rel_repo}"
        context["binder_url"] = url

    if jupyterhub_url:
        url = f"{jupyterhub_url}/hub/user-redirect/git-pull?repo={repo_url}&urlpath={ui_pre}/{repo}/{path_rel_repo}"
        context["jupyterhub_url"] = url


def compile_scss():
    path_css_folder = Path(__file__).parent.joinpath("static")
    scss = path_css_folder.joinpath("jupyterbook.scss")
    css = sass.compile(filename=str(scss))
    path_css_folder.joinpath("jupyterbook.css").write_text(css)


class NewTocTree(TocTree):
    """A monkey-patch of the TocTree so we can intercept extra keywords without raising Sphinx errors."""
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
    app.connect("html-page-context", add_hub_urls)

    app.connect("builder-inited", add_static_path)
    app.add_html_theme("sphinx_book_theme", get_html_theme_path())
    app.connect("html-page-context", add_to_context)
    directives.register_directive("toctree", NewTocTree)
    app.env.jb_extra_toc_info = {key: [] for key in EXTRA_TOC_OPTIONS.keys()}
