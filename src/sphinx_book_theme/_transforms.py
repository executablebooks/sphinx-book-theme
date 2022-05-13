from sphinx.transforms.post_transforms import SphinxPostTransform
from typing import Any
from docutils import nodes as docutil_nodes
from sphinx import addnodes as sphinx_nodes
from .nodes import SideNoteNode
import copy


class HandleFootnoteTransform(SphinxPostTransform):
    """Transform footnotes into side/marginnotes."""

    default_priority = 1
    formats = ("html",)

    def run(self, **kwargs: Any) -> None:
        theme_options = self.env.config.html_theme_options
        if theme_options.get("use_sidenotes", False) is False:
            return None
        # Cycle through footnote references, and move their content next to the reference
        # This lets us display the reference in the margin, or just below on narrow screens.
        for node in self.document.traverse(docutil_nodes.footnote_reference):
            parent = None
            # Each footnote reference should have a single node it points to via `ids`
            for ftnode in self.document.traverse(docutil_nodes.footnote):
                # matching the footnote reference with footnote
                if (
                    len(ftnode.attributes["backrefs"])
                    and ftnode.attributes["backrefs"][0] == node.attributes["ids"][0]
                ):
                    parent = ftnode.parent
                    text = ftnode.children[1].astext()

                    sidenote = SideNoteNode()
                    para = docutil_nodes.inline()
                    label = ftnode.children[0].astext()

                    if text.startswith("{-}"):
                        # marginnotes will have content starting with {-}
                        # remove the number so it doesn't show
                        para.attributes["classes"].append("marginnote")
                        para.append(docutil_nodes.Text(text.replace("{-}", "")))

                        sidenote.attributes["names"].append(f"marginnote-role-{label}")
                    else:
                        # sidenotes are the default behavior if no {-}
                        # in this case we keep the number
                        superscript = docutil_nodes.superscript("", label)
                        para.attributes["classes"].append("sidenote")
                        para.extend([superscript, docutil_nodes.Text(text)])

                        sidenote.attributes["names"].append(f"sidenote-role-{label}")
                        sidenote.append(superscript)

                    # If the reference is nested (e.g. in an admonition), duplicate the content node
                    # And place it just before the parent container, so it works w/ margin
                    # Only show one or another depending on screen width.
                    node_parent = node.parent
                    para_dup = copy.deepcopy(para)
                    # looping to check parent node
                    while not isinstance(
                        node_parent, (docutil_nodes.section, sphinx_nodes.document)
                    ):
                        # if parent node is another container
                        if not isinstance(
                            node_parent,
                            (docutil_nodes.paragraph, docutil_nodes.footnote),
                        ):
                            node_parent.replace_self([para, node_parent])
                            para_dup.attributes["classes"].append("d-n")
                            break
                        node_parent = node_parent.parent

                    node.replace_self([sidenote, para_dup])
                    break
            if parent:
                parent.remove(ftnode)
