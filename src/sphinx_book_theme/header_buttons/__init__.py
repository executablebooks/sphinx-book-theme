"""Generate metadata for header buttons."""
from sphinx.errors import SphinxError
from sphinx.locale import get_translation
from pydata_sphinx_theme import _get_theme_options, _config_provided_by_user
from sphinx.util import logging


LOGGER = logging.getLogger(__name__)
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


def _update_context_with_repository_info(opts, context):
    """Use the pydata theme to get the "edit this page" link."""
    # Check for manually given options first
    repo_url = opts.get("repository_url", "")
    branch = opts.get("repository_branch", "")
    provider = opts.get("repository_provider", "")
    relpath = opts.get("path_to_docs", "")
    if branch == "":
        branch = "main"

    # We assume the final two parts of the repository URL are the org/repo
    parts = repo_url.strip("/").split("/")
    org, repo = parts[-2:]

    # Infer the provider if it wasn't manually given
    provider_url = ""
    if provider == "":
        # We assume the provider URL is all of the parts that come before org/repo
        provider_url = "/".join(parts[:-2])
        for iprov in ["github", "gitlab", "bitbucket"]:
            if iprov in provider_url.lower():
                provider = iprov
                break

    # If provider is still empty, raise an error because we don't recognize it
    if provider == "":
        raise SphinxError(f"Provider not recognized in repository url {repo_url}")

    # Update the context because this is what the get_edit_url function uses.
    repository_information = {
        f"{provider}_user": org,
        f"{provider}_repo": repo,
        f"{provider}_version": branch,
        "doc_path": relpath,
    }

    # In case a self-hosted GitLab or BitBucket instance is used
    if provider_url != "":
        repository_information[f"{provider}_url"] = provider_url
    context.update(repository_information)


def _get_repo_url(context):
    """Return the provider URL based on what is defined in context."""
    for provider in ["github", "bitbucket", "gitlab"]:
        if f"{provider.lower()}_url" in context:
            source_user = f"{provider.lower()}_user"
            source_repo = f"{provider.lower()}_repo"
            provider_url = f"{provider.lower()}_url"
            repo_url = (
                f"{context[provider_url]}/{context[source_user]}/{context[source_repo]}"
            )
            return repo_url, provider


def prep_header_buttons(app, pagename, templatename, context, doctree):
    """Prep an empty list that we'll populate with header buttons."""
    context["header_buttons"] = []


def add_header_buttons(app, pagename, templatename, context, doctree):
    """Populate the context with header button metadata we'll insert in templates."""
    opts = _get_theme_options(app)
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
                "label": "fullscreen-button",
            }
        )

    # Edit this page button
    # Add HTML context variables that the pydata theme uses that we configure elsewhere
    # For some reason the source_suffix sometimes isn't there even when doctree is
    repo_keywords = [
        "use_issues_button",
        "use_source_button",
        "use_edit_page_button",
        "use_repository_button",
    ]
    for key in repo_keywords:
        opts[key] = _as_bool(opts.get(key))

    # Update pydata `html_context` options by inferring them from `repository_url`
    if "repository_url" in opts:
        _update_context_with_repository_info(opts, context)

    # Create source buttons for any that are enabled
    if any(opts.get(kw) for kw in repo_keywords):
        # Loop through the possible buttons and construct+add their URL
        repo_buttons = []
        if opts.get("use_repository_button"):
            repo_url, provider = _get_repo_url(context)

            repo_buttons.append(
                {
                    "type": "link",
                    "url": repo_url,
                    "tooltip": translation("Source repository"),
                    "text": "Repository",
                    "icon": f"fab fa-{provider.lower()}",
                    "label": "source-repository-button",
                }
            )

        if opts.get("use_source_button") and doctree and suff:
            # We'll re-use this to make action-specific URLs
            provider, edit_url = context["get_edit_provider_and_url"]()
            # Convert URL to a blob so it's for viewing
            if provider.lower() == "github":
                # Use plain=1 to ensure the source text is shown, not rendered
                source_url = edit_url.replace("/edit/", "/blob/") + "?plain=1"
            elif provider.lower() == "gitlab":
                source_url = edit_url.replace("/edit/", "/blob/")
            elif provider.lower() == "bitbucket":
                source_url = edit_url.replace("?mode=edit", "")

            repo_buttons.append(
                {
                    "type": "link",
                    "url": source_url,
                    "tooltip": translation("Show source"),
                    "text": translation("Show source"),
                    "icon": "fas fa-code",
                    "label": "source-file-button",
                }
            )

        if opts.get("use_edit_page_button") and doctree and suff:
            # We'll re-use this to make action-specific URLs
            provider, edit_url = context["get_edit_provider_and_url"]()
            repo_buttons.append(
                {
                    "type": "link",
                    "url": edit_url,
                    "tooltip": translation("Suggest edit"),
                    "text": translation("Suggest edit"),
                    "icon": "fas fa-pencil-alt",
                    "label": "source-edit-button",
                }
            )

        if opts.get("use_issues_button"):
            repo_url, provider = _get_repo_url(context)
            if "github.com" not in repo_url:
                LOGGER.warn(f"Open issue button not yet supported for {provider}")
            else:
                repo_buttons.append(
                    {
                        "type": "link",
                        "url": f"{repo_url}/issues/new?title=Issue%20on%20page%20%2F{context['pagename']}.html&body=Your%20issue%20content%20here.",  # noqa: E501
                        "text": translation("Open issue"),
                        "tooltip": translation("Open an issue"),
                        "icon": "fas fa-lightbulb",
                        "label": "source-issues-button",
                    }
                )

        # If we have multiple repo buttons enabled, add a group, otherwise just 1 button
        if len(repo_buttons) > 1:
            header_buttons.append(
                {
                    "type": "group",
                    "tooltip": translation("Source repositories"),
                    "icon": f"fab fa-{provider.lower()}",
                    "buttons": repo_buttons,
                    "label": "source-buttons",
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
                    "label": "download-notebook-button",
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
                "label": "download-source-button",
            }
        )
        download_buttons.append(
            {
                "type": "javascript",
                "javascript": "window.print()",
                "text": ".pdf",
                "tooltip": translation("Print to PDF"),
                "icon": "fas fa-file-pdf",
                "label": "download-pdf-button",
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
