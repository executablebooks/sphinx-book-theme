import os
from pathlib import Path
from shutil import copytree, rmtree
from subprocess import check_call

from bs4 import BeautifulSoup
import pytest
import sphinx
from sphinx.testing.util import SphinxTestApp
from sphinx.testing.path import path as sphinx_path


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
        app = make_app(
            srcdir=sphinx_path(os.path.abspath((tmp_path / src_folder))), **kwargs
        )
        return SphinxBuild(app, tmp_path / src_folder)

    yield _func


def test_parallel_build():
    # We cannot use the sphinx_build_factory because SpinxTestApp does
    # not have a way to pass parallel=2 to the Sphinx constructor
    # https://github.com/sphinx-doc/sphinx/blob/d8c006f1c0e612d0dc595ae463b8e4c3ebee5ca4/sphinx/testing/util.py#L101
    check_call(
        "sphinx-build -j 2 -W -b html tests/sites/parallel-build build", shell=True
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
        kernel_name = 'kernelName: "{}",'.format(kernel)
        if kernel_name not in thebe_config.prettify():
            raise AssertionError(f"{kernel_name} not in {kernels_expected}")

    # -- Sidebar --------------------------------------------------------------
    index_html = sphinx_build.html_tree("index.html")
    # Navigation entries
    if sphinx_build.software_versions == ".sphinx4":
        # Sphinx 4 adds some aria labeling that isn't in sphinx3, so just test sphinx4
        sidebar = index_html.find(attrs={"id": "bd-docs-nav"})
        file_regression.check(
            sidebar.prettify(),
            basename="build__sidebar-primary__nav",
            extension=".html",
            encoding="utf8",
        )

    # Check navbar numbering
    sidebar_ntbk = sphinx_build.html_tree("section1", "ntbk.html").find(
        "nav", id="bd-docs-nav"
    )
    # Pages and sub-pages should be numbered
    assert "1. Page 1" in str(sidebar_ntbk)
    assert "3.1. Section 1 page1" in str(sidebar_ntbk)

    # -- Header ---------------------------------------------------------------
    header_article = sphinx_build.html_tree("section1", "ntbk.html").find(
        "div", class_="header-article"
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
        file_regression.check(
            page_toc.prettify(),
            basename=f"build__pagetoc--{page.with_suffix('').name}",
            extension=".html",
            encoding="utf8",
        )


def test_navbar_options_home_page_in_toc(sphinx_build_factory):

    sphinx_build = sphinx_build_factory(
        "base", confoverrides={"html_theme_options.home_page_in_toc": True}
    ).build(
        assert_pass=True
    )  # type: SphinxBuild
    navbar = sphinx_build.html_tree("index.html").find("nav", id="bd-docs-nav")
    # double checks if the master_doc has the current class
    li = navbar.find("li", attrs={"class": "current"})
    assert "Index with code in title" in str(li)


def test_navbar_options_single_page(sphinx_build_factory):
    """Test that"""
    sphinx_build = sphinx_build_factory(
        "base", confoverrides={"html_theme_options.single_page": True}
    ).build(
        assert_pass=True
    )  # type: SphinxBuild
    sidebar = sphinx_build.html_tree("section1", "ntbk.html").find(
        "div", id="site-navigation"
    )
    assert len(sidebar.find_all("div")) == 0  # Sidebar should be empty
    assert "single-page" in sidebar.attrs["class"]  # Class added on single page


@pytest.mark.parametrize(
    "option,value",
    [
        ("extra_navbar", "<div>EXTRA NAVBAR</div>"),
        ("navbar_footer_text", "<div>EXTRA NAVBAR</div>"),
        ("extra_footer", "<div>EXTRA FOOTER</div>"),
    ],
)
def test_navbar_options(sphinx_build_factory, option, value):
    sphinx_build = sphinx_build_factory(
        "base", confoverrides={f"html_theme_options.{option}": value}
    ).build(
        assert_pass=True
    )  # type: SphinxBuild
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
        }
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build(
        assert_pass=True
    )

    header = sphinx_build.html_tree("section1", "ntbk.html").select(
        ".header-article__right"
    )
    file_regression.check(
        header[0].prettify(),
        basename=f"header__repo-buttons--{name}",
        extension=".html",
        encoding="utf8",
    )


def test_header_launchbtns(sphinx_build_factory, file_regression):
    """Test launch buttons."""
    sphinx_build = sphinx_build_factory("base").build(assert_pass=True)
    launch_btns = sphinx_build.html_tree("section1", "ntbk.html").select(
        ".menu-dropdown-launch-buttons"
    )
    file_regression.check(launch_btns[0].prettify(), extension=".html", encoding="utf8")


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
            }
        },
    ).build(assert_pass=True)
    header = sphinx_build.html_tree("section1", "ntbk.html").select(
        ".header-article__right"
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
        confoverrides={"html_theme_options.show_navbar_depth": 2},
    ).build(
        assert_pass=True
    )  # type: SphinxBuild
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
        "html_theme_options.use_download_button": False,
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
    confoverrides = {"html_theme_options.toc_title": "My Contents"}
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


def test_logo_only(sphinx_build_factory):
    confoverrides = {"html_theme_options.logo_only": True}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build(
        assert_pass=True
    )

    logo_text = sphinx_build.html_tree("page1.html").find_all(
        "h1", attrs={"id": "site-title"}
    )
    assert not logo_text
