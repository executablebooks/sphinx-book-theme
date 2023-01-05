---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.8'
    jupytext_version: 1.4.1+dev
kernelspec:
  display_name: Python 3
  language: python
  name: python3

execution:
  timeout: -1
---

# Theme-specific elements

This page contains a number of reference elements to see how they look in this
theme. The information is not meant to be easy to read or understand, just browse
through and see how things look!

## Full-width elements

### Code cells

```{code-cell} ipython3
:tags: [remove_cell]

# Generate some code that we'll use later on in the page
import numpy as np
import matplotlib.pyplot as plt

square = np.random.randn(100, 100)
wide = np.random.randn(100, 1000)
```

```{code-cell} ipython3
:tags: [full_width]

## A full-width square figure
fig, ax = plt.subplots()
ax.imshow(square)
```

```{code-cell} ipython3
:tags: [full_width]

## A full-width wide figure
fig, ax = plt.subplots()
ax.imshow(wide)
```

```{code-cell} ipython3
# Now here's the same figure at regular width
fig, ax = plt.subplots()
ax.imshow(wide)
```

### Markdown

```{container} full-width

This is some markdown that should be shown at full width.

Here's the Jupyter logo:

![](https://raw.githubusercontent.com/adebar/awesome-jupyter/master/assets/logo.png)

:::{note}
Here's a full-width admonition!
:::

```

### Mathematics

\begin{equation}
  \int_0^\infty \frac{x^3}{e^x-1}\,dx = \frac{\pi^4}{15}
\end{equation}

$$
  \int_0^\infty \frac{x^3}{e^x-1}\,dx = \frac{\pi^4}{15}
$$


```{math}
:label: my_label
w_{t+1} = (1 + r_{t+1}) s(w_t) + y_{t+1}
```

Link to above: {eq}`my_label`

```{math}
:label: my_label2
w_{t+1} = (1 + r_{t+1}) s(w_t) + y_{t+1} \\
w_{t+1} = (1 + r_{t+1}) s(w_t) + y_{t+1} \\
w_{t+1} = (1 + r_{t+1}) s(w_t) + y_{t+1}
```

Link to above: {eq}`my_label2`

* $$
\mathcal{O}(f) = \{ g |
    \exists c > 0,
    \exists n_0 \in \mathbb{N}_0,
    \forall n \geq n_0
        :
    [g(n) \leq c \cdot f(n)]\}$$

A really long math equation

