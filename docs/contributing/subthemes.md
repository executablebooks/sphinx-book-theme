# Creating sub-themes

It is possible to create sub-themes from this, in order to bring much of the same functionality but modify the style and behavior a bit.
This page has a few helpful tips for doing so.

:::{warning}
Creating sub-themes requires advanced Sphinx skills, and is not explicitly a supported feature of this theme.
There are no promises that we won't make breaking changes here, so be sure to test your sub-theme against the latest branch and / or pin your versions!!
:::

## Hashing your assets

This theme defines a function called `hash_html_assets` that can be used to create hashes for your style files, and updates the Sphinx links to include them with `?digest=`.
You can re-use this function in a sub-theme if you wish - to do so, look at the function signature of `hash_html_assets`.

For example, here's a Python snippet that reuses this function:

```python
from sphinx_book_theme import hash_assets_for_files

def hash_html_assets(app, pagename, templatename, context, doctree):
    assets = ["styles/your-css-asset.css", "scripts/your-js-asset.js"]
    STATIC_PATH = "path to your theme's static folder"
    hash_assets_for_files(assets, STATIC_PATH, context)

def setup(app):
  app.connect("html-page-context", hash_html_assets)
```

## Defining your own CSS

If you'd like to define a new CSS stylesheet for your sub-theme, make sure to import the CSS for this theme as well.
As a best practice, you should put your sub-theme's CSS stylesheet in the `STATIC_PATH/styles/` folder, similar to this theme.
Then, you can import this theme's CSS with:

```scss
@import "sphinx-book-theme.css";

// And include your own CSS below
```
