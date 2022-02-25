---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.8.2
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Jupyter notebooks

This is a page to demonstrate the look and feel of Jupyter Notebook elements.


## Hiding elements

### Hiding inputs

```{code-cell} ipython3
:tags: [remove_cell]

# Generate some code that we'll use later on in the page
import numpy as np
import matplotlib.pyplot as plt

square = np.random.randn(100, 100)
wide = np.random.randn(100, 1000)
```

```{code-cell} ipython3
:tags: [hide_input]

# Hide input
square = np.random.randn(100, 100)
wide = np.random.randn(100, 1000)

fig, ax = plt.subplots()
ax.imshow(square)

fig, ax = plt.subplots()
ax.imshow(wide)
```

### Hiding outputs

```{code-cell} ipython3
:tags: [hide_output]

# Hide output
square = np.random.randn(100, 100)
wide = np.random.randn(100, 1000)

fig, ax = plt.subplots()
ax.imshow(square)

fig, ax = plt.subplots()
ax.imshow(wide)
```

### Hiding markdown

````{toggle}
```{note}
This is a hidden markdown cell

It should be hidden!
```
````

```{admonition} And here's a toggleable note
:class: dropdown
With a body!
```

+++

### Hiding both inputs and outputs

```{code-cell} ipython3
:tags: [hide_output, hide_input]

square = np.random.randn(100, 100)
wide = np.random.randn(100, 1000)

fig, ax = plt.subplots()
ax.imshow(square)

fig, ax = plt.subplots()
ax.imshow(wide)
```

### Hiding the whole cell

```{code-cell} ipython3
:tags: [hide_cell]

square = np.random.randn(100, 100)
wide = np.random.randn(100, 1000)

fig, ax = plt.subplots()
ax.imshow(square)

fig, ax = plt.subplots()
ax.imshow(wide)
```

## Enriched outputs

### Math

```{code-cell} ipython3
# You can also include enriched outputs like Math
from IPython.display import Math
Math("\sum_{i=0}^n i^2 = \frac{(n^2+n)(2n+1)}{6}")
```

### Pandas DataFrames


```{code-cell} ipython3

import pandas as pd
df = pd.DataFrame([['hi', 'there'], ['this', 'is'], ['a', 'DataFrame']], columns=['Word A', 'Word B'])
df
```

Styled DataFrames (see [the Pandas Styling docs](https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html)).

```{code-cell} ipython3
:tags: [hide-input]

import pandas as pd

np.random.seed(24)
df = pd.DataFrame({'A': np.linspace(1, 10, 10)})
df = pd.concat([df, pd.DataFrame(np.random.randn(10, 4), columns=list('BCDE'))],
               axis=1)
df.iloc[3, 3] = np.nan
df.iloc[0, 2] = np.nan

def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val < 0 else 'black'
    return 'color: %s' % color

def highlight_max(s):
    '''
    highlight the maximum in a Series yellow.
    '''
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]

df.style.\
    applymap(color_negative_red).\
    apply(highlight_max).\
    set_table_attributes('style="font-size: 10px"')
```

## Interactive outputs

### Folium

```{code-cell} ipython3
import folium
```

```{code-cell} ipython3
m = folium.Map(
    location=[45.372, -121.6972],
    zoom_start=12,
    tiles='Stamen Terrain'
)

folium.Marker(
    location=[45.3288, -121.6625],
    popup='Mt. Hood Meadows',
    icon=folium.Icon(icon='cloud')
).add_to(m)

folium.Marker(
    location=[45.3311, -121.7113],
    popup='Timberline Lodge',
    icon=folium.Icon(color='green')
).add_to(m)

folium.Marker(
    location=[45.3300, -121.6823],
    popup='Some Other Location',
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)


m
```

## Stdout

```{code-cell} ipython3
# The ! causes this to run as a shell command
!jupyter -h
```

## Formatting code cells

### Scrolling cell outputs

```{code-cell} ipython3
:tags: [output_scroll]
for ii in range(40):
    print(f"this is output line {ii}")
```

### Scrolling cell inputs

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
