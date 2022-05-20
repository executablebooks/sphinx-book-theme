"""Generate metadata for header buttons."""

from sphinx.errors import SphinxError


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


def prep_header_buttons(app, pagename, templatename, context, doctree):
    """Prep an empty list that we'll populate with header buttons."""
    context["header_buttons"] = []


def add_header_buttons(app, pagename, templatename, context, doctree):
    """Populate the context with header button metadata we'll insert in templates."""
    opts = app.config.html_theme_options
    pathto = context["pathto"]
    header_buttons = context["header_buttons"]

    # If we have a suffix, then we have a source file
    suff = context.get("page_source_suffix")

    # Full screen button
    if _as_bool(opts.get("use_fullscreen_button", True)):
        header_buttons.append(
            {
                "type": "button",
                "onclick": "toggleFullScreen()",
                "title": "Fullscreen mode",
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
                    "type": "button",
                    "url": repo_url,
                    "title": "Source repository",
                    "content": "repository",
                    "icon": "fab fa-github",
                }
            )

        if opts.get("use_issues_button"):
            repo_buttons.append(
                {
                    "type": "button",
                    "url": f"{repo_url}/issues/new?title=Issue%20on%20page%20%2F{context['pagename']}.html&body=Your%20issue%20content%20here.",  # noqa: E501
                    "content": "open issue",
                    "title": "Open an issue",
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

            repo_buttons.append(
                {
                    "type": "button",
                    "url": context["get_edit_url"](),
                    "title": "Edit this page",
                    "content": "suggest edit",
                    "icon": "fas fa-pencil-alt",
                }
            )

        # If we have multiple repo buttons enabled, add a group, otherwise just 1 button
        if len(repo_buttons) > 1:
            for rb in repo_buttons:
                rb["tooltip_placement"] = "left"
            header_buttons.append(
                {
                    "type": "dropdown",
                    "icon": "fab fa-github",
                    "items": repo_buttons,
                    "side": "right",
                }
            )
        elif len(repo_buttons) == 1:
            # Remove the text since it's just a single button, want just an icon.
            repo_buttons[0]["text"] = ""
            header_buttons.extend(repo_buttons)

    # Download buttons for various source content.
    if _as_bool(opts.get("use_download_button", True)) and suff:
        download_buttons = []

        # Create the dropdown list of buttons
        if context.get("ipynb_source"):
            download_buttons.append(
                {
                    "type": "button",
                    "url": f'{pathto("_sources", 1)}/{context.get("ipynb_source")}',
                    "content": ".ipynb",
                    "icon": "fas fa-code",
                    "title": "Download notebook file",
                    "tooltip_placement": "left",
                }
            )

        download_buttons.append(
            {
                "type": "button",
                "url": f'{pathto("_sources", 1)}/{context["sourcename"]}',
                "content": suff,
                "title": "Download source file",
                "tooltip_placement": "left",
                "icon": "fas fa-file",
            }
        )
        download_buttons.append(
            {
                "type": "button",
                "onclick": "printPdf(this)",
                "content": ".pdf",
                "title": "Print to PDF",
                "tooltip_placement": "left",
                "icon": "fas fa-file-pdf",
            }
        )

        # Add the group
        header_buttons.append(
            {
                "type": "dropdown",
                "icon": "fas fa-download",
                "items": download_buttons,
                "side": "right",
            }
        )
