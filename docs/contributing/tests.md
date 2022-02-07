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

### Unit tests

Use the variable `sphinx_build.software_versions` to conditionally run tests based on the version of Sphinx.

For example:

```python
if sphinx_build.software_versions == ".sphinx3":
   foo
elif sphinx_build.software_versions == ".sphinx4":
   bar
```

### Regression tests

Regression tests are trickier, because updating them generally requires re-running the tests, not hand-editing code.
This is cumbersome for maintenance because we have to run the test suite two times for each regression that is updated.
For this reason, we have a more lightweight approach:

**If a regression test differs between Sphinx versions**, decide if the difference is substantial.
Do we gain something meaningful by testing both major versions of Sphinx, or is the difference unrelated to our theme's functionality?

1. **If not substantial**, then add a conditional and only run the regression test on the latest Sphinx version we support.
   Add a note to explain why you're only testing against one version of Sphinx.

   For example:

   ```python
   if sphinx_build.software_versions == ".sphinx4":
       # Only Sphinx4 because Sphinx3 adds an extra whitespace and isn't important
       file_regression.check(...)
   ```
2. **If it is substantial**, follow these steps:

   To support multiple Sphinx versions with regression tests, use the `extension` key to create a different regression file for that version of Sphinx.
   For example:

   ```python
   file_regression.check(
     html.prettify(),
     basename="foo",
     extension=f"{sphinx_build.software_versions}.html",
     encoding="utf8",
   )
   ```
