(customize:single-page)=
# Use a single-page version of this theme

If your documentation only has a single page, and you don't need the left
navigation bar, then you may configure `sphinx-book-theme` to run in **single page mode**
with the following configuration:

```python
html_theme_options = {
    ...
    "single_page": True
    ...
}
```
