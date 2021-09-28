# -- Project information -----------------------------------------------------
import os
from pathlib import Path
from urllib import request

project = "Sphinx Book Theme"
copyright = "2020"
author = "the Executable Book Project"
# language = "fr"  # For testing language translations

master_doc = "index"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "ablog",
    "myst_nb",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_thebe",
    "sphinx_togglebutton",
    "sphinxcontrib.bibtex",
    "sphinxext.opengraph",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.8", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}
nitpick_ignore = [
    ("py:class", "docutils.nodes.document"),
    ("py:class", "docutils.parsers.rst.directives.body.Sidebar"),
]

suppress_warnings = ["myst.domains", "ref.ref"]

numfig = True

myst_enable_extensions = [
    "dollarmath",
    # "amsmath",
    "deflist",
    # "html_admonition",
    # "html_image",
    "colon_fence",
    # "smartquotes",
    # "replacements",
    # "linkify",
    # "substitution",
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"
html_logo = "_static/logo-wide.svg"
html_title = "Sphinx Book Theme"
html_copy_source = True
html_sourcelink_suffix = ""
html_favicon = "_static/logo-square.svg"
html_last_updated_fmt = ""

html_sidebars = {
    "reference/blog/*": [
        "sidebar-logo.html",
        "search-field.html",
        "postcard.html",
        "recentposts.html",
        "tagcloud.html",
        "categories.html",
        "archives.html",
        "sbt-sidebar-nav.html",
        "sbt-sidebar-footer.html",
    ]
}
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
jupyter_execute_notebooks = "cache"
thebe_config = {
    "repository_url": "https://github.com/binder-examples/jupyter-stacks-datascience",
    "repository_branch": "master",
}

html_theme_options = {
    "theme_dev_mode": True,
    "path_to_docs": "docs",
    "repository_url": "https://github.com/executablebooks/sphinx-book-theme",
    # "repository_branch": "gh-pages",  # For testing
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        # "jupyterhub_url": "https://datahub.berkeley.edu",  # For testing
        "colab_url": "https://colab.research.google.com/",
        "notebook_interface": "jupyterlab",
        "thebe": True,
    },
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
    "use_download_button": True,
    "logo_only": True,
    # For testing
    # "use_fullscreen_button": False,
    # "home_page_in_toc": True,
    # "single_page": True,
    # "extra_footer": "<a href='https://google.com'>Test</a>",  # DEPRECATED KEY
    # "extra_navbar": "<a href='https://google.com'>Test</a>",
    # "show_navbar_depth": 2,
}

# -- ABlog config -------------------------------------------------
blog_path = "reference/blog"
blog_post_pattern = "reference/blog/*.md"
blog_baseurl = "https://sphinx-book-theme.readthedocs.io"
fontawesome_included = True
post_auto_image = 1
post_auto_excerpt = 2
execution_show_tb = "READTHEDOCS" in os.environ
bibtex_bibfiles = ["references.bib"]
bibtex_reference_style = "author_year"

# -- Download kitchen sink reference docs -------------------------------------
# These are the kitchen sink files used by the Sphinx Themes gallery at
# https://github.com/sphinx-themes/sphinx-themes.org
# To re-download, delete the `references/kitchen-sink` folder and build the docs
kitchen_sink_files = [
    "api.rst",
    "index.rst",
    "lists-and-tables.rst",
    "paragraph-markup.rst",
]
for ifile in kitchen_sink_files:
    path_file = Path(f"reference/kitchen-sink/{ifile}")
    path_file.parent.mkdir(exist_ok=True)
    if not path_file.exists():
        print(f"Downloading kitchen sink file {ifile}")
        resp = request.urlopen(
            f"https://github.com/sphinx-themes/sphinx-themes.org/raw/master/sample-docs/kitchen-sink/{ifile}"  # noqa
        )
        header = ".. DOWNLOADED FROM sphinx-themes.org, DO NOT MANUALLY EDIT\n"
        path_file.write_text(header + resp.read().decode())
