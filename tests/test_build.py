from bs4 import BeautifulSoup
from pathlib import Path
from subprocess import run
from shutil import copytree, rmtree
import pytest


path_tests = Path(__file__).parent.resolve()
path_base = path_tests.joinpath("sites", "base")


@pytest.fixture(scope="session")
def sphinx_build(tmpdir_factory):
    class SphinxBuild:
        path_tmp = Path(tmpdir_factory.mktemp("build"))
        path_book = path_tmp.joinpath("book")
        path_build = path_book.joinpath("_build")
        path_html = path_build.joinpath("html")
        path_pg_index = path_html.joinpath("index.html")
        path_pg_ntbk = path_html.joinpath("section1", "ntbk.html")
        cmd_base = ["sphinx-build", ".", "_build/html", "-a", "-W"]

        def copy(self, path=None):
            """Copy the specified book to our tests folder for building."""
            if path is None:
                path = path_base
            if not self.path_book.exists():
                copytree(path, self.path_book)

        def build(self, cmd=None):
            """Build the test book"""
            cmd = [] if cmd is None else cmd
            run(self.cmd_base + cmd, cwd=self.path_book, check=True)

        def clean(self):
            """Clean the _build folder so files don't clash with new tests."""
            rmtree(self.path_build)

    return SphinxBuild()


def test_build_book(file_regression, sphinx_build):
    """Test building the base book template and config."""
    sphinx_build.copy()

    # Basic build with defaults
    sphinx_build.build()
    assert sphinx_build.path_pg_index.exists()

    # Check interact links for both ipynb and myst-nb
    for path in ["section1/ntbk.ipynb", "section1/ntbkmd.md"]:
        path_ntbk = sphinx_build.path_html.joinpath(*path.split("/"))
        ntbk_text = path_ntbk.with_suffix(".html").read_text()
        assert (
            f"https://mybinder.org/v2/gh/executablebooks/sphinx-book-theme/master?urlpath=lab/tree/TESTPATH/{path}"  # noqa E501
            in ntbk_text
        )
        assert (
            f"https://datahub.berkeley.edu/hub/user-redirect/git-pull?repo=https://github.com/executablebooks/sphinx-book-theme&urlpath=lab/tree/sphinx-book-theme/TESTPATH/{path}"  # noqa E501
            in ntbk_text
        )
        assert (
            f"https://colab.research.google.com/github/executablebooks/sphinx-book-theme/blob/master/TESTPATH/{path}"  # noqa E501
            in ntbk_text
        )

    # Check for correct kernel name in jupyter notebooks
    kernels_expected = {
        "section1/ntbk.ipynb": "python3",
        "section1/ntbk_octave.ipynb": "octave",
        "section1/ntbk_julia.ipynb": "julia-1.4",
    }
    for path, kernel in kernels_expected.items():
        path_ntbk = sphinx_build.path_html.joinpath(*path.split("/"))
        ntbk_text = path_ntbk.with_suffix(".html").read_text()
        assert 'kernelName: "{}",'.format(kernel) in ntbk_text

    # Check a few components that should be true on each page
    index_text = sphinx_build.path_pg_index.read_text()
    index_html = BeautifulSoup(index_text, "html.parser")
    sidebar = index_html.find_all(attrs={"class": "bd-sidebar"})[0]
    # Index should *not* be in navbar
    assert "Index</a>" not in index_text
    # Captions make it into navbar
    assert '<p class="margin-caption">My caption</p>' in index_text
    # Opengraph should not be in the HTML because we have no baseurl specified
    assert (
        '<meta property="og:url"         content="https://blah.com/foo/section1/ntbk.html" />'  # noqa E501
        not in index_text
    )
    # Edit button should not be on page
    assert '<a class="edit-button"' not in index_text
    # Sub-sections shouldn't be in the TOC because we haven't expanded it yet
    assert "Section 1 page1</a>" not in str(sidebar)
    sphinx_build.clean()


