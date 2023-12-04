import os
from pathlib import Path
from shutil import copytree, rmtree
from subprocess import check_call
from importlib.metadata import version
from packaging.version import parse

from bs4 import BeautifulSoup
import pytest
import sphinx
from sphinx.testing.util import SphinxTestApp

sphinx_version = parse(version("sphinx"))
if sphinx_version.major < 7:
    from sphinx.testing.path import path as sphinx_path
else:
    from pathlib import Path as sphinx_path


path_tests = Path(__file__).parent


class SphinxBuild:
    def __init__(self, app: SphinxTestApp, src: Path):
        self.app = app
        self.src = src
        self.software_versions = (
            f".sphinx{sphinx.version_info[0]}"  # software version tracking for fixtures
        )

    def build(self, assert_pass=True):
        self.app.build()
        assert self.warnings == "", self.status
        return self

    @property
    def status(self):
        return self.app._status.getvalue()

    @property
    def warnings(self):
        return self.app._warning.getvalue()

    @property
    def outdir(self):
        return Path(self.app.outdir)

    def html_tree(self, *path):
        path_page = self.outdir.joinpath(*path)
        if not path_page.exists():
            raise ValueError(f"{path_page} does not exist")
        return BeautifulSoup(path_page.read_text("utf8"), "html.parser")


@pytest.fixture()
def sphinx_build_factory(make_app, tmp_path):
    def _func(src_folder, **kwargs):
        copytree(path_tests / "sites" / src_folder, tmp_path / src_folder)
        app = make_app(srcdir=sphinx_path(tmp_path / src_folder), **kwargs)
        return SphinxBuild(app, tmp_path / src_folder)

    yield _func


def test_parallel_build():
    # We cannot use the sphinx_build_factory because SpinxTestApp does
    # not have a way to pass parallel=2 to the Sphinx constructor
    # https://github.com/sphinx-doc/sphinx/blob/d8c006f1c0e612d0dc595ae463b8e4c3ebee5ca4/sphinx/testing/util.py#L101
    check_call(
        f"sphinx-build -j 2 -W -b html {path_tests}/sites/parallel-build build",
        shell=True,
    )


def test_build_book(sphinx_build_factory, file_regression):
    """Test building the base book template and config."""
    sphinx_build = sphinx_build_factory("base")  # type: SphinxBuild
    sphinx_build.build(assert_pass=True)
    assert (sphinx_build.outdir / "index.html").exists(), sphinx_build.outdir.glob("*")

    # -- Notebooks ------------------------------------------------------------
    # Check for correct kernel name
    kernels_expected = {
        "ntbk.html": "python3",
        "ntbk_octave.html": "octave",
        "ntbk_julia.html": "julia-1.4",
    }
    for filename, kernel in kernels_expected.items():
        ntbk_html = sphinx_build.html_tree("section1", filename)
        thebe_config = ntbk_html.find("script", attrs={"type": "text/x-thebe-config"})
        kernel_name = 'name: "{}",'.format(kernel)
        if kernel_name not in thebe_config.prettify():
            raise AssertionError(f"{kernel_name} not in {kernels_expected}")

    # -- Sidebar --------------------------------------------------------------
    index_html = sphinx_build.html_tree("index.html")
    # Navigation entries
    if sphinx_build.software_versions == ".sphinx4":
        # Sphinx 4 adds some aria labeling that isn't in sphinx3, so just test sphinx4
        sidebar = index_html.find(attrs={"class": "bd-docs-nav"})
        file_regression.check(
            sidebar.prettify(),
            basename="build__sidebar-primary__nav",
            extension=".html",
            encoding="utf8",
        )

    # Check navbar numbering
    sidebar_ntbk = sphinx_build.html_tree("section1", "ntbk.html").find(
        "nav", attrs={"class": "bd-docs-nav"}
    )
    # Pages and sub-pages should be numbered
    assert "1. Page 1" in str(sidebar_ntbk)
    assert "3.1. Section 1 page1" in str(sidebar_ntbk)

    # -- Header ---------------------------------------------------------------
    header_article = sphinx_build.html_tree("section1", "ntbk.html").find(
        "div", class_="bd-header-article"
    )

    file_regression.check(
        header_article.prettify(),
        basename="build__header-article",
        extension=".html",
        encoding="utf8",
    )
    # Edit button should not be on page
    assert '<a class="edit-button"' not in str(index_html)
    # Title should be just text, no HTML
    assert "Index with code in title" in str(index_html)

    # -- Page TOC -------------------------------------------------------------
    # Test that the TOCtree is rendered properly across different title arrangements
    for page in sphinx_build.outdir.joinpath("titles").rglob("**/page-*"):
        page_html = BeautifulSoup(page.read_text("utf8"), "html.parser")
        page_toc = page_html.find("div", attrs={"class": "bd-toc"})
        if page_toc:
            file_regression.check(
                page_toc.prettify(),
                basename=f"build__pagetoc--{page.with_suffix('').name}",
                extension=".html",
                encoding="utf8",
            )
        else:
            # page with no subheadings now does not have the secondary sidebar markup
            assert len(page_html.find_all("section")) == 1


