# Configuration and page elements

There are a number of ways to configure `sphinx-book-theme`. This page covers some of the main ways
to do so. It also serves as a reference to make sure that visual elements look correct

## Sidebar content

You can also specify content that should exist in the sidebar. This content
will be placed to the right, allowing it to exist separately from your main
content. To add sidebar content, use this syntax:

````
```{sidebar} **My sidebar title**
Here is my sidebar content, it is pretty cool!
```
````

```{sidebar} **Here is my sidebar content**
It is pretty cool!
```

### Adding content to sidebars

Sidebar content can include all kinds of things, such as code blocks:

````{sidebar} Code blocks in sidebars
```python
print("here is some python")
```
````

`````
````{sidebar} Code blocks in sidebars
```python
print("here is some python")
```
````
`````

as well as admonitions and images:

````{sidebar} **Notes in sidebars**
```{note}
Wow, a note with an image in a sidebar!
![](images/cool.jpg)
```
````

`````
````{sidebar} **Notes in sidebars**
```{note}
Wow, a note with an image in a sidebar!
![](images/cool.jpg)
```
````
`````

## Full-width content

```{note}
:class: tag_full_width
This is my test
```

Let's see what happens.

## Launch buttons with Binder and JupyterHub

You can automatically add Binder and JupyterHub links to pages that were build from
notebooks. This lets users quickly click to interact with your documentation's content.

To use either Binder or JupyterHub links, you'll first need to configure your
documentation's repository url:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}"
    ...
}
```

**To add Binder links** to your page, next add the following configuration:

```python
html_theme_options = {
    ...
    "binderhub_url": "https://{your-binderhub-url}"
    ...
}
```

**To add JupyterHub links** to your page, add the following configuration:

```python
html_theme_options = {
    ...
    "jupyterhub_url": "https://{your-binderhub-url}"
    ...
}
```

**To configure a relative path to your documentation**, add the following configuration:

```python
html_theme_options = {
    ...
    "path_to_docs" = "{path-relative-to-repo-root}"
    ...
}
```

**To control the user interface that is opened with links**, add the following configuration:

```python
html_theme_options = {
    ...
    "notebook_interface": "jupyterlab",
    ...
}
```

## Quotations and epigraphs

Here is what quotations and epigraphs look like in `sphinx-book-theme`:

A quote with no attribution:

> Here's my quote, it's pretty neat.
> I wonder how many lines I can create with
> a single stream-of-consciousness quote.
> I could try to add a list of ideas to talk about.
> I suppose I could just keep going on forever,
> but I'll stop here.

Sometimes you'd like to draw more attention to a quote. To do so, use the `{epigraph}` directive.
Below is an epigraph, click the button to the right of it to show the code that was used
to generate it:

```{epigraph}
Here's my quote, it's pretty neat.
I wonder how many lines I can create with
a single stream-of-consciousness quote.
I could try to add a list of ideas to talk about.
I suppose I could just keep going on forever,
but I'll stop here.
```

`````{toggle}
````
```{epigraph}
Here's my quote, it's pretty neat.
I wonder how many lines I can create with
a single stream-of-consciousness quote.
I could try to add a list of ideas to talk about.
I suppose I could just keep going on forever,
but I'll stop here.
```
````
`````

You can also add an attribution to epigraphs by adding a blank line,
followed by a line that starts with `--`. This will be renderered like so:

```{epigraph}
Here's my quote, it's pretty neat.
I wonder how many lines I can create with
a single stream-of-consciousness quote.
I could try to add a list of ideas to talk about.
I suppose I could just keep going on forever,
but I'll stop here.

-- Jo the Jovyan, *[the jupyter book docs](https://beta.jupyterbook.org)*
```

`````{toggle}
````
```{epigraph}
Here's my quote, it's pretty neat.
I wonder how many lines I can create with
a single stream-of-consciousness quote.
I could try to add a list of ideas to talk about.
I suppose I could just keep going on forever,
but I'll stop here.

-- Jo the Jovyan
```
````
`````

## Controlling the left table of contents

You can control some elements of the left table of contents. Here are the main features:

### Expand sections of your TOC

To make all sub-pages of the left Table of Contents expanded, add `:expand_sections:` to the
`toctree` for that section.

### Add a header to your TOC

If you'd like to add a header above a section of TOC links, use `:caption: My header text`
in your `toctree` directive for that section.

### Add a divider to your TOC

If you'd like to add a divider above a section of TOC links, use `:divider:`
in your `toctree` directive for that section.