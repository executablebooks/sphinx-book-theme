# Customize the secondary sidebar

The secondary sidebar contains information about the current page.
It begins at the top of the page (in the topbar), and extends downwards (by default, from the right side of the page).
This page describes ways to control and customize the secondary sidebar.

## Rename the in-page Table of Contents

You can rename the title of the in-page table of contents, in the right sidebar:

```python
html_theme_options = {
    "toc_title": "{your-title}"
}
```

The default value of the title is `Contents`.