def test_navbar_options_home_page_in_toc(sphinx_build_factory):
    sphinx_build = sphinx_build_factory(
        "base", confoverrides={"html_theme_options.home_page_in_toc": True}
    ).build(assert_pass=True)  # type: SphinxBuild
    navbar = sphinx_build.html_tree("index.html").find(
        "nav", attrs={"class": "bd-docs-nav"}
    )
    # double checks if the master_doc has the current class
    li = navbar.find("li", attrs={"class": "current"})
    assert "Index with code in title" in str(li)


@pytest.mark.parametrize(
    "option,value",
    [
        ("extra_footer", "<div>EXTRA FOOTER</div>"),
    ],
)
def test_navbar_options(sphinx_build_factory, option, value):
    sphinx_build = sphinx_build_factory(
        "base", confoverrides={f"html_theme_options.{option}": value}
    ).build(assert_pass=True)  # type: SphinxBuild
    assert value in str(sphinx_build.html_tree("section1", "ntbk.html"))


@pytest.mark.parametrize(
    "edit,repo,issues,name",
    [
        (True, True, True, "all-on"),
        (True, False, False, "one-on"),
        (False, False, False, "all-off"),
    ],
)
def test_header_repository_buttons(
    sphinx_build_factory, file_regression, edit, repo, issues, name
):
    # All buttons on
    confoverrides = {
        "html_theme_options": {
            "use_edit_page_button": edit,
            "use_repository_button": repo,
            "use_issues_button": issues,
            "repository_url": "https://github.com/executablebooks/sphinx-book-theme",
            "navigation_with_keys": True,
        }
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build(
        assert_pass=True
    )

    header = sphinx_build.html_tree("section1", "ntbk.html").select(
        ".header-article-items__end"
    )
    file_regression.check(
        header[0].prettify(),
        basename=f"header__repo-buttons--{name}",
        extension=".html",
        encoding="utf8",
    )


@pytest.mark.parametrize(
    "provider, repo",
    [
        ("", "https://github.com/executablebooks/sphinx-book-theme"),
        ("github", "https://gh.mycompany.com/executablebooks/sphinx-book-theme"),
        ("", "https://gitlab.com/gitlab-org/gitlab"),
        ("", "https://opensource.ncsa.illinois.edu/bitbucket/scm/u3d/3dutilities"),
        ("gitlab", "https://mywebsite.com/gitlab/gitlab-org/gitlab"),
    ],
)
def test_source_button_url(sphinx_build_factory, file_regression, provider, repo):
    """Test that source button URLs are properly constructed."""
    # All buttons on
    use_issues = "github.com" in repo or "gitlab.com" in repo or provider == "gitlab"
    confoverrides = {
        "html_theme_options": {
            "repository_url": repo,
            "use_repository_button": True,
            "use_edit_page_button": True,
            "use_source_button": True,
            "use_issues_button": use_issues,
            "navigation_with_keys": True,
        }
    }
    # Decide if we've manually given the provider
    manual = provider != ""

    # Infer the provider from the names so we can name the regression tests
    if not provider:
        for iprov in ["github", "gitlab", "bitbucket"]:
            if iprov in repo:
                provider = iprov
                break

    provider_reg_file = provider
    if manual:
        confoverrides["html_theme_options"]["repository_provider"] = provider
        provider_reg_file = provider_reg_file + "_manual"

    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build(
        assert_pass=True
    )
    # Check that link of each button is correct, and that the icon has right provider
    links = sphinx_build.html_tree("section1", "ntbk.html").select(
        ".dropdown-source-buttons .dropdown-menu a"
    )
    icons = sphinx_build.html_tree("section1", "ntbk.html").select(
        ".dropdown-source-buttons .dropdown-menu i"
    )
    links = [ii["href"] for ii in links]
    icons = [str(ii) for ii in icons]
    check = "\n".join(["\n".join(ii) for ii in zip(links, icons)])
    file_regression.check(
        check,
        basename=f"header__source-buttons--{provider_reg_file}",
        extension=".html",
        encoding="utf8",
    )


def test_header_launchbtns(sphinx_build_factory, file_regression):
    """Test launch buttons."""
    sphinx_build = sphinx_build_factory("base").build(assert_pass=True)
    launch_btns = sphinx_build.html_tree("section1", "ntbk.html").select(
        ".dropdown-launch-buttons"
    )
    file_regression.check(launch_btns[0].prettify(), extension=".html", encoding="utf8")


def test_empty_header_launchbtns(sphinx_build_factory, file_regression):
    """Launch buttons should not show at all if no valid launch providers."""
    # Here we define part of the launch button config, but no valid provider
    sphinx_build = sphinx_build_factory(
        "base",
        confoverrides={
            "html_theme_options": {
                "launch_buttons": {"notebook_interface": "notebook"},
                "navigation_with_keys": True,
            }
        },
    ).build(assert_pass=True)
    launch_btns = sphinx_build.html_tree("section1", "ntbk.html").select(
        ".dropdown-launch-buttons"
    )
    assert len(launch_btns) == 0


@pytest.mark.parametrize(
    "provider, repo",
    [
        ("", "https://github.com/executablebooks/sphinx-book-theme"),
        ("", "https://gitlab.com/gitlab-org/gitlab"),
        ("", "https://opensource.ncsa.illinois.edu/bitbucket/scm/u3d/3dutilities"),
        ("gitlab", "https://mywebsite.com/gitlab/gitlab-org/gitlab"),
    ],
)
def test_launch_button_url(sphinx_build_factory, file_regression, provider, repo):
    """Test that source button URLs are properly constructed."""

    launch_buttons = {
        "binderhub_url": "https://mybinder.org",
        "jupyterhub_url": "https://hub.myorg.edu",
    }
    if "github.com" in repo:
        launch_buttons["colab_url"] = "https://colab.research.google.com"
        launch_buttons["deepnote_url"] = "https://deepnote.com"

    confoverrides = {
        "html_theme_options": {
            "repository_url": repo,
            "repository_branch": "foo",
            "path_to_docs": "docs",
            "launch_buttons": launch_buttons,
            "navigation_with_keys": True,
        }
    }

    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build(
        assert_pass=True
    )
    # Check that link of each button is correct
    all_links = []
    for ifile in (("section1", "ntbk.html"), ("section1", "ntbkmd.html")):
        links = sphinx_build.html_tree(*ifile).select(
            ".dropdown-launch-buttons .dropdown-menu a"
        )
        links = [ii["href"] for ii in links]
        all_links.append("/".join(ifile))
        all_links.append("\n".join(links) + "\n")

    if provider == "":
        provider = [ii for ii in ["github", "gitlab", "bitbucket"] if ii in repo][0]
    else:
        provider += "_manual"

    file_regression.check(
        "\n".join(all_links),
        basename=f"header__launch-buttons--{provider}",
        extension=".html",
        encoding="utf8",
    )


def test_repo_custombranch(sphinx_build_factory, file_regression):
    """Test custom branch for launch and edit buttons."""
    sphinx_build = sphinx_build_factory(
        "base",
        confoverrides={
            "html_theme_options": {
                "repository_branch": "foo",
                "use_edit_page_button": True,
                "repository_url": "https://github.com/executablebooks/sphinx-book-theme",  # noqa: E501
                "launch_buttons": {"binderhub_url": "https://mybinder.org"},
                "navigation_with_keys": True,
            }
        },
    ).build(assert_pass=True)
    header = sphinx_build.html_tree("section1", "ntbk.html").select(
        ".header-article-items__end"
    )
    # The Binder link should point to `foo`, as should the `edit` button
    file_regression.check(
        header[0].prettify(),
        basename="header__repo-buttons--custom-branch",
        extension=".html",
        encoding="utf8",
    )


@pytest.mark.skipif(os.name == "nt", reason="myst-nb path concatenation error (#212)")
def test_singlehtml(sphinx_build_factory):
    """Test building with a single HTML page."""
    sphinx_build = sphinx_build_factory("base", buildername="singlehtml").build(
        assert_pass=True
    )
    assert (sphinx_build.outdir / "index.html").exists(), sphinx_build.outdir.glob("*")


def test_docs_dirhtml(sphinx_build_factory):
    """Test that builds with dirhtml pass without error."""
    sphinx_build = sphinx_build_factory("base", buildername="dirhtml").build(
        assert_pass=True
    )
    assert (sphinx_build.outdir / "index.html").exists(), sphinx_build.outdir.glob("*")


def test_show_navbar_depth(sphinx_build_factory):
    """Test with different levels of show_navbar_depth."""
    sphinx_build = sphinx_build_factory(
        "base",
        confoverrides={
            "html_theme_options": {
                "show_navbar_depth": 2,
                "navigation_with_keys": True,
            }
        },
    ).build(assert_pass=True)  # type: SphinxBuild
    sidebar = sphinx_build.html_tree("section1", "ntbk.html").find_all(
        attrs={"class": "bd-sidebar"}
    )[0]
    for checkbox in sidebar.select("li.toctree-l1 > input"):
        assert "checked" in checkbox.attrs
    for checkbox in sidebar.select("li.toctree-l2 > input"):
        assert "checked" not in checkbox.attrs


def test_header_download_button_off(sphinx_build_factory):
    """Download button should not show up in the header when configured as False."""
    confoverrides = {
        "html_theme_options": {
            "use_download_button": False,
            "navigation_with_keys": True,
        }
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build(
        assert_pass=True
    )
    download_btns = sphinx_build.html_tree("section1", "ntbk.html").select(
        ".menu-dropdown-download-buttons"
    )
    assert len(download_btns) == 0


def test_header_fullscreen_button_off(sphinx_build_factory, file_regression):
    confoverrides = {
        "html_theme_options.use_fullscreen_button": False,
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build(
        assert_pass=True
    )

    fullscreen_buttons = sphinx_build.html_tree("section1", "ntbk.html").select(
        ".full-screen-button"
    )
    assert len(fullscreen_buttons) == 0


def test_right_sidebar_title(sphinx_build_factory, file_regression):
    confoverrides = {"html_theme_options.toc_title": "My test content title"}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build(
        assert_pass=True
    )

    sidebar_title = sphinx_build.html_tree("page1.html").find_all(
        "div", attrs={"class": "tocsection"}
    )[0]

    file_regression.check(sidebar_title.prettify(), extension=".html", encoding="utf8")

    # Testing the exception for empty title
    rmtree(str(sphinx_build.src))

    confoverrides = {"html_theme_options.toc_title": ""}


def test_sidenote(sphinx_build_factory, file_regression):
    confoverrides = {"html_theme_options.use_sidenotes": True}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build(
        assert_pass=True
    )

    page2 = sphinx_build.html_tree("page2.html")

    sidenote_html = page2.select("section > #sidenotes")
    regression_file = "test_sidenote_6" if sphinx_version.major < 7 else "test_sidenote"
    file_regression.check(
        sidenote_html[0].prettify(),
        extension=".html",
        encoding="utf8",
        basename=regression_file,
    )


def test_marginnote(sphinx_build_factory, file_regression):
    confoverrides = {"html_theme_options.use_sidenotes": True}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build(
        assert_pass=True
    )

    page2 = sphinx_build.html_tree("page2.html")

    marginnote_html = page2.select("section > #marginnotes")
    regression_file = (
        "test_marginnote_6" if sphinx_version.major < 7 else "test_marginnote"
    )
    file_regression.check(
        marginnote_html[0].prettify(),
        extension=".html",
        encoding="utf8",
        basename=regression_file,
    )
