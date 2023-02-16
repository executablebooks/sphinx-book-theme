# Secondary sidebar and table of contents

The secondary sidebar contains information about the current page.
It begins at the top of the page (in the header), and extends downwards (by default, from the right side of the page).
This page describes ways to control and customize the secondary sidebar.

## Rename the in-page Table of Contents

You can rename the title of the in-page table of contents, in the right sidebar:

```python
html_theme_options = {
    "toc_title": "{your-title}"
}
```

The default value of the title is `Contents`.

## Show more levels of the in-page TOC by default

Normally only the 2nd-level headers of a page are shown in the within-page table of contents, and deeper levels are only shown when they are part of an active section (when it is scrolled on screen).

You can show deeper levels by default by using the following configuration, indicating how many levels should be displayed:

```python
html_theme_options = {
  "show_toc_level": 2
}
```

All headings up to and including the level specified will now be shown regardless of what is displayed on the page.
