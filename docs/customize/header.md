# Header content

A header extends the interface of your documentation to provide high-level information and links for readers at the top of the page.
They are often used to provide organization-wide branding, cross-links between documentation, and links to social media and external websites.

Your header will be displayed above the sidebar and article content, but will disappear as readers scroll down.
On mobile displays, the header will be collapsed with a button to expand vertically.

## Enable and configure the header

Enable headers in your documentation by providing **a header configuration** in `conf.py`:

```python
html_theme_options = {
  "header": { <your configuration here> }
}
```

For one example, see the header configuration of this documentation, in YAML format.

````{admonition} YAML configuration for this theme's header
:class: dropdown
Below is YAML configuration for this theme's header.
It is read by `conf.py` and converted into a Python dictionary at build time.

```{literalinclude} ../_data/config-header.yml
:language: yaml
```
````

See the rest of these sections for how to add various elements to your header.

## Header sections

There are three major sections that you can control with your header:

- [`brand`](header:brand): A special section for displaying a logo or site brand.
- [`start`](header:start): Left-aligned header components.
- [`end`](header:end): Right-aligned header components.

Each section has its own configuration, which is specified via keys in the `header` configuration, like so:

```python
html_theme_options = {
  "header": {
    "brand": { <brand configuration here> },
    "start": [ <list of start section components> ],
    "end": [ <list of end section components> ],
  }
}
```

Where the values of `"start":` and `"end":` are both [lists of component configuration items](header:components).

(header:brand)=
### `brand` section

The "brand" section is another place to put your title / logo if you don't want it to be in the primary sidebar (or, a place to put a higher-level logo like an organization-wide logo).
It is centered above your sidebar, and displayed to the left on mobile.

#### Add an image logo

To add a logo image to the brand section, see this sample configuration:

```python
html_theme_options = {
  "header": {
    "brand": {
      # Specifies that the brand area will use an image logo
      "type": "link",
      # Source of the image to be used
      "image": "https://executablebooks.org/en/latest/_static/logo.svg",
      # Link for the image
      "url": "https://sphinx-book-theme.readthedocs.io",
    },
  }
}
```

#### Add brand text

To add text instead of an image, use the following configuration.
You can put arbitrary HTML in the `content` configuration:

```python
html_theme_options = {
  "header": {
    "brand": {
      # Specifies that we will use text instead of an image logo
      "type": "text",
      # Text that will be displayed
      "content": "My documentation!",
      # Link for the image
      "url": "https://sphinx-book-theme.readthedocs.io",
    },
  }
}
```

(header:start)=
### `start` section

Your header's start section will be left-aligned with your article content (when the sidebar is present).
On mobile devices, it will be hidden under a collapsible button.

To add components to your header's start section, use the following configuration:

```python
html_theme_options = {
  "header": {
    "start": [ <list of component configuration> ]
  }
}
```

(header:end)=
### `end` section


Your header's end section will be right-aligned with the page.
On mobile devices, it will be hidden under a collapsible button.

To add components to your header's end section, use the following configuration:

```python
html_theme_options = {
  "header": {
    "end": [ <list of component configuration> ]
  }
}
```

(header:components)=
## Components

Components are small UI elements that can be added to your header's sections.

Add components to the two major sections of your header ([`start`](header:start) and [`end`](header:end)) by providing **lists of component configuration**.
Each component configuration takes a **`type:`** key to specify what type of component it is, as well as a collection of **`key:val`** parameters that modify the component's behavior.

For example, the following configuration adds two link components to the "start" section of a header, in `conf.py`:

```python
html_theme_options = {
  "header": {
    "start": [
      {
        "type": "text",
        "url": "https://executablebooks.org",
        "content": "Executable Books"
      },
      {
        "type": "text",
        "url": "https://jupyterbook.org",
        "content": "Jupyter Book"
      },
    ]
  }
}
```

The rest of these sections describe the components you can use:

### Buttons

Buttons are flexible UI components that trigger various actions when clicked.
They can be links, or they can trigger arbitrary JavaScript that you provide.
Use them as call-to-action items, or as a way to trigger events on your page if you are using custom JavaScript.

Clicking a button can trigger one of two actions:

- **Link to an internal or external page**
- **Trigger a JavaScript function**

Buttons have three visual sections that you may control, that roughly follow this structure:

```html
<button>
  <button-icon><button-image><button-content>
</button>
```

- **`icon`**: A small, square icon. May be configured with **FontAwesome** icons or a path to an image (local or remove).
- **`image`**: A larger image that may be rectangular. May be configured with **FontAwesome** icons or a path to an image (local or remove).
- **`content`**: Arbitrary text (or extra HTML) to put inside the button.

