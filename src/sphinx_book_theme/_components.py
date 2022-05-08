"""Functions to compile HTML components to be placed on a page.

These are meant to be used by Jinja templates via the Sphinx HTML context.

A dictionary defines the components that are available to the theme.
Keys of this dictionary should be the `"type"` values that users provide in
their configuration.
The remaining values in the user configuration are passed as kwargs to the func.
"""
from sphinx.util import logging

SPHINX_LOGGER = logging.getLogger(__name__)


# Add functions to render header components
def component_text(app, context, content="", url="", classes=[]):
    classes = " ".join(classes)
    html = f"<span class='component-text {classes}'>{content}</span>"
    if url:
        html = f'<a href="{url}" class="link-primary">{html}</a>'
    return html


def component_button(app, context, content="", url="", onclick="", classes=[]):
    if url and onclick:
        raise Exception("Button component cannot have both url and onclick specified.")
    classes = " ".join(classes)
    if onclick:
        onclick = ' onclick="{onclick}"'

    classes = " ".join(classes)
    html = f"""
    <button class="btn btn-outline-primary {classes}"{onclick} type="button">
        {content}
    </button>
    """
    if url:
        html = f'<a href="{url}">{html}</a>'

    return html


def component_image(app, context, src="", url="", classes=[]):
    if not src.startswith("http"):
        src = context["pathto"](src, 1)
    html = f"""
    <img src={src}>
    """
    if url:
        html = f"<a href={url}>{html}</a>"
    return html


def component_html(app, context, html=""):
    return html


def component_dropdown(app, context, content="", items=[]):
    dropdown_items = []
    for component in items:
        link = f"""
        <a href="{component['url']}" class="dropdown-item">{component['content']}</a>
        """
        dropdown_items.append(link)
    dropdown_items = "\n".join(dropdown_items)
    html = f"""
    <div class="dropdown">
        <button class="btn dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            {content}
        </button>
        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
            {dropdown_items}
        </div>
    </div>
    """  # noqa
    return html


def component_icon_links(app, context, icons, classes=[]):
    context = {"theme_icon_links": icons}
    # Add the pydata theme icon-links macro as a function we can re-use
    return app.builder.templates.render("icon-links.html", context)


COMPONENT_FUNCS = {
    "text": component_text,
    "button": component_button,
    "html": component_html,
    "image": component_image,
    "icon-links": component_icon_links,
    "dropdown": component_dropdown,
}
