# Contributing

This page contains developer documentation to help others contribute to
`sphinx-book-theme`.

## Releases

`sphinx-book-theme` uses [a GitHub Action](https://github.com/ExecutableBookProject/sphinx-book-theme/blob/master/.github/workflows/tests.yml#L57)
to automate as much of the release process as possible. There is a secret stored in
the repository that can push new releases to PyPI when new tags are created.

To create a new release, follow these steps:

* **Remove `dev0` from the version** by changing the line starting with `__version__ ==` in `__init__.py`.
  Use [semantic versioning](https://semver.org/) to decide whether it is a
  major or minor bump. For example:

  ```
  __version__ = "v0.8.1dev0"
  ```
  becomes
  ```
  __version__ = "v0.8.1"
  ```

* **Commit and push to master**

  ```
  git commit -m "RLS: <version number>
  git push upstream master
  ```

* **Create a new release on GitHub**. Use the `<version-number>` for both the tag and
  title for the new release. For example: `v0.8.1`.

* **Bump the version** and add `dev0` back to the version string. Use
  [semantic versioning](https://semver.org/) to decide whether it is a
  major or minor bump. For example:

  ```
  __version__ = "v0.8.2dev0"
  ```

  finally, commit and push the change

  ```
  git commit -m "DEV: v0.8.2dev0"
  git push upstream master
  ```

Once you create the new release, GitHub Actions will automatically build the new
release and update PyPI.
