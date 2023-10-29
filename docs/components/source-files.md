(customize:source-files)=
# Buttons that link to source files

There are a collection of buttons that you can use to link back to your source
repository. This lets users browse the repository, or take actions like suggest
an edit or open an issue.

(source-buttons:repository)=
## Set your source repository

You need to define a **source repository** for this functionality to work.
This is the online space where your code / documentation is hosted.
In each case, they require the following configuration to exist:

```python
html_theme_options = {
    ...
    "repository_url": "https://{your-provider}/{org}/{repo}",
    ...
}
```

Three providers are supported:

- **GitHub**: For example, `https://github.com/executablebooks/sphinx-book-theme`.
  This includes custom URLs for self-hosted GitHub.
- **GitLab**: For example, `https://gitlab.com/gitlab-org/gitlab`.
  This includes custom URLs for self-hosted GitLab.
- **BitBucket**: For example, `https://opensource.ncsa.illinois.edu/bitbucket/scm/u3d/3dutilities`.

In each case, we **assume the final two URL items are the `org/repo` pair**.

### Manually specify the provider

If your provider URL is more complex (e.g., if you're self-hosting your provider), you can manually specify the provider with the following configuration:

```python
html_theme_options = {
    ...
    "repository_provider": "gitlab"  # or "github", "bitbucket",
    "repository_url": "selfhostedgh.mycompany.org/user/repo",
    ...
}
```

Once this is provided, you may add source buttons by following the following sections.

(source-buttons:source)=
## Add a button to the page source

Show the raw source of the page on the provider you've proivded.
To add a button to the page source, first [configure your source repository](source-buttons:repository) and then add:

```python
html_theme_options = {
    ...
    "use_source_button": True,
    ...
}
```

Then configure the **repository branch** to use for your source.
By default it is `main`, but if you'd like to change this, use the following configuration:

```python
html_theme_options = {
    ...
    "repository_branch": "{your-branch}",
    ...
}
```

Finally, **configure the relative path to your documentation**.
By default, this is the root of the repository, but if your documentation is hosted in a sub-folder, use the following configuration:

```python
html_theme_options = {
    ...
    "path_to_docs": "{path-relative-to-site-root}",
    ...
}
```

## Add a button to suggest edits

Allow users to edit the page text directly on the provider and submit a pull request to update the documentation.
To add a button to edit the page, first [configure your source repository](source-buttons:repository) and then add:

```python
html_theme_options = {
    ...
    "use_edit_page_button": True,
    ...
}
```

Then follow the [branch and relative path instructions in the source file section](source-buttons:source).


(source-files:repository)=
## Add a link to your repository

To add a link to your repository, add the following configuration:

```python
html_theme_options = {
    ...
    "use_repository_button": True,
    ...
}
```

## Add a button to open issues

To add a button to open an issue about the current page, use the following
configuration:

```python
html_theme_options = {
    ...
    "use_issues_button": True,
    ...
}
```
