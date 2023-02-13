# Header content

By default, this theme does not contain any header content, it only has a sidebar and a main content window.
However, you may [use the PyData Sphinx Theme's header configuraiton](https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html#header-navigation-bar) to add your own header components.
If any of this configuration is set, then your header will show at the top of the page.

For example, you can add a button to the header like so:

**Create a HTML template**. In `_templates/mybutton.html`, put the following text:

```html
<button>My test button</button>
```

Make sure that `_templates` is [on your templates path](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-templates_path).

**Add the template to the navbar**. To add the component to the navbar, you can use one of three configuration options:

- `navbar_start`: Adds it to the beginning of the header.
- `navbar_center`: Adds it to the center of the header.
- `navbar_end`: Adds it to the end of hte header.

For example, to add the button to the end of your header, use this configuration:

```python
html_theme_options = {
  "navbar_end": ["mybutton.html"]
}
```

:::{admonition} Override the entire header
Alternatively, you can over-ride the entire header by defining a file at `_templates/sections/header.html`.
:::

## Style the header

Note that the header has very little styling applied to it by default.
So you should [add custom styles to the theme](custom-css.md) in order to achieve the look and feel you want.
