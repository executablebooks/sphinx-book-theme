# Sphinx extension styles

This page shows of some special-case styling for various Sphinx extensions.


## `sphinxcontrib-bibtex` - References and bibliographies

[`sphinxcontrib-bibtex`](https://sphinxcontrib-bibtex.readthedocs.io/en/latest/) provides support for citations and bibliographies.

Because this theme deals with scholarly and scientific communication, `sphinxcontrib-bibtex` should work particularly well.

Here's are a few citations:

- Default citation {cite}`project_jupyter-proc-scipy-2018`, {cite}`holdgraf_rapid_2016,project_jupyter-proc-scipy-2018`. (should be same as parenthetical)
- Parenthetical citation {cite:p}`project_jupyter-proc-scipy-2018`, {cite:p}`holdgraf_rapid_2016,project_jupyter-proc-scipy-2018`.
- Textual citation {cite:t}`project_jupyter-proc-scipy-2018`, {cite:t}`holdgraf_rapid_2016,project_jupyter-proc-scipy-2018`.

And here's a bibliography:

```{bibliography}
```


## `ABlog` - Blog post list

[ABlog](https://ablog.readthedocs.io/) is a Sphinx extension for blogging with Sphinx.

Here's a sample post list:

```{postlist}
:date: "%Y-%m-%d"
:format: "{date} - {title}"
:excerpts:
```

## `sphinx-togglebutton` - Toggle content with buttons

A block toggle:

```{toggle}

:::{note} This note is toggled!
:::

```

A block toggle in the margin:

::::{container} margin

```{toggle}

:::{note} This note is toggled!
:::

```

::::

An admonition toggle:

:::{note}
:class: dropdown

This note will be toggled!

:::

An admonition toggle in the margin

::::{note}
:class: margin

:::{toggle}

This toggle is in the margin!

:::

::::

## `sphinx-tabs` - Tabbed content

% For some reason sphinx-tabs doesn't work properly with myst markdown
% so using rST here.
````{eval-rst}
.. tabs::

   .. tab:: Apples

      Apples are green, or sometimes red.

   .. tab:: Pears

      Pears are green.

   .. tab:: Oranges

      Oranges are orange.
````

## `sphinxcontrib.youtube` for videos

[`sphinxcontrib.youtube`](https://github.com/sphinx-contrib/youtube) makes it possible to easily embed videos in your documentation.

```{youtube} 2Z7wDaYt53Y
```

## `sphinx-design` for UI components

{bdg-primary}`Test badge`.
