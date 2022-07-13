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
    content=None,
    title=None,
    icon=None,
    image=None,
    outline=None,
    id=None,
    tooltip_placement=None,
    url=None,
    onclick=None,
    button_id=None,
    label_for=None,
    attributes={},
    classes=[],
):
    """Render a clickable button.

    There are three possible actions that will be triggered,
    corresponding to different kwargs having values.

    Meta Parameters
    ---------------
    app: An instance of sphinx.Application
    context: A Sphinx build context dictionary

    General parameters
    ------------------
    content: Content to populate inside the button.
    title: A tooltip / accessibility-friendly title.
    icon: A tiny square icon. A set of FontAwesome icon classes, or path to an image.
    image: A larger image of any aspect ratio. A path to a local or remote image.
    button_id: The ID to be added to this button.
    outline: Whether to outline the button.
    tooltip_placement: Whether the tooltip will be to the left, right, top, or bottom.
    attributes: A dictionary of any key:val attributes to add to the button.
    classes: A list of CSS classes to add to the button.

    Action-specific parameters
    --------------------------
    url: The URL to which a button will direct when clicked.
    onclick: JavaScript that will be called when a person clicks.
    label_for: The input this label should trigger when clicked (button is a label).
    """
    # Set up attributes and classes that will be used to create HTML attributes at end
    attributes = attributes.copy()
    attributes.update({"type": "button"})

    # Update classes with custom added ones
    default_classes = ["btn", "icon-button"]
    if classes:
        if isinstance(classes, str):
            classes = [classes]
    else:
        classes = []
    classes.extend(default_classes)

    # Give an outline if desired.
    if outline:
        classes.append("btn-outline")

    # Checks for proper arguments
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
        classes.append("icon-button-no-content")
    else:
        btn_content += f'<span class="btn__content-container">{content}</span>'

    if button_id:
        attributes["id"] = button_id

    # Handle tooltips if a title is given
    if title:
        title = context["translate"](title)
        tooltip_placement = "bottom" if not tooltip_placement else tooltip_placement
        attributes["data-toggle"] = "tooltip"
        attributes["aria-label"] = title
        attributes["data-placement"] = tooltip_placement
        attributes["title"] = title

    # Convert all the options for the button into a string of HTML attributes
    attributes["class"] = " ".join(classes)
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
    app, context, content="", icon="", side="left", classes=None, items=[], **kwargs
):
    # Render the items inside the dropdown
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

    # Set up the classes for the dropdown
    classes = [] if not classes else classes
    if content:
        classes.append("dropdown-toggle")

    # Unique ID to trigger the show event
    dropdown_id = "menu-dropdown-"
    dropdown_id += hashlib.md5(dropdown_items.encode("utf-8")).hexdigest()[:5]

    # Generate the dropdown button HTML
    dropdown_attributes = {
        "aria-haspopup": "true",
        "aria-expanded": "false",
        "type": "button",
    }
    if "title" in kwargs:
        SPHINX_LOGGER.warn("Cannot use title / tooltip with dropdown menu. Removing.")
        kwargs.pop("title")

    html_button = component_button(
        app,
        context,
        content=content,
        icon=icon,
        attributes=dropdown_attributes,
        classes=classes,
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