To add buttons components to header sections, use the following component configuration:

```python

# Provided as a list item to `start:` or `end:`
{
  # Specifies the `button` component
  "type": "button",

  ## Controls button behavior ##
  # If provided, the button will be a link to another page.
  "url": "https://google.com",
  # If provided, clicking the button will trigger this JavaScript.
  "onclick": "SomeFunction()",

  ## Controls button style ##
  # An icon that will be displayed before the text
  # Can be a set of fontawesome classes, or a path to an image
  "icon": "fas fa-bars",
  # An image path that will be displayed before the text
  "image": "https://executablebooks.org/en/latest/_static/logo.svg",
  # The text that will be displayed inside the button.
  "content": "My button's text",
  # An optional list of classes to add
  "classes": ["one", "two"]
}
```

Note tha **url** and **onclick** cannot both be provided in the same button's configuration.

#### Button icons

There are two kinds of icons you can control with the `icon` parameter:

- **FontAwesome icons**: FontAwesome icon classes like `fas fa-arrow-right`. See [the FontAwesome documentation](https://fontawesome.com/icons) for a list of classes and icons. For example:

  ```python
  # Provided as a list item to `start:` or `end:`
  {
    # Specifies the `button` component
    "type": "button",
    "icon": "fab fa-github"
    "url": "https://github.com"
  }
  ```
- **A path to an image**: Any local image you include with your documentation.

  For example, with a remote image:

  ```python
  # Provided as a list item to `start:` or `end:`
  {
    # Specifies the `button` component
    "type": "button",
    "image": "https://executablebooks.org/en/latest/_static/logo.svg"
    "url": "https://executablebooks.org"
  }
  ```

  With a local image:

  ```python
  # Provided as a list item to `start:` or `end:`
  {
    # Specifies the `button` component
    "type": "button",
    "image": "./_static/myimage.png"
    "url": "https://executablebooks.org"
  }
  ```

Finally, if a button is configured **only with an icon**, it will have a special class `icon-button` added to it that will make it contract slightly in size and spacing.

### Dropdown menus

Dropdown menus provide a clickable button that will display a list of links.
It is a useful way to provide more links in your header without using too much horizontal space.

To add dropdown components to header sections, use the following component configuration:

```python
# Provided as a list item to `start:` or `end:`
{
  # Specifies a `dropdown` type
  "type": "dropdown",
  # Text to be displayed on the button
  "content": "EBP Projects",
  # A list of dropdown links. Each is a configuration for a button.
  "items": [
    {
      "url": "https://executablebooks.org",
      "content": "Executable Books"
    },
    {
      "url": "https://jupyterbook.org",
      "content": "Jupyter Book"
    },
  ],
  # An optional list of classes to add
  "classes": ["one", "two"]
},
```

### Groups

Groups are a way of telling the theme that several UI components should be grouped together.
They will have a wrapping container, will have less spacing between them, and will be displayed _horizontally_ on narrow screens.

For example, to group several icon buttons together use a configuration like so:

```python
# Provided as a list item to `start:` or `end:`
{
  # Specifies a `group` type
  "type": "group",
  # A list of group items. Each is a configuration for a button.
  "items": [
    {
      "icon": "fab fa-github",
      "url": "https://github.com
    },
    {
      "icon": "fab fa-twitter",
      "url": "https://twitter.com
    },
    {
      "icon": "fab fa-discourse",
      "url": "https://discourse.com
    },
  ],
  # An optional list of classes to add
  "classes": ["one", "two"]
},
```

### HTML Snippets

You may provide custom HTML snippets that are inserted into the header as-is.
These are useful to define your own components or styling.

To add raw HTML components to header sections, use the following component configuration:

```python
# Provided as a list item to `start:` or `end:`
{
  # Specifies a `html` component
  "type": "html",
  # The HTML to be inserted
  "html": "<span>My custom span</span>",
},
```

## Over-write the header entirely

Instead of using any of the above functionality, you can also provide your own raw HTML for the header.
Use it if you need to have much more flexibility and control over the header.

To do so, you must define your own Sphinx Template in a specific location.
The contents of this template will be inserted into the theme.
Here is how to do this:

- Create a templates folder in your theme's root. Assuming your documentation is in the `docs/` folder:

  ```console
  $ cd docs/
  $ mkdir _templates
  ```
- Add the `_templates/` folder to your Sphinx configuration templates:

  ```python
  templates_path = ["_templates"]
  ```
- Create the following template file and add HTML to id:

  ```console
  $ echo "<p>Some text!</p>" > _templates/sections/header.html
  ```
- Build your documentation, and you should see content of this file show up above your site.
