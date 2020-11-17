---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.8'
    jupytext_version: 1.4.2
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Configuration and page elements

There are a number of ways to configure `sphinx-book-theme`. This page covers some of the main ways
to do so. It also serves as a reference to make sure that visual elements look correct

## Sidebars

There are two different kinds of sidebar-like content in `sphinx-book-theme`,
typical `{sidebar}` directives, as well as a theme-specific `{margin}` directive.
This section covers both. Both allow you to place extra content
separately from your main content.

```{tip}
Sidebar content will generally overlap with the white space where your site's
table of contents lives. When the reader scrolls sidebar content into view, the
right TOC should hide itself automatically.
```

### Margins

You can specify content that should exist in the right margin. This will behave
like a regular sidebar until the screen hits a certain width, at which point this
content will "pop out" to the right white space. To add margin content, use this syntax:

````
```{margin} **My margin title**
Here is my margin content, it is pretty cool!
```
````

```{margin} **Here is my margin content**
It is pretty cool!
```

### Content sidebars

Content sidebars exist in-line with your text, but allow the rest of the
page to flow around them, rather than moving to the right margin.
To add content sidebars, use this syntax:

````
```{sidebar} **My sidebar title**
Here is my sidebar content, it is pretty cool!
```
````

Note how the content wraps around the sidebar to the right.
However, the sidebar text will still be in line with your content. There are
certain kinds of elements, such as "note" blocks and code cells, that may
clash with your sidebar. If this happens, try using a `{margin}` instead.


````{sidebar} **My sidebar title**
```{note}
Here is my sidebar content, it is pretty cool!
```
![](images/cool.jpg)
````


### Adding content to margins and sidebars

Sidebar/margin content can include all kinds of things, such as code blocks:

````{margin} Code blocks in margins
```python
print("here is some python")
```
````

`````
````{margin} Code blocks in margins
```python
print("here is some python")
```
````
`````

as well as admonitions and images:

````{margin} **Notes in margins**
```{note}
Wow, a note with an image in a margin!
![](images/cool.jpg)
```
````

`````
````{margin} **Notes in margins**
```{note}
Wow, a note with an image in a margin!
![](images/cool.jpg)
```
````
`````

### Margin figure captions

There are a few theme-specific figure configurations. Here is a figure with
a caption to the right.

```{figure} images/cool.jpg
---
width: 60%
figclass: margin-caption
alt: My figure text
name: myfig5
---
And here is my figure caption
```

We can reference the figure with {ref}`myfig5`. Or a numbered reference like
{numref}`myfig5`.

And here is a figure with a caption below. We'll add a note below to create
some vertical space to see better.

```{figure} images/cool.jpg
---
figclass: margin
alt: My figure text
name: myfig4
---
And here is my figure caption
```

We can reference the figure with {ref}`myfig4`. Or a numbered reference like
{numref}`myfig4`.

## Full-width content

Full-width content extends into the right margin, making it stand out against
the rest of your book's content. To add full-width content to your page, add the
class `full-width` to any of the elements in your documentation. For example, you can
add a `full-width` tag to a note element like this:

````
```{note}
:class: full-width
This content will be full-width
```
````

This code results in the following output:

```{note}
:class: full-width
This content will be full-width
```

```{margin} A note for ipynb users
If you are using a Jupyter Notebook as inputs to your documentation using the
[MyST-NB extension](https://myst-nb.readthedocs.io/en/latest/), you can trigger
this behavior with a code cell by adding a `full-width` tag to the cell.
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

## Formatting code cells

### Scrolling cell outputs

The traditional Jupyter Notebook interface allows you to toggle **output scrolling**
for your cells. This allows you to visualize part of a long output without it taking up
the entire page.

You can trigger this behavior in Jupyter Book by adding the following
tag to a cell's metadata:

```json
{
    "tags": [
        "scroll-output",
    ]
}
```

For example, the following cell has a long output, but will be scrollable in the book:

```{code-cell} ipython3
:tags: [output_scroll]
for ii in range(40):
    print(f"this is output line {ii}")
```

### Scrolling cell inputs

If your input code is long and takes up a lot of your page, you can make it scrollable
as well by adding the following tag to a cell's metadata:

```json
{
    "tags": [
        "scroll-input",
    ]
}
```

For example, the following cell has a long input, but will be scrollable in the book:

```{code-cell} ipython3
:tags: [scroll-input]
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
b = "This line has no meaning"
print(b)
```
