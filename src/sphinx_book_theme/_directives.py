"""A lightweight example directive to make it easy to demonstrate code / results."""
from sphinx.util.docutils import SphinxDirective
from docutils.parsers.rst import directives
from typing import List
from docutils import nodes


class ExampleDirective(SphinxDirective):
    """A directive to show source / result content blocks."""

    name = "example"
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "class": directives.class_option,
    }

    def run(self) -> List[nodes.Node]:
        content_text = "\n".join(self.content)

        # Update our content and place it in a container
        parent = nodes.container(classes=["bt-example"])

        # If we have a title, add it above the source code
        if self.arguments:
            title_container = nodes.container(classes=["bt-example__title"])
            title_container.append(nodes.paragraph(text=self.arguments[0]))
            parent.append(title_container)

        # Create the literal container, add a literal version of the content to it
        literal_container = nodes.container(classes=["bt-example__source"])
        literal_container.append(nodes.paragraph(text="Source"))
        literal_container.append(nodes.literal_block(text=content_text))
        parent.append(literal_container)

        # Now render the content inside of a specific container
        rendered_container = nodes.container(classes=["bt-example__result"])
        rendered_container.append(nodes.paragraph(text="Result"))
        self.state.nested_parse(self.content, 0, rendered_container)
        parent.append(rendered_container)

        return [parent]
