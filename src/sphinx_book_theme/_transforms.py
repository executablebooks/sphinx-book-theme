from sphinx.transforms.post_transforms import SphinxPostTransform
from typing import Any
from docutils import nodes


class HandleFootnoteTransform(SphinxPostTransform):

    default_priority = 400

    def apply(self, **kwargs: Any) -> None:
        for node in self.document.traverse(nodes.footnote_reference):
            node.attributes["classes"].append("sidenote-reference")
            parent = None
            for ftnode in self.document.traverse(nodes.footnote):
                parent = ftnode.parent
                if ftnode.attributes["backrefs"][0] == node.attributes["ids"][0]:
                    ftnode.attributes["classes"].append("sidenote")
                    node.parent.append(ftnode.deepcopy())
            parent.remove(ftnode)
