# Contributing

This page contains developer documentation to help others contribute to
`sphinx-book-theme`.


## Code of Conduct

The `sphinx-book-theme` project follows the
[Executable Book Project code of conduct](https://executablebooks.org/en/latest/about.html#code-of-conduct).


## Releases

`sphinx-book-theme` uses [a GitHub Action](https://github.com/executablebooks/sphinx-book-theme/blob/master/.github/workflows/tests.yml#L57)
to automate as much of the release process as possible. There is a secret stored in
the repository that can push new releases to PyPI when new tags are created.

To create a new release, follow these steps:

* **Bump the version** by changing the line starting with `__version__ ==` in `__init__.py`.
  Use [semantic versioning](https://semver.org/) to decide whether it is a
  major or minor bump.

* **Commit and push to master**

  ```
  git commit -m "RELEASE: <version number>
  git push upstream master
  ```

* **Create a new release on GitHub**. Use the `<version-number>` for both the tag and
  title for the new release. For example: `v0.8.1`.

Once you create the new release, GitHub Actions will automatically build the new
release and update PyPI.