def test_navbar_options(file_regression, sphinx_build):
    sphinx_build.copy()

    # Check navbar numbering
    cmd = ["-D", "html_theme_options.number_toc_sections=True"]
    sphinx_build.build(cmd)
    ntbk_text = BeautifulSoup(sphinx_build.path_pg_ntbk.read_text(), "html.parser")
    navbar = ntbk_text.find("nav", id="bd-docs-nav")
    # Pages and sub-pages should be numbered
    assert "1. Page 1</a>" in str(navbar)
    assert "3.1 Section 1 page1</a>" in str(navbar)
    sphinx_build.clean()

    # "home_page_in_toc": True,
    cmd = ["-D", "html_theme_options.home_page_in_toc=True"]
    sphinx_build.build(cmd)
    ntbk_text = BeautifulSoup(sphinx_build.path_pg_ntbk.read_text(), "html.parser")
    navbar = ntbk_text.find("nav", id="bd-docs-nav")
    assert "Index</a>" in str(navbar)
    sphinx_build.clean()

    # "single_page": True
    cmd = ["-D", "html_theme_options.single_page=True"]
    sphinx_build.build(cmd)
    ntbk_text = BeautifulSoup(sphinx_build.path_pg_ntbk.read_text(), "html.parser")
    sidebar = ntbk_text.find("div", id="site-navigation")
    assert len(sidebar.find_all("div")) == 0
    assert "col-md-2" in sidebar.attrs["class"]
    sphinx_build.clean()

    # Test extra navbar
    cmd = ["-D", "html_theme_options.extra_navbar='<div>EXTRA NAVBAR</div>'"]
    sphinx_build.build(cmd)
    ntbk_text = sphinx_build.path_pg_ntbk.read_text()
    assert "<div>EXTRA NAVBAR</div>" in ntbk_text
    sphinx_build.clean()

    # Test extra navbar deprecated key
    cmd = [
        "-D",
        "html_theme_options.navbar_footer_text='<div>EXTRA NAVBAR</div>'",
    ]
    sphinx_build.build(cmd)
    ntbk_text = sphinx_build.path_pg_ntbk.read_text()
    assert "<div>EXTRA NAVBAR</div>" in ntbk_text
    sphinx_build.clean()

    # Test extra footer
    cmd = ["-D", "html_theme_options.extra_footer='<div>EXTRA FOOTER</div>'"]
    sphinx_build.build(cmd)
    ntbk_text = sphinx_build.path_pg_ntbk.read_text()
    assert "<div>EXTRA FOOTER</div>" in ntbk_text
    sphinx_build.clean()

    # Explicitly expanded sections are expanded when not active
    cmd = ["-D", "html_theme_options.expand_sections=section1/index"]
    sphinx_build.build(cmd)
    ntbk_text = BeautifulSoup(sphinx_build.path_pg_ntbk.read_text(), "html.parser")
    sidebar = ntbk_text.find_all(attrs={"class": "bd-sidebar"})[0]
    assert "Section 1 page1</a>" in str(sidebar)
    sphinx_build.clean()


def test_header_info(file_regression, sphinx_build):
    sphinx_build.copy()

    # opengraph is generated when baseurl is given
    baseurl = "https://blah.com/foo/"
    path_logo = path_tests.parent.joinpath("docs", "_static", "logo.png")
    cmd = ["-D", f"html_baseurl={baseurl}", "-D", f"html_logo={path_logo}"]
    sphinx_build.build(cmd)

    ntbk_text = BeautifulSoup(sphinx_build.path_pg_ntbk.read_text(), "html.parser")
    header = ntbk_text.find("head")
    assert (
        '<meta content="https://blah.com/foo/section1/ntbk.html" property="og:url">'
        in str(header)
    )
    assert (
        '<meta content="https://blah.com/foo/_static/logo.png" property="og:image"/>'
        in str(header)
    )
    sphinx_build.clean()


def test_topbar(file_regression, sphinx_build):
    sphinx_build.copy()

    # Test source buttons edit button
    cmd = [
        "-D",
        "html_theme_options.use_edit_page_button=True",
        "-D",
        "html_theme_options.use_repository_button=True",
        "-D",
        "html_theme_options.use_issues_button=True",
    ]
    sphinx_build.build(cmd)
    ntbk_text = BeautifulSoup(sphinx_build.path_pg_ntbk.read_text(), "html.parser")
    source_btns = ntbk_text.find_all("div", attrs={"class": "sourcebuttons"})[0]
    file_regression.check(source_btns.prettify(), extension=".html")
    sphinx_build.clean()

    # Test that turning buttons off works
    cmd = [
        "-D",
        "html_theme_options.use_edit_page_button=False",
        "-D",
        "html_theme_options.use_repository_button=False",
        "-D",
        "html_theme_options.use_issues_button=True",
    ]
    sphinx_build.build(cmd)
    ntbk_text = BeautifulSoup(sphinx_build.path_pg_ntbk.read_text(), "html.parser")
    source_btns = ntbk_text.find_all("div", attrs={"class": "sourcebuttons"})[0]
    file_regression.check(
        source_btns.prettify(), basename="test_topbar_hidebtns", extension=".html"
    )
    sphinx_build.clean()
