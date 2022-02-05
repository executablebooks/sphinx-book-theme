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

:::{seealso}
See the [paragraph markup page](kitchen-sink/paragraph-markup.rst) for more references styling.
:::

## `ABlog` - Blog post list

[ABlog](https://ablog.readthedocs.io/en/latest/) is a Sphinx extension for blogging with Sphinx.

Here's a sample post list:

```{postlist}
:date: "%Y-%m-%d"
:format: "{date} - {title}"
:excerpts:
```

## `sphinx-togglebutton` - Toggle content with buttons

An admonition toggle:

## `sphinx-tabs` - Tabbed content

::::{tabs}
:::{tab} Apples
Some apples.
:::
:::{tab} Oranges
Some oranges.
:::
:::{tab} Pears
Some pears.
:::
::::
