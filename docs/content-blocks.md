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

-- Jo the Jovyan, *[the jupyter book docs](https://jupyterbook.org)*
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

-- Jo the Jovyan, *[the jupyter book docs](https://jupyterbook.org)*
```
````
`````

(margin:sidenote)=
## Sidenotes and marginnotes

This theme has support for [Tufte-stype margin / side notes](https://edwardtufte.github.io/tufte-css/), with a UX similar to [pandoc-sidenote](https://github.com/jez/pandoc-sidenote).

Sidenotes are numbered, and behave like footnotes, except they live in the margin and don’t force the reader to jump their eye to the bottom of the page.
For example, here is a sidenote[^ex].
On narrow screens, sidenotes are hidden until a user clicks the number.
If you're on a mobile device, try clicking the sidenote number above.

[^ex]: Here's my sidenote text!

    On narrow screens, this text won't show up unless you click the superscript number!

Marginnotes are not numbered, but behave the same way as sidenotes.
On mobile devices a symbol will be displayed that will display the marginnote when clicked[^exmn].
For example, there's a marginnote in the previous sentence, and you should see a symbol show to display it on mobile screens.

[^exmn]: {-} This is a margin note. Notice there isn’t a number preceding the note.

:::{seealso}
Sidenotes and marginnotes are inline content - you cannot use block-level content inside of these notes.
If you'd like to use block-level content in the margins, see [](margin:block).
:::

### Activate sidenotes and marginnotes

The theme activates sidenotes and marginnotes by over-riding footnote syntax to instead exist in the margin.

To convert your footnotes to *instead* be sidenotes/marginnotes, use this configuration:

```python
html_theme_options = {
  ...
  "use_sidenotes": True,
  ...
}
```

This will turn your **footnotes** into **sidenotes** or **marginnotes**.

### Create a sidenote

For example, the following sentence defines a sidenote and its respective content:

```markdown
Here's my sentence and a sidenote[^sn1].

[^sn1]: And here's my sidenote content.
```

Here's my sentence and a sidenote[^sn1].

[^sn1]: And here's my sidenote content.

### Create a marginnote

Marginnotes are defined by adding `{-}` at the beginning of the content block.
For example, the following syntax defines a marginnote:

```markdown
Here's my sentence and a marginnote[^mn1].

[^mn1]: {-} And here's my marginnote content.
```

Here's my sentence and a marginnote[^mn1].

[^mn1]: {-} And here's my marginnote content.


(margin:block)=
## Block margin content with the `{margin}` directive

The `{margin}` directive allows you to create block-level margin content with an optional title.
It is a wrapper around the Sphinx `{sidebar}` directive, and largely does its magic via CSS classes (see below).

:::{seealso}
If you'd like in-line margin content with numbered references, see [](margin:sidenote).
:::

Here's how you can use the `{margin}` directive:

```{margin} **Here is my margin content**
It is pretty cool!
```

````
```{margin} **My margin title**
Here is my margin content, it is pretty cool!
```
````

## Figure captions in the margin

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

### CSS classes for custom margin content

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


### Adding content to margins and sidebars

Margin content can include all kinds of things, such as code blocks:

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


## Sidebars

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
