from docutils import nodes
from sphinx.application import Sphinx
from typing import Any, cast
from sphinx.writers.latex import LaTeXTranslator


class SideNoteNode(nodes.Element):
    """A node that will not be rendered."""

    def __init__(self, rawsource="", *children, **attributes):
        super().__init__("", **attributes)

    @classmethod
    def add_node(cls, app: Sphinx) -> None:
        add_node = cast(Any, app.add_node)  # has the wrong typing for sphinx<4
        add_node(
            cls,
            override=True,
            html=(visit_SideNoteNode, depart_SideNoteNode),
            latex=(visit_SideNoteNode, depart_SideNoteNode),
        )


def visit_SideNoteNode(self, node):
    if isinstance(self, LaTeXTranslator):
        pass
    else:
        tagid = node.attributes["names"][0]
        self.body.append(f"<label for='{tagid}' class='margin-toggle'>")
        self.body.append(self.starttag(node, "span"))


def depart_SideNoteNode(self, node):
    if isinstance(self, LaTeXTranslator):
        pass
    else:
        tagid = node.attributes["names"][0]
        self.body.append("</span>\n\n")
        self.body.append("</label>")
        self.body.append(
            f"<input type='checkbox' id='{tagid}' name='{tagid}' class='margin-toggle'>"
        )
