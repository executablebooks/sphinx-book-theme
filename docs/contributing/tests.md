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
