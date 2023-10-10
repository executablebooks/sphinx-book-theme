# Page footer

The page footer spans the entire width of the page, and is only visible once you scroll to the end of the article's content.

By default, it is empty and not visible.
However, there are two configuration points where you can add items to your footer:

`html_theme_options["footer_start"]` accepts a list of HTML templates that will be placed at the beginning (left on most screens) of the footer.

`html_theme_options["footer_end"]` accepts a list of HTML templates that will be placed at the end (right on most screens) of the footer.

For example, the configuration below assumes there is a template at `_templates/test.html`.
It adds the `_templates` folder to Sphinx's templates path, and adds the template to both the start and end section of the footer.

```python
templates_path = ["_templates"]
html_theme_options = {
  "footer_start": ["test.html"],
  "footer_end": ["test.html"]
}
```
