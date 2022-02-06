(contribute/testing)=
# Testing infrastructure

Our testing infrastructure uses pytest

## Run the tests with a single environment

You can run the test suite with the default environment like so:

```console
$ tox
```

You can specify a specific environment like so:

```console
# Run the tests with Python 3.9, Sphinx 4
$ tox -e py39-sphinx4
```

## List all test environments

To list all of the test environments to may choose from, run:

```console
$ tox -a
```

Each one corresponds to a test environment or a task to build the documentation, and has its own virtual environment.

See the `tox.ini` file in the repository's root for details of all available development environments.

## Supply arguments to pytest

To supply arguments to pytest, use `--` and pass arguments after.
For example:


```console
$ tox -- -x
```

## Re-build an environment from scratch

By default, `tox` will only install the necessary environment **once**.
If you'd like to force a re-build, use the `-r` parameter. For example:

```console
$ tox -r -e py38-sphinx3
```

## Test audits with lighthouse

This theme uses the [`treosh/lighthouse-ci-action`](https://github.com/treosh/lighthouse-ci-action) to run some basic audits on our performance, accessibility, etc.

To preview the output of these tests:

- Click on the `docs-audit` GitHub Action job from a Pull Request.
- Scroll to the "Audit with Lighthouse" section
- If there are errors, you should see them along with the link to preview the report at `report: <URL TO PAGE>`.
- If there are not errors, you can list them by clicking the `uploading` section, which will reveal links to the report for each page


## Test multiple Sphinx versions

This theme is tested against the latest two major versions of Sphinx.
We try to set up our regression tests such that there are no differences between these two Sphinx versions.

**If it is important that we include a test that differs between Sphinx versions**, use the variable `sphinx_build.software_versions` to conditionally run tests based on the version of Sphinx.

For example:

```python
if sphinx_build.software_versions == "sphinx3":
   foo
elif sphinx_build.software_versions == "sphinx4":
   bar
```

If you are building a regression test, use the `extension` key to create a different regression file for that version of Sphinx.
For example:

```python
file_regression.check(
   html.prettify(),
   basename="foo",
   extension=f"{sphinx_build.software_versions}.html",
   encoding="utf8",
)
```

On Sphinx 3, this will create a file called `foo.sphinx3.html`.

:::{admonition} Do this sparingly!
:class: warning

Conditional testing logic across multiple major Sphinx versions has a negative impact on the maintainability and technical debt of this theme, so use this only when absolutely necessary.
:::
