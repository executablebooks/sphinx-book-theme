"""A lightweight book theme based on the pydata sphinx theme."""
from pathlib import Path
import sphinx
import docutils
from pandas_sphinx_theme import setup as pandas_setup
from myst_nb.parser import CellNode

__version__ = "0.0.1dev0"

def get_html_theme_path():
    """Return list of HTML theme paths."""
    theme_path = str(Path(__file__).parent.absolute())
    return theme_path


def add_static_path(app):
    static_path = Path(__file__).parent.joinpath("static").absolute()
    app.config.html_static_path.append(str(static_path))


def add_to_context(app, pagename, templatename, context, doctree):
    def shrink_if_sidebar():
        out = ""
        if doctree is not None:
            sidebar_elements = doctree.traverse(docutils.nodes.sidebar)
            cell_containers = list(doctree.traverse(CellNode))
            popout_tags = [cl for cell in cell_containers for cl in cell.attributes['classes'] if "tag_popout" == cl]
            if any(len(ii) > 0 for ii in [sidebar_elements, popout_tags]):
                out = "col-xl-9"
        return out


    def nav_to_html_list(nav, level=1, include_item_names=False):
        if len(nav) == 0:
            return ''
        ul = [f'<ul class="nav sidenav_l{level}">']
        # If we don't include parents, next `ul` should be the same level
        next_level = level+1 if include_item_names else level
        for child in nav:
            # If we're not rendering title names and have no children, skip
            if (child is None) or not (include_item_names or child['children']):
                continue
            active = 'active' if child['active'] else ''
            ul.append("  " + f'<li class="{active}">')
            # Render links for the top-level names if we wish
            if include_item_names:
                ul.append("  "*2 + f'<a href="{ child["url"] }">{ child["title"] }</a>')

            # Render HTML lists for children if we're on an active section
            if active and child["children"]:
                # Always include the names of the children
                child_list = nav_to_html_list(child["children"], level=next_level, include_item_names=True)
                ul.append(child_list)
            ul.append("  " + '</li>')
        ul.append("</ul>")

        # Now add indentation for our level
        base_indent = "  " * (level - 1)
        ul = [base_indent + line for line in ul]
        ul = '\n'.join(ul)
        return ul

    context["shrink_if_sidebar"] = shrink_if_sidebar
    context["nav_to_html_list"] = nav_to_html_list


def setup(app):
    app.connect("builder-inited", add_static_path)
    app.add_html_theme("sphinx_book_theme", get_html_theme_path())
    pandas_setup(app)
    app.connect("html-page-context", add_to_context)
