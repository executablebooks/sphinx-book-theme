# Add your own CSS rules

To customize the look of your site further, you can customize your CSS stylesheets,
as described in the [ReadTheDocs Docs](https://docs.readthedocs.io/en/stable/guides/adding-custom-css.html#adding-custom-css-or-javascript-to-sphinx-documentation).

First, create a CSS file and place it in `_static/custom.css`.
An example CSS file to change the color of the top-level headers might look like this.

```css
h1 {
    color: #003B71 !important;
}
```

You also need these two lines in your `conf.py` file
```python
html_static_path = ["_static"]
html_css_files = ["custom.css"]
```
