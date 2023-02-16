# Content footer

There is a content footer that spans the width of the page, and is visibile when you scroll to the bottom of the content.

By default, the content footer has the following items:

- `author.html`: Display the author of the page, if present.
- `copyright.html`: Display copyright information about the website.
- `last-updated.html`: Display the latest date that the website was updated.
- `extra-footer.html`: A placeholder for arbitrary HTML you may add (see [](content-footer:extra-footer)).

(content-footer:extra-footer)=
## Add extra HTML to your content footer

You may add custom HTML to the content footer via `conf.py`.
This is a shortcut in case you wish to avoid defining your own HTML template.

To do so, use the `extra_footer` configuration and provide any HTML that you wish.
For example:

```python
html_theme_options = {
    ...
    "extra_footer": "<div>hi there!</div>",
}
```
