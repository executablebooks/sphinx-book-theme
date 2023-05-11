
# Add a download page button

You can add a button allowing users to download the currently viewed page in several formats: `raw source`, `pdf` or `ipynb` if one was generated as part of the build.
To include this button, use the following configuration:

```python
html_theme_options = {
    ...
    "use_download_button": True,
    ...
}
```

```{note}
This theme over-rides the Sphinx default for `html_source_suffix` to be `''` instead of `.txt`.
This is because most users of this theme want to download source files of the pages themselves, which do not begin with `.txt`.
If you wish to add a different source suffix, manually specify `html_source_suffix` in `conf.py`.
```
