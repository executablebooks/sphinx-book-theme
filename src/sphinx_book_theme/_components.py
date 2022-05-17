"""Functions to compile HTML components to be placed on a page.

These are meant to be used by Jinja templates via the Sphinx HTML context.

A dictionary defines the components that are available to the theme.
Keys of this dictionary should be the `"type"` values that users provide in
their configuration.
The remaining values in the user configuration are passed as kwargs to the func.
"""
from sphinx.util import logging
import hashlib

SPHINX_LOGGER = logging.getLogger(__name__)


def component_button(
    app,
    context,
    content="",
    title="",
    icon="",
    image="",
    url="",
    onclick="",
    button_id="",
    label_for="",
    id="",
    tooltip_placement="",
    attributes={},
    classes=[],
):
    attributes = attributes.copy()
    attributes.update({"type": "button", "class": ["btn", "icon-button"]})
    attributes["class"].extend(classes.copy())
    btn_content = ""
    if url and onclick:
        raise Exception("Button component cannot have both url and onclick specified.")

    if not (icon or content or image):
        raise Exception("Button must have either icon, content, or image specified.")

    if onclick:
        attributes["onclick"] = onclick

    if id:
        attributes["id"] = id

    if icon:
        if icon.startswith("fa"):
            icon = f'<i class="{icon}"></i>'
        else:
            if not icon.startswith("http"):
                icon = context["pathto"](icon, 1)
            icon = f'<img src="{icon}">'
        btn_content += f'<span class="btn__icon-container">{icon}</span>'

    if image:
        if not image.startswith("http"):
            image = context["pathto"](image, 1)
        btn_content += f"""
        <span class="btn__image-container"><img src="{image}" /></span>
        """

    if not content:
        attributes["class"].append("icon-button-no-content")
    else:
        btn_content += content

    if button_id:
        attributes["id"] = button_id

    attributes["aria-label"] = title

    # Handle tooltips
    title = context["translate"](title)
    tooltip_placement = "bottom" if not tooltip_placement else tooltip_placement

    # If we're already using data-toggle, wrap the button content in a span.
    # This lets us use another data-toggle.
    if "data-toggle" in attributes:
        btn_content = f"""
        <span data-toggle="tooltip" data-placement="{tooltip_placement}" title="{title}">
            {btn_content}
        </span>
        """  # noqa
    else:
        attributes["data-placement"] = tooltip_placement
        attributes["title"] = title

    # Convert all the options for the button into a string of HTML attributes
    attributes["class"] = " ".join(attributes["class"])
    attributes_str = " ".join([f'{key}="{val}"' for key, val in attributes.items()])

    # Generate the button HTML
    if label_for:
        html = f"""
        <label for="{label_for}" {attributes_str}>
            {btn_content}
        </label>
        """
    else:
        html = f"""
        <button {attributes_str}>
            {btn_content}
        </button>
        """

    # Wrap the whole thing in a link if one is specified
    if url:
        # If it doesn't look like a web URL, assume it's a local page
        if not url.startswith("http"):
            url = context["pathto"](url)
        html = f'<a href="{url}">{html}</a>'

    return html


def component_group(app, context, items=None, **kwargs):
    # Items to go inside dropdown
    group_items = []
    for component in items:
        # Pop the `button` type in case it was incorrectly given, since we force button
        if "type" in component:
            component.pop("type")
        group_items.append(
            component_button(
                app,
                context,
                **component,
            )
        )
    group_items = "\n".join(group_items)
    html = f"""
    <div class="component-group">{group_items}</div>
    """
    return html


def component_dropdown(
    app, context, content="", icon="", side="left", items=[], **kwargs
):
    # Items to go inside dropdown
    dropdown_items = []
    for component in items:
        # Pop the `button` type in case it was incorrectly given, since we force button
        if "type" in component:
            component.pop("type")
        dropdown_items.append(
            component_button(
                app,
                context,
                **component,
            )
        )
    dropdown_items = "\n".join(dropdown_items)

    # These control the look of the button
    button_classes = []
    if content:
        button_classes.append("dropdown-toggle")

    # Unique ID to trigger the show event
    dropdown_id = "menu-dropdown-"
    dropdown_id += hashlib.md5(dropdown_items.encode("utf-8")).hexdigest()[:5]

    # Generate the button HTML
    dropdown_attributes = {
        "data-toggle": "dropdown",
        "aria-haspopup": "true",
        "aria-expanded": "false",
        "type": "button",
    }
    html_button = component_button(
        app,
        context,
        content=content,
        icon=icon,
        attributes=dropdown_attributes,
        classes=button_classes,
        button_id=dropdown_id,
        **kwargs,
    )

    dropdown_classes = ["dropdown-menu"]
    if side == "right":
        dropdown_classes.append("dropdown-menu-right")
    dropdown_classes = " ".join(dropdown_classes)

    html_dropdown = f"""
    <div class="dropdown">
        {html_button}
        <div class="{dropdown_classes}" aria-labelledby="{dropdown_id}">
            {dropdown_items}
        </div>
    </div>
    """  # noqa
    return html_dropdown


def component_html(app, context, html=""):
    return html


COMPONENT_FUNCS = {
    "button": component_button,
    "dropdown": component_dropdown,
    "group": component_group,
    "html": component_html,
}
