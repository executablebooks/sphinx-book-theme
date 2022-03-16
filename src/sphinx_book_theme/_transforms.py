from sphinx.transforms.post_transforms import SphinxPostTransform
from typing import Any
from docutils import nodes as docutil_nodes
from .nodes import SideNoteNode


class HandleFootnoteTransform(SphinxPostTransform):

    default_priority = 1

    def apply(self, **kwargs: Any) -> None:
        theme_options = self.env.config.html_theme_options
        if theme_options.get("use_sidenotes", False) is True:
            for node in self.document.traverse(docutil_nodes.footnote_reference):
                parent = None
                for ftnode in self.document.traverse(docutil_nodes.footnote):
                    # matching the footnote reference with footnote
                    if (
                        len(ftnode.attributes["backrefs"])
                        and ftnode.attributes["backrefs"][0]
                        == node.attributes["ids"][0]
                    ):
                        parent = ftnode.parent
                        text = ftnode.children[1].astext()

                        sidenote = SideNoteNode()
                        para = docutil_nodes.inline()
                        if text.startswith("{-}"):
                            # marginnotes
                            para.attributes["classes"].append("marginnote")
                            para.append(docutil_nodes.Text(text.replace("{-}", "")))

                            sidenote.attributes["names"].append("marginnote-role")
                        else:
                            # sidenotes
                            label = ftnode.children[0].astext()

                            superscript = docutil_nodes.superscript("", label)
                            para.attributes["classes"].append("sidenote")
                            para.extend([superscript, docutil_nodes.Text(text)])

                            sidenote.attributes["names"].append(
                                f"sidenote-role-{label}"
                            )
                            sidenote.append(superscript)
                        node.replace_self([sidenote, para])
                        break
                if parent:
                    parent.remove(ftnode)
