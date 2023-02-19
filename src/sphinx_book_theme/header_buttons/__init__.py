"""Generate metadata for header buttons."""

from sphinx.errors import SphinxError
from sphinx.locale import get_translation

MESSAGE_CATALOG_NAME = "booktheme"
translation = get_translation(MESSAGE_CATALOG_NAME)


def _as_bool(var):
    """Cast string as a boolean with some extra checks.

    If var is a string, it will be matched to 'true'/'false'
    If var is a bool, it will be returned
    If var is None, it will return False.
    """
    if isinstance(var, str):
        return var.lower() == "true"
    elif isinstance(var, bool):
        return var
    else:
        return False


def _config_provided_by_user(app, key):
    """Check if the user has manually provided the config."""
    # TODO: Remove this when we bump pydata to the latest version and import from there.
    return any(key in ii for ii in [app.config.overrides, app.config._raw_config])


def prep_header_buttons(app, pagename, templatename, context, doctree):
    """Prep an empty list that we'll populate with header buttons."""
    context["header_buttons"] = []


def add_header_buttons(app, pagename, templatename, context, doctree):
    """Populate the context with header button metadata we'll insert in templates."""
    opts = app.builder.theme_options
    pathto = context["pathto"]
    header_buttons = context["header_buttons"]

    # If we have a suffix, then we have a source file
    suff = context.get("page_source_suffix")

    # Full screen button
    if _as_bool(opts.get("use_fullscreen_button", True)):
        header_buttons.append(
            {
                "type": "javascript",
                "javascript": "toggleFullScreen()",
                "tooltip": translation("Fullscreen mode"),
                "icon": "fas fa-expand",
            }
        )

    # Edit this page button
    # Add HTML context variables that the pydata theme uses that we configure elsewhere
    # For some reason the source_suffix sometimes isn't there even when doctree is
    repo_keywords = [
        "use_issues_button",
        "use_edit_page_button",
        "use_repository_button",
    ]
    for key in repo_keywords:
        opts[key] = _as_bool(opts.get(key))

    if any(opts.get(kw) for kw in repo_keywords):
        repo_url = opts.get("repository_url", "")
        if not repo_url:
            raise SphinxError(
                "Repository buttons enabled, but repository_url not given. "
                "Please add a repository_url."
            )
        repo_buttons = []
        if opts.get("use_repository_button"):
            repo_buttons.append(
                {
                    "type": "link",
                    "url": repo_url,
                    "tooltip": translation("Source repository"),
                    "text": "repository",
                    "icon": "fab fa-github",
                }
            )

        if opts.get("use_issues_button"):
            repo_buttons.append(
                {
                    "type": "link",
                    "url": f"{repo_url}/issues/new?title=Issue%20on%20page%20%2F{context['pagename']}.html&body=Your%20issue%20content%20here.",  # noqa: E501
                    "text": translation("open issue"),
                    "tooltip": translation("Open an issue"),
                    "icon": "fas fa-lightbulb",
                }
            )

        if opts.get("use_edit_page_button") and doctree and suff:
            branch = opts.get("repository_branch", "")
            if branch == "":
                branch = "master"
            relpath = opts.get("path_to_docs", "")
            org, repo = repo_url.strip("/").split("/")[-2:]

            # Update the context because this is what the get_edit_url function uses.
            context.update(
                {
                    "github_user": org,
                    "github_repo": repo,
                    "github_version": branch,
                    "doc_path": relpath,
                }
            )

            provider, url = context["get_edit_provider_and_url"]()
            repo_buttons.append(
                {
                    "type": "link",
                    "url": url,
                    "tooltip": translation("Edit on") + f"{provider}",
                    "text": translation("suggest edit"),
                    "icon": "fas fa-pencil-alt",
                }
            )

        # If we have multiple repo buttons enabled, add a group, otherwise just 1 button
        if len(repo_buttons) > 1:
            header_buttons.append(
                {
                    "type": "group",
                    "tooltip": translation("Source repositories"),
                    "icon": "fab fa-github",
                    "buttons": repo_buttons,
                    "label": "repository-buttons",
                }
            )
        elif len(repo_buttons) == 1:
            # Remove the text since it's just a single button, want just an icon.
            repo_buttons[0]["text"] = ""
            header_buttons.extend(repo_buttons)

    # Download buttons for various source content.
    if _as_bool(opts.get("use_download_button", True)) and suff:
        download_buttons = []

        # An ipynb file if it was created as part of the build (e.g. by MyST-NB)
        if context.get("ipynb_source"):
            download_buttons.append(
                {
                    "type": "link",
                    "url": f'{pathto("_sources", 1)}/{context.get("ipynb_source")}',
                    "text": ".ipynb",
                    "icon": "fas fa-code",
                    "tooltip": translation("Download notebook file"),
                }
            )

        # Download the source file
        download_buttons.append(
            {
                "type": "link",
                "url": f'{pathto("_sources", 1)}/{context["sourcename"]}',
                "text": suff,
                "tooltip": translation("Download source file"),
                "icon": "fas fa-file",
            }
        )
        download_buttons.append(
            {
                "type": "javascript",
                "javascript": "window.print()",
                "text": ".pdf",
                "tooltip": translation("Print to PDF"),
                "icon": "fas fa-file-pdf",
            }
        )

        # Add the group
        header_buttons.append(
            {
                "type": "group",
                "tooltip": translation("Download this page"),
                "icon": "fas fa-download",
                "buttons": download_buttons,
                "label": "download-buttons",
            }
        )


def update_sourcename(app):
    # Download the source file
    # Sphinx defaults to .txt for html_source_suffix even though the pages almost
    # always are stored in their native suffix (.rst, .md, or .ipynb). So unless
    # the user manually specifies an html_source_suffix, default to an empty string.
    # _raw_config is the configuration as provided by the user.
    # If a key isn't in it, then the user didn't provide it
    if not _config_provided_by_user(app, "html_sourcelink_suffix"):
        app.config.html_sourcelink_suffix = ""