$$
\begin{align}
\mathrm{SetConv} \left( \{(x^{c},y^{c})\}_{c=1}^{C} \right)(x) \left( \{(x^{c},y^{c})\}_{c=1}^{C} \right)(x) \left( \{(x^{c},y^{c})\}_{c=1}^{C} \right)(x)
&= \sum_{c=1}^{C} y^{(c)} w_{\theta} \left( x - x^{(c)} \right)  \sum_{c=1}^{C} y^{(c)} w_{\theta} \left( x - x^{(c)} \right) \sum_{c=1}^{C} y^{(c)} w_{\theta} \left( x - x^{(c)} \right)\\
&= \left( y^{(c')} w_{\theta} \left( x - x^{(c')} \right) \right) + \sum_{c \neq c'}  y^{(c)} w_{\theta} \left( x - x^{(c)} \right) \\
&= 0 + \sum_{c \neq c'}  y^{(c)} w_{\theta} \left( x - x^{(c)} \right)
\end{align}
$$

Full width equations work

```{math}
:class: full-width

\begin{align}
\mathrm{SetConv} \left( \{(x^{c},y^{c})\}_{c=1}^{C} \right)(x) \left( \{(x^{c},y^{c})\}_{c=1}^{C} \right)(x) \left( \{(x^{c},y^{c})\}_{c=1}^{C} \right)(x)
&= \sum_{c=1}^{C} y^{(c)} w_{\theta} \left( x - x^{(c)} \right)  \sum_{c=1}^{C} y^{(c)} w_{\theta} \left( x - x^{(c)} \right) \sum_{c=1}^{C} y^{(c)} w_{\theta} \left( x - x^{(c)} \right)\\
&= \left( y^{(c')} w_{\theta} \left( x - x^{(c')} \right) \right) + \sum_{c \neq c'}  y^{(c)} w_{\theta} \left( x - x^{(c)} \right) \\
&= 0 + \sum_{c \neq c'}  y^{(c)} w_{\theta} \left( x - x^{(c)} \right)
\end{align}
```

+++

## Margins

+++

Margin content can include all kinds of things, such as code blocks:

````{margin} Code blocks in margins
```python
print("here is some python")
```
````

as well as admonitions and images:

````{margin} **Notes in margins**
```{note}
Wow, a note with an image in a margin!
![](../images/cool.jpg)
```
````

### Margin under lower level shouldn't have different left-alignment

````{margin} **Notes in margins**
```{note}
Wow, a note with an image in a margin!
![](../images/cool.jpg)
```
````

### Margins with toggle buttons

Here's some margin content, let's see how it interacts w/ the toggle button

```{margin} My margin
Here's my margin content
```

Here's a toggleable note:

```{note}
:class: toggle
My note
```

### Margins with full-width content

```{note}
:class: tag_fullwidth
This is my test
```

Let's see what happens

```{code-cell} ipython3
:tags: [margin]

## code cell in the margin with output
fig, ax = plt.subplots()
ax.imshow(wide)
```

````{margin}

Markdown cell with code in margin

```python
a = 2
b = 3
def aplusb(a, b):
    return a+b
```
and now r

```r
a <- 2
b <- 4
a+b
```

how does it look?

Markdown cell with images in sidebar

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />

````
+++

### More content after the margin content

This is extra content after the margins to see if cells overlap and such.
Also to make sure you can still interact with the margin content.
This is extra content after the margins to see if cells overlap and such.
Also to make sure you can still interact with the margin content.

```python
a = 2
```

This is extra content after the margins to see if cells overlap and such.
Also to make sure you can still interact with the margin content.
This is extra content after the margins to see if cells overlap and such.
Also to make sure you can still interact with the margin content.
This is extra content after the margins to see if cells overlap and such.
Also to make sure you can still interact with the margin content.

### Figures with margin captions

The `margin-caption` class should cause a figure's caption to pop out to the right.

```{figure} ../images/cool.jpg
---
width: 60%
figclass: margin-caption
alt: My figure text
name: reference-margin-fig
---
And here is my figure caption, if you look to the left, you can see that COOL is in big red letters. But you probably already noticed that, really I am just taking up space to see how the margin caption looks like when it is really long :-).
```

:::{note}
:class: margin
This note should not overlap with the margin caption!
:::

Entire figures in the margin:

```{figure} ../images/cool.jpg
---
width: 60%
figclass: margin
alt: My figure text
---
This figure should be entirely in the margin.
```

## Sidenotes and marginnotes

Here's a sentence[^sn1] with multiple [^sn2] sidenotes.

[^sn1]: Test sidenote 1.
[^sn2]: Test sidenote 2.

Here's a sentence[^mn1] with multiple marginnotes[^mn2].

[^mn1]: {-} Test marginnote 1.
[^mn2]: {-} Test marginnote 2.


Sidenotes inside of admonitions should behave the same:

:::{note}
An admonition with a sidenote defined in the admonition[^snam1] and another defined outside of the admonition [^snam2].

[^snam1]: Sidenote defined in the admonition.

:::

[^snam2]: Sidenote defined outside the admonition.


## Nested admonitions

These aren't theme-specific, but we still show below to make sure they work.

::::{note} Here's a note!
:::{tip} And a tip!
:::
::::

## MyST Markdown elements

Here are a few design elements to show off MyST Markdown.

### Table alignment

To ensure that markdown alignment is rendered properly.

| Default Header | Left Align | Right Align | Center Align |
| -------------- | :--------- | ----------: | :----------: |
| Cell 1 | Cell 2 | Cell 3 | Cell 4 |
| Cell 1 | Cell 2 | Cell 3 | Cell 4 |

### List table width

Testing list tables take width as expected.

```{list-table}
:width: 100%
* - a
  - b
* - c
  - d
```
