"""A lightweight book theme based on the pydata sphinx theme."""
from pathlib import Path
import sphinx
import docutils
from pandas_sphinx_theme import setup as pandas_setup

__version__ = "0.0.1dev0"

def get_html_theme_path():
    """Return list of HTML theme paths."""
    theme_path = str(Path(__file__).parent.absolute())
    return theme_path


def add_static_path(app):
    static_path = Path(__file__).parent.joinpath("static").absolute()
    app.config.html_static_path.append(str(static_path))


# -----------------------------------------------------------------------------
# Sphinx monkeypatch for adding toctree objects into context.
# This converts the docutils nodes into a nested dictionary that Jinja can
# use in our templating.


def docutils_node_to_jinja(list_item, only_pages=False):
    """Convert a docutils node to a structure that can be read by Jinja.

    Parameters
    ----------
    list_item : docutils list_item node
        A parent item, potentially with children, corresponding to the level
        of a TocTree.
    only_pages : bool
        Only include items for full pages in the output dictionary. Exclude
        anchor links (TOC items with a URL that starts with #)

    Returns
    -------
    nav : dict
        The TocTree, converted into a dictionary with key/values that work
        within Jinja.
    """
    if not list_item.children:
        return None

    # We assume this structure of a list item:
    # <list_item>
    #     <compact_paragraph >
    #         <reference> <-- the thing we want
    reference = list_item.children[0].children[0]
    title = reference.astext()
    url = reference.attributes["refuri"]
    active = "current" in list_item.attributes["classes"]

    # If we've got an anchor link, skip it if we wish
    if only_pages and '#' in url:
        return None

    # Converting the docutils attributes into jinja-friendly objects
    nav = {}
    nav["title"] = title
    nav["url"] = url
    nav["active"] = active

    # Recursively convert children as well
    # If there are sub-pages for this list_item, there should be two children:
    # a paragraph, and a bullet_list.
    nav["children"] = []
    if len(list_item.children) > 1:
        # The `.children` of the bullet_list has the nodes of the sub-pages.
        subpage_list = list_item.children[1].children
        for sub_page in subpage_list:
            child_nav = docutils_node_to_jinja(sub_page, only_pages=only_pages)
            if child_nav is not None:
                nav["children"].append(child_nav)
    return nav


def update_page_context(self, pagename, templatename, ctx, event_arg):
    from sphinx.environment.adapters.toctree import TocTree

    def get_nav_object(maxdepth=None, collapse=True, **kwargs):
        """Return a list of nav links that can be accessed from Jinja.

        Parameters
        ----------
        maxdepth: int
            How many layers of TocTree will be returned
        collapse: bool
            Whether to only include sub-pages of the currently-active page,
            instead of sub-pages of all top-level pages of the site.
        kwargs: key/val pairs
            Passed to the `TocTree.get_toctree_for` Sphinx method
        """
        # The TocTree will contain the full site TocTree including sub-pages.
        # "collapse=True" collapses sub-pages of non-active TOC pages.
        # maxdepth controls how many TOC levels are returned
        toctree = TocTree(self.env).get_toctree_for(
            pagename, self, collapse=collapse, maxdepth=maxdepth, **kwargs
        )

        # toctree has this structure
        #   <caption>
        #   <bullet_list>
        #       <list_item classes="toctree-l1">
        #       <list_item classes="toctree-l1">
        # `list_item`s are the actual TOC links and are the only thing we want
        toc_items = [item for child in toctree.children for item in child
                     if isinstance(item, docutils.nodes.list_item)]

        # Now convert our docutils nodes into dicts that Jinja can use
        nav = [docutils_node_to_jinja(child, only_pages=True)
               for child in toc_items]
        nav = [item for item in nav if item is not None]
        return nav

    def get_page_toc_object():
        """Return a list of within-page TOC links that can be accessed from Jinja."""
        self_toc = TocTree(self.env).get_toc_for(pagename, self)

        try:
            nav = docutils_node_to_jinja(self_toc.children[0])
            return nav
        except:
            return {}

    def nav_to_html_list(nav, level=1, include_item_names=False):
        if len(nav) == 0:
            return ''
        ul = [f'<ul class="nav sidenav_l{level}">']
        # If we don't include parents, next `ul` should be the same level
        next_level = level+1 if include_item_names else level
        for child in nav:
            # If we're not rendering title names and have no children, skip
            if not (include_item_names or child['children']):
                continue
            active = 'active' if child['active'] else ''
            ul.append("  " + f'<li class="{active}">')
            # Render links for the top-level names if we wish
            if include_item_names:
                ul.append("  "*2 + f'<a href="{ child["url"] }">{ child["title"] }</a>')

            # Render HTML lists for children
            if child["children"]:
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

    ctx["get_nav_object"] = get_nav_object
    ctx["get_page_toc_object"] = get_page_toc_object
    ctx["nav_to_html_list"] = nav_to_html_list
    return None

sphinx.builders.html.StandaloneHTMLBuilder.update_page_context = update_page_context

def setup(app):
    app.connect("builder-inited", add_static_path)
    app.add_html_theme("sphinx_book_theme", get_html_theme_path())
    pandas_setup(app)
