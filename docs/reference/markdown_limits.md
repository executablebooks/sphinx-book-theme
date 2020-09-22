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
---

# Layout and demo and reference

This page contains a number of reference elements to see how they look in this
theme. The information is not meant to be easy to read or understand, just browse
through and see how things look!

## Glossary

```{glossary}
term one
  An indented explanation of term 1

A second term
  An indented explanation of term2
```

To reference terms in your glossary, use the `{term}` role. For example,
`` {term}`term one` `` becomes {term}`term one`. And `` {term}`A second term` ``
becomes {term}`A second term`.

## Interactive code

```{code-cell} ipython3
import plotly.io as pio
import plotly.express as px
import plotly.offline as py

pio.renderers.default = "notebook"

df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", size="sepal_length")
fig
```

+++

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

# Hide input
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

## Full-width elements
### Full width code cells

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

+++ {"tags": ["full_width"]}

### Full-width markdown

This is some markdown that should be shown at full width.

Here's the Jupyter logo:

![](https://raw.githubusercontent.com/adebar/awesome-jupyter/master/logo.png)

+++

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

+++

### Margins

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
### Toggle buttons

Here's some margin content, let's see how it interacts w/ the toggle button

```{margin} My margin
Here's my margin content
```

Here's a toggleable note:

```{note}
:class: toggle
My note
```

### Full-width content

```{note}
:class: tag_fullwidth
This is my test
```

Let's see what happens

```{code-cell} ipython3
:tags: [popout]

## code cell in the margin with output
fig, ax = plt.subplots()
ax.imshow(wide)
```

+++ {"tags": ["popout"]}

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

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" style="max-width:200px" />

+++

### More content after the popouts

This is extra content after the popouts to see if cells overlap and such.
Also to make sure you can still interact with the popout content.
This is extra content after the popouts to see if cells overlap and such.
Also to make sure you can still interact with the popout content.

```python
a = 2
```

This is extra content after the popouts to see if cells overlap and such.
Also to make sure you can still interact with the popout content.
This is extra content after the popouts to see if cells overlap and such.
Also to make sure you can still interact with the popout content.
This is extra content after the popouts to see if cells overlap and such.
Also to make sure you can still interact with the popout content.

+++

## Markdown limits

The remaining part of this page has been taken from the Markdown
documentation, and is meant to give an idea of how Jupyter Book renders really long pages of
very diverse content!

### Common publishing items

```{figure} ../images/cool.jpg
---
width: 200px
alt: My figure text
name: myfig
---
And here is my figure caption
```

We can reference the figure with {ref}`myfig`. Or a numbered reference like
{numref}`myfig`.

```{figure} ../images/cool.jpg
---
width: 200px
align: left
alt: My figure text
name: myfig2
---
And here is my figure caption
```

We can reference the figure with {ref}`myfig2`. Or a numbered reference like
{numref}`myfig2`.

```{figure} ../images/cool.jpg
---
width: 60%
align: right
alt: My figure text
name: myfig3
---
And here is my figure caption
```

We can reference the figure with {ref}`myfig3`. Or a numbered reference like
{numref}`myfig3`.

### Really wide content

Here's how really wide content alters the page:

#### Pre blocks

```
123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789
```

#### Wide images

<img src="https://jupyter.org/assets/nav_logo.svg" style="width: 1000px" />

### Testing `code in headers`

The above should be roughly the same size...

### Testing Unicode headers

The following headers test that we are able to render non-American characters
in ways that look nice.

#### Це тестовий заголовок Кирилицею
Lorem ipsum

#### これは日本語のテストヘッダーです
Lorem ipsum

#### هذا اختبار للرأس باللغة العربية
Lorem ipsum

#### 這是中文標題測試

### Markdown Cheatsheet
This is intended as a quick reference and showcase. For more complete info, see [John Gruber's original spec](http://daringfireball.net/projects/markdown/) and the [Github-flavored Markdown info page](http://github.github.com/github-flavored-markdown/).

This cheatsheet is specifically *Markdown Here's* version of Github-flavored Markdown. This differs slightly in styling and syntax from what Github uses, so what you see below might vary a little from what you get in a *Markdown Here* email, but it should be pretty close.

You can play around with Markdown on our [live demo page](http://www.markdown-here.com/livedemo.html).

<a name="emphasis"/>

#### Emphasis

```bash
Emphasis, aka italics, with *asterisks* or _underscores_.

Strong emphasis, aka bold, with **asterisks** or __underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses two tildes. ~~Scratch this.~~
```

Emphasis, aka italics, with *asterisks* or _underscores_.

Strong emphasis, aka bold, with **asterisks** or __underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses two tildes. ~~Scratch this.~~


<a name="lists"/>

#### Lists

```bash
1. First ordered list item
2. Another item
  * Unordered sub-list.
1. Actual numbers don't matter, just that it's a number
  1. Ordered sub-list
4. And another item.

   Some text that should be aligned with the above item.

* Nested unordered list
  * Unordered sub-list

* Unordered list can use asterisks
- Or minuses
+ Or pluses
```

1. First ordered list item
2. Another item
  * Unordered sub-list.
1. Actual numbers don't matter, just that it's a number
  1. Ordered sub-list
4. And another item.

   Some text that should be aligned with the above item.

* Nested unordered list
  * Unordered sub-list

* Unordered list can use asterisks
- Or minuses
+ Or pluses

<a name="links"/>

#### Links

There are two ways to create links.

```bash
[I'm an inline-style link](https://www.google.com)

[I'm a reference-style link][Arbitrary case-insensitive reference text]

[You can use numbers for reference-style link definitions][1]

Or leave it empty and use the [link text itself]

URLs and URLs in angle brackets will automatically get turned into links.
http://www.example.com or <http://www.example.com> and sometimes
example.com (but not on Github, for example).

Some text to show that the reference links can follow later.

[arbitrary case-insensitive reference text]: https://www.mozilla.org
[1]: http://slashdot.org
[link text itself]: http://www.reddit.com
```

[I'm an inline-style link](https://www.google.com)

[I'm a reference-style link][Arbitrary case-insensitive reference text]

[You can use numbers for reference-style link definitions][1]

Or leave it empty and use the [link text itself]

URLs and URLs in angle brackets will automatically get turned into links.
http://www.example.com or <http://www.example.com> and sometimes
example.com (but not on Github, for example).

Some text to show that the reference links can follow later.

[arbitrary case-insensitive reference text]: https://www.mozilla.org
[1]: http://slashdot.org
[link text itself]: http://www.reddit.com

<a name="images"/>

#### Images

```md
Here's our logo (hover to see the title text):

Inline-style:
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

Reference-style:
![alt text][logo]

[logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
```

Here's our logo (hover to see the title text):

Inline-style:
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

Reference-style:
![alt text][logo]

[logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"

<a name="code"/>

#### Code and Syntax Highlighting

Code blocks are part of the Markdown spec, but syntax highlighting isn't. However, many renderers -- like Github's and *Markdown Here* -- support syntax highlighting. *Markdown Here* supports highlighting for dozens of languages (and not-really-languages, like diffs and HTTP headers); to see the complete list, and how to write the language names, see the [highlight.js demo page](http://softwaremaniacs.org/media/soft/highlight/test.html).

```bash
Inline `code` has `back-ticks around` it.
```

Inline `code` has `back-ticks around` it.

Blocks of code are either fenced by lines with three back-ticks <code>```</code>, or are indented with four spaces. I recommend only using the fenced code blocks -- they're easier and only they support syntax highlighting.

<pre lang="no-highlight"><code>```javascript
var s = "JavaScript syntax highlighting";
alert(s);
```

```python
s = "Python syntax highlighting"
print s
```

```bash
No language indicated, so no syntax highlighting.
But let's throw in a &lt;b&gt;tag&lt;/b&gt;.
```
</code></pre>



```javascript
var s = "JavaScript syntax highlighting";
alert(s);
```

```python
s = "Python syntax highlighting"
print s
```

```md
No language indicated, so no syntax highlighting in Markdown Here (varies on Github).
But let's throw in a <b>tag</b>.
```

Again, to see what languages are available for highlighting, and how to write those language names, see the [highlight.js demo page](http://softwaremaniacs.org/media/soft/highlight/test.html).

<a name="tables"/>

#### Tables

Tables aren't part of the core Markdown spec, but they are part of GFM and *Markdown Here* supports them. They are an easy way of adding tables to your email -- a task that would otherwise require copy-pasting from another application.

```md
Colons can be used to align columns.

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

The outer pipes (|) are optional, and you don't need to make the raw Markdown line up prettily. You can also use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3
```

Colons can be used to align columns.

| Tables        | Are           | Cool |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

The outer pipes (|) are optional, and you don't need to make the raw Markdown line up prettily. You can also use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3

<a name="blockquotes"/>

#### Blockquotes

```md
> Blockquotes are very handy in email to emulate reply text.
> This line is part of the same quote.

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote.
```

> Blockquotes are very handy in email to emulate reply text.
> This line is part of the same quote.

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote.

<a name="html"/>

#### Inline HTML

You can also use raw HTML in your Markdown, and it'll mostly work pretty well.

```html
<dl>
  <dt>Definition list</dt>
  <dd>Is something people use sometimes.</dd>

  <dt>Markdown in HTML</dt>
  <dd>Does *not* work **very** well. Use HTML <em>tags</em>.</dd>
</dl>
```

<dl>
  <dt>Definition list</dt>
  <dd>Is something people use sometimes.</dd>

  <dt>Markdown in HTML</dt>
  <dd>Does *not* work **very** well. Use HTML <em>tags</em>.</dd>
</dl>

<a name="hr"/>

#### Horizontal Rule

```md
Three or more...

---

Hyphens

***

Asterisks

___

Underscores
```

Three or more...

---

Hyphens

***

Asterisks

___

Underscores

<a name="lines"/>

#### Line Breaks

My basic recommendation for learning how line breaks work is to experiment and discover -- hit &lt;Enter&gt; once (i.e., insert one newline), then hit it twice (i.e., insert two newlines), see what happens. You'll soon learn to get what you want. "Markdown Toggle" is your friend.

Here are some things to try out:

```bash
Here's a line for us to start with.

This line is separated from the one above by two newlines, so it will be a *separate paragraph*.

This line is also a separate paragraph, but...
This line is only separated by a single newline, so it's a separate line in the *same paragraph*.
```

Here's a line for us to start with.

This line is separated from the one above by two newlines, so it will be a *separate paragraph*.

This line is also begins a separate paragraph, but...
This line is only separated by a single newline, so it's a separate line in the *same paragraph*.

(Technical note: *Markdown Here* uses GFM line breaks, so there's no need to use MD's two-space line breaks.)

<a name="videos"/>

#### YouTube Videos

They can't be added directly but you can add an image with a link to the video like this:

```md
<a href="http://www.youtube.com/watch?feature=player_embedded&v=YOUTUBE_VIDEO_ID_HERE
" target="_blank"><img src="http://img.youtube.com/vi/YOUTUBE_VIDEO_ID_HERE/0.jpg"
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>
```

Or, in pure Markdown, but losing the image sizing and border:

```md
[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/YOUTUBE_VIDEO_ID_HERE/0.jpg)](http://www.youtube.com/watch?v=YOUTUBE_VIDEO_ID_HERE)
```

<a name="tex"/>

#### TeX Mathematical Formulae

A full description of TeX math symbols is beyond the scope of this cheatsheet. Here's a [good reference](https://en.wikibooks.org/wiki/LaTeX/Mathematics), and you can try stuff out on [CodeCogs](https://www.codecogs.com/latex/eqneditor.php). You can also play with formulae in the Markdown Here options page.

Here are some examples to try out:

```bash
$-b \pm \sqrt{b^2 - 4ac} \over 2a$
$x = a_0 + \frac{1}{a_1 + \frac{1}{a_2 + \frac{1}{a_3 + a_4}}}$
$\forall x \in X, \quad \exists y \leq \epsilon$
```

The beginning and ending dollar signs (`$`) are the delimiters for the TeX markup.

#### Build the book's HTML locally

Once you've generated the markdown for your notebooks and installed the
necessary dependencies. You are ready to build your book HTML.

Ensure that your notebooks have been converted to markdown, there should be a
collection of them in `_build/`.

In order to locally build your book's HTML with Jekyll, you'll need to either install
a container software (Docker or Singularity) or Ruby.

In our experience, we've found that [containers](https://www.docker.com/resources/what-container)
provide an easier installation for most systems.
If you are developing on a system where you have administrator privileges
(i.e., you have `root` permissions), we recommend you use [Docker](https://docs.docker.com/get-started/).

We also provide instructions for using [Singularity](https://www.sylabs.io/guides/2.6/user-guide/quick_start.html),
an alternate containerization software for systems where you do not have administrator privileges.
To learn more about using containers, please see the
[Docker for scientists guide](https://neurohackweek.github.io/docker-for-scientists/).

##### Building your site locally with Containers: Docker

First, you'll need to make sure you have Docker installed.
There are [installation instructions for each operating system](https://hub.docker.com/search/?type=edition&offering=community)
to guide you through this process.

Once Docker is available on your system, you can build the image locally with:

```bash
docker pull emdupre/jupyter-book
```

You can then access this image with:

```bash
docker run --rm --security-opt label:disable  \
   -v /full/path/to/your/book:/srv/jekyll \
   -p 4000:4000 \
   -it -u 1000:1000 \
   emdupre/jupyter-book bundle exec jekyll serve --host 0.0.0.0
```

If you navigate to `http://0.0.0.0:4000/jupyter-book/` in your browser,
you should see a preview copy of your book.
If you instead see an error, please try to update your local book;
see [the Jupyter Book FAQ section](https://jupyterbook.org/guide/04_faq.html#how-can-i-update-my-book)
for more details on how to do so.

##### Building your site locally with Containers: Singularity

If you are on a system where you do not have administrator privileges (such as a shared
computing cluster), you will not be able to use Docker.
Instead, you can use Singularity.
First, you'll need to check with your resource manager that Singularity is available
on your system.

You can then create a Jupyter Book Singularity image using:

```bash
singularity build jupyter-book.simg docker://emdupre/jupyter-book
```

Next, you can access this image with:

```bash
singularity run -B /full/path/to/your/book:/srv/jekyll \
    --pwd /srv/jekyll \
    jupyter-book.simg bundle exec jekyll serve
```

And that's it! If you navigate to `http://127.0.0.1:4000/jupyter-book/` in your browser,
you should see a preview copy of your book.

##### Building your site locally with Ruby

You can also choose to build your site locally without a container.
In this case, you'll need Ruby, an open-source programming language, to build your site's
HTML with Jekyll. The easiest way to install Ruby on *nix systems is to use
the *`conda`* package manager:

```bash
conda install -c conda-forge ruby
```
Once you have Ruby installed, run

```bash
make install
```

which will install Bundler (a Ruby dependency management tool) and then install the plugins
needed to build the site for your book.

You can then build the site locally by running:

```bash
make site
```

Alternatively, you can preview your book's site locally by running this command:

```bash
make serve
```

This should open up a port on your computer with a live version of the book.


##### When should you build the HTML locally?

You might ask: if GitHub pages can build my site automatically from the markdown files, why
build it locally? The main reason for this is that you get more flexibility by building locally
and serving raw HTML, as opposed to auto-building the site with GitHub-pages.

In particular, if you wish to use any **extra Jekyll plugins**, such as the `jekyll-scholar` plugin that
enables you to add citations and bibliographies, then you need to build your site
locally as HTML. GitHub-pages doesn't let you enable any extra plugins if it auto-builds your site.

#### Create an *online* repository for your book

You've created your book on your own computer, but you haven't yet added it
online. This section covers the steps to create your own GitHub repository,
and to add your book's content to it.

1. First, log-in to GitHub, then go to the "create a new repository" page:

https://github.com/new

2. Next, add a name and description for your book. You can choose whatever
   initialization you'd like.

3. Now, clone the empty repository to your computer:

   ```bash
   git clone https://github.com/<my-org>/<my-book-name>
   ```

4. Copy all of your book files and folders (what was created when you ran `jupyter-book create mybook`)
   into the new repository. For example, if you created your book locally with `jupyter-book create mylocalbook`
   and your online repository is called `myonlinebook`, the command would be:

   ```bash
   cp -r mylocalbook/* myonlinebook/
   ```

   This will copy over the local book files into the online book folder.

5. Commit the new files to the repository in `myonlinebook/`:

   ```bash
   cd myonlinebook
   git add ./*
   git commit -m "adding my first book!"
   git push
   ```

That's it!

#### Publish your book online with GitHub Pages

Once you've built the markdown for your book (in `_build`) or built the HTML
for your book (in `_site`), you can push your book contents to GitHub so that
others can access your book. To do so, follow these steps:

0. Confirm that your site files are built. You should see a
   collection of markdown files/folders in the `_build` folder,
   or a collection of HTML in your `_site/` folder.
1. Commit and push the changes to your repository.
2. Enable GitHub site building for your repository.

   From your GitHub repository, click `Settings` then scroll down to the
   `GitHub Pages` section. You should see the message `Your site is published at <YOUR-URL>`.
   Ensure that you're building from the correct folder.

3. Go to the URL listed at `<YOUR-URL>` and you should see your live site.
