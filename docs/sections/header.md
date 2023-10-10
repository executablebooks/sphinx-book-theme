# Header and navbar

By default, this theme does not contain any header content, it only has a sidebar and a main content window.
However, you may [use the PyData Sphinx Theme's header configuraiton](https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html#header-navigation-bar) to add your own header components.
If any of this configuration is set, then your header will show at the top of the page.

## Add components to the header navbar

There are three configuration options you can use in `html_theme_options`:

**`navbar_start`**: Adds components to the beginning of the header. **Visible on all screen sizes**. Use this for adding a logo that you want to persist over time.

**`navbar_center`**: Adds components to the center of the header, or to the left if no `navbar_start` is defined. **Moved to the sizebar on mobile**. Use this for extra navigation content to external pages.

**`navbar_end`**: Adds components to the end of the header. **Moved to the sizebar on mobile**. Use this for extra social links or buttons.

## An example

For example, you can add a button to the header like so:

**Create a HTML template**. In `_templates/mybutton.html`, put the following text:

```html
<button>My test button</button>
```

Make sure that `_templates` is [on your templates path](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-templates_path).

**Add the following to `conf.py`**:

```python
html_theme_options = {
  "navbar_end": ["mybutton.html"]
}
```

Your header should now be visible, and the `mybutton.html` content should now show up in the upper-right.

:::{admonition} Override the entire header
Alternatively, you can over-ride the entire header by defining a file at `_templates/sections/header.html`.
:::

## Style the header

Note that the header has very little styling applied to it by default.
So you should [add custom styles to the theme](../components/custom-css.md) in order to achieve the look and feel you want.
