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

# Special content blocks

There are a few content blocks that are unique to this theme.


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

-- Jo the Jovyan, *[the jupyter book docs](https://beta.jupyterbook.org)*
```
````
`````

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

### Margin content

You can specify content that should exist in the right margin. This will behave
like a regular sidebar until the screen hits a certain width, at which point this
content will "pop out" to the right white space.

There are two ways to add content to the margin: via the `{margin}` directive, and via adding CSS classes to your own content.

#### Use a `{margin}` directive to add margin content

The `{margin}` directive allows you to create margin content with your own title and content block.
It is a wrapper around the Sphinx `{sidebar}` directive, and largely does its magic via CSS classes (see below).

Here's how you can use the `{margin}` directive:

```{margin} **Here is my margin content**
It is pretty cool!
```

````
```{margin} **My margin title**
Here is my margin content, it is pretty cool!
```
````

#### Use CSS classes to add margin content

You may also directly add CSS classes to elements on your page in order to make them behave like margin content.
To do so, add the `margin` CSS class to any element on the page.
Many Sphinx directives allow you to directly add classes.
For example, here's the syntax to add a `margin` class to a `{note}` directive:

:::{note}
:class: margin
This note will be in the margin!
:::

```
:::{note}
:class: margin
This note will be in the margin!
:::
```

This works for most elements on the page, but in general this works best for "parent containers" that are the top-most element of a bundle of content.

For example, we can even put a whole figure in the margin like so:


You can also put the whole figure in the margin if you like.
Here is a figure with a caption below. We'll add a note below to create
some vertical space to see better.

```{figure} images/cool.jpg
---
figclass: margin
alt: My figure text
name: myfig4
---
And here is my figure caption
```

````
```{figure} images/cool.jpg
---
figclass: margin
alt: My figure text
name: myfig4
---
And here is my figure caption
```
````

We can reference the figure with {ref}`myfig4`. Or a numbered reference like
{numref}`myfig4`.

#### Figure captions in the margin

You can configure figures to use the margin for captions.
Here is a figure with a caption to the right.

```{figure} images/cool.jpg
---
width: 60%
figclass: margin-caption
alt: My figure text
name: myfig5
---
And here is my figure caption, if you look to the left, you can see that COOL is in big red letters. But you probably already noticed that, really I am just taking up space to see how the margin caption looks like when it is really long :-).
```

And the text that produced it:

````
```{figure} images/cool.jpg
---
width: 60%
figclass: margin-caption
alt: My figure text
name: myfig5
---
And here is my figure caption, if you look to the left, you can see that COOL is in big red letters. But you probably already noticed that, really I am just taking up space to see how the margin caption looks like when it is really long :-)
```
````

We can reference the figure with {ref}`this reference <myfig5>`. Or a numbered reference like
{numref}`myfig5`.

### Content sidebars

Content sidebars exist in-line with your text, but allow the rest of the
page to flow around them, rather than moving to the right margin.
To add content sidebars, use this syntax:

````{sidebar} **My sidebar title**
```{note}
Here is my sidebar content, it is pretty cool!
```
![](images/cool.jpg)
````

Note how the content wraps around the sidebar to the right.
However, the sidebar text will still be in line with your content. There are
certain kinds of elements, such as "note" blocks and code cells, that may
clash with your sidebar. If this happens, try using a `{margin}` instead.

````
```{sidebar} **My sidebar title**
Here is my sidebar content, it is pretty cool!
```
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

```{admonition} A note for ipynb users
If you are using a Jupyter Notebook as inputs to your documentation using the
[MyST-NB extension](https://myst-nb.readthedocs.io/en/latest/), you can trigger
this behavior with a code cell by adding a `full-width` tag to the cell.
```
