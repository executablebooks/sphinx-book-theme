from bs4 import BeautifulSoup
from pathlib import Path
from subprocess import check_output
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
            return check_output(self.cmd_base + cmd, cwd=self.path_book).decode("utf8")

        def path(self, *args):
            return self.path_html.joinpath(*args)

        def get(self, *args):
            path_page = self.path(*args)
            if not path_page.exists():
                raise ValueError(f"{path_page} does not exist")
            return BeautifulSoup(path_page.read_text(), "html.parser")

        def clean(self):
            """Clean the _build folder so files don't clash with new tests."""
            rmtree(self.path_build)

    return SphinxBuild()


def test_build_book(file_regression, sphinx_build):
    """Test building the base book template and config."""
    sphinx_build.copy()

    # Basic build with defaults
    sphinx_build.build()
    assert sphinx_build.path("index.html").exists()

    # Check for correct kernel name in jupyter notebooks
    kernels_expected = {
        "section1/ntbk.html": "python3",
        "section1/ntbk_octave.html": "octave",
        "section1/ntbk_julia.html": "julia-1.4",
    }
    for path, kernel in kernels_expected.items():
        ntbk_text = sphinx_build.get(*path.split("/"))
        thebe_config = ntbk_text.find("script", attrs={"type": "text/x-thebe-config"})
        kernel_name = 'kernelName: "{}",'.format(kernel)
        if kernel_name not in thebe_config.prettify():
            raise AssertionError(f"{kernel_name} not in {kernels_expected}")

    # Check a few components that should be true on each page
    index_html = sphinx_build.get("index.html")
    sidebar = index_html.find_all(attrs={"class": "bd-sidebar"})[0]
    file_regression.check(sidebar.prettify(), extension=".html")

    # Opengraph should not be in the HTML because we have no baseurl specified
    assert (
        '<meta property="og:url"         content="https://blah.com/foo/section1/ntbk.html" />'  # noqa E501
        not in str(index_html)
    )
    # Edit button should not be on page
    assert '<a class="edit-button"' not in str(index_html)
    # Title should be just text, no HTML
    assert "Index with code in title" in str(index_html)
    # Check navbar numbering
    sidebar_ntbk = sphinx_build.get("section1", "ntbk.html").find(
        "nav", id="bd-docs-nav"
    )
    # Pages and sub-pages should be numbered
    assert "1. Page 1" in str(sidebar_ntbk)
    assert "3.1. Section 1 page1" in str(sidebar_ntbk)
    # Check opengraph metadata
    html_escaped = sphinx_build.get("page1.html")
    escaped_description = html_escaped.find("meta", property="og:description")
    file_regression.check(
        escaped_description.prettify(),
        basename="escaped_description",
        extension=".html",
    )
    sphinx_build.clean()


def test_navbar_options(file_regression, sphinx_build):
    sphinx_build.copy()

    # "home_page_in_toc": True,
    cmd = ["-D", "html_theme_options.home_page_in_toc=True"]
    sphinx_build.build(cmd)
    navbar = sphinx_build.get("section1", "ntbk.html").find("nav", id="bd-docs-nav")
    assert "Index with code in title" in str(navbar)
    sphinx_build.clean()

    # "single_page": True
    cmd = ["-D", "html_theme_options.single_page=True"]
    sphinx_build.build(cmd)
    sidebar = sphinx_build.get("section1", "ntbk.html").find(
        "div", id="site-navigation"
    )
    assert len(sidebar.find_all("div")) == 0
    assert "col-md-2" in sidebar.attrs["class"]
    sphinx_build.clean()

    # Test extra navbar
    cmd = ["-D", "html_theme_options.extra_navbar='<div>EXTRA NAVBAR</div>'"]
    sphinx_build.build(cmd)
    assert "<div>EXTRA NAVBAR</div>" in str(sphinx_build.get("section1", "ntbk.html"))
    sphinx_build.clean()

    # Test extra navbar deprecated key
    cmd = [
        "-D",
        "html_theme_options.navbar_footer_text='<div>EXTRA NAVBAR</div>'",
    ]
    sphinx_build.build(cmd)
    assert "<div>EXTRA NAVBAR</div>" in str(sphinx_build.get("section1", "ntbk.html"))
    sphinx_build.clean()

    # Test extra footer
    cmd = ["-D", "html_theme_options.extra_footer='<div>EXTRA FOOTER</div>'"]
    sphinx_build.build(cmd)
    assert "<div>EXTRA FOOTER</div>" in str(sphinx_build.get("section1", "ntbk.html"))
    sphinx_build.clean()

    # Explicitly expanded sections are expanded when not active
    cmd = ["-D", "html_theme_options.expand_sections=section1/index"]
    sphinx_build.build(cmd)
    sidebar = sphinx_build.get("section1", "ntbk.html").find_all(
        attrs={"class": "bd-sidebar"}
    )[0]
    assert "Section 1 page1" in str(sidebar)
    sphinx_build.clean()


def test_header_info(file_regression, sphinx_build):
    sphinx_build.copy()

    # opengraph is generated when baseurl is given
    baseurl = "https://blah.com/foo/"
    path_logo = path_tests.parent.joinpath("docs", "_static", "logo.png")
    cmd = ["-D", f"html_baseurl={baseurl}", "-D", f"html_logo={path_logo}"]
    sphinx_build.build(cmd)

    header = sphinx_build.get("section1", "ntbk.html").find("head")
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
    source_btns = sphinx_build.get("section1", "ntbk.html").find_all(
        "div", attrs={"class": "sourcebuttons"}
    )[0]
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
    source_btns = sphinx_build.get("section1", "ntbk.html").find_all(
        "div", attrs={"class": "sourcebuttons"}
    )[0]
    file_regression.check(
        source_btns.prettify(), basename="test_topbar_hidebtns", extension=".html"
    )
    sphinx_build.clean()

    # Test launch buttons
    sphinx_build.build()
    launch_btns = sphinx_build.get("section1", "ntbk.html").find_all(
        "div", attrs={"class": "dropdown-buttons"}
    )[1]
    file_regression.check(
        launch_btns.prettify(), basename="test_topbar_launchbtns", extension=".html"
    )
    sphinx_build.clean()

    # Test custom branch for launch buttons
    cmd = [
        "-D",
        "html_theme_options.repository_branch=foo",
    ]
    sphinx_build.build(cmd)
    launch_btns = sphinx_build.get("section1", "ntbk.html").find_all(
        "div", attrs={"class": "dropdown-buttons"}
    )[1]
    file_regression.check(
        launch_btns.prettify(), basename="test_repo_custombranch", extension=".html"
    )
    sphinx_build.clean()


def test_singlehtml(file_regression, sphinx_build):
    """Test building with a single HTML page."""
    sphinx_build.copy()

    # Ensure that it works without error
    cmd = ["-b", "singlehtml"]
    check_output(sphinx_build.cmd_base + cmd, cwd=sphinx_build.path_book).decode("utf8")
