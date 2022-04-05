from sphinx.transforms.post_transforms import SphinxPostTransform
from typing import Any
from docutils import nodes as docutil_nodes
from .nodes import SideNoteNode


class HandleFootnoteTransform(SphinxPostTransform):

    default_priority = 1

    def apply(self, **kwargs: Any) -> None:
        theme_options = self.env.config.html_theme_options
        if "use_sidenotes" in theme_options and theme_options["use_sidenotes"] is True:
            for node in self.document.traverse(docutil_nodes.footnote_reference):
                node.attributes["classes"].append("sidenote-reference")
                sidenote = SideNoteNode()
                parent = None
                for ftnode in self.document.traverse(docutil_nodes.footnote):
                    parent = ftnode.parent
                    if (
                        len(ftnode.attributes["backrefs"])
                        and ftnode.attributes["backrefs"][0]
                        == node.attributes["ids"][0]
                    ):
                        label = ftnode.children[0].astext()
                        text = ftnode.children[1].astext()

                        superscript = docutil_nodes.superscript("", label)
                        para = docutil_nodes.inline()
                        para.attributes["classes"].append("sidenote")
                        para.extend([superscript, docutil_nodes.Text(text)])

                        sidenote.attributes["names"].append(f"sidenote-{label}")
                        sidenote.append(superscript)
                        node.replace_self([sidenote, para])
                    parent.remove(ftnode)
