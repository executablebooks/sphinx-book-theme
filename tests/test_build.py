from bs4 import BeautifulSoup
from pathlib import Path
from subprocess import run
from shutil import copytree, rmtree


path_tests = Path(__file__).parent.resolve()
path_base = path_tests.joinpath("sites", "base")


def test_build_book(tmpdir):
    """Test building the book template and a few test configs."""
    # Copy over the base build content and config to tmpdir
    path_tmpdir = Path(tmpdir)
    copytree(path_base, path_tmpdir.joinpath(path_base.name))
    path_tmp_base = path_tmpdir.joinpath("base")

    cmd_base = ["sphinx-build", ".", "_build/html", "-a", "-W"]
    run(cmd_base, cwd=path_tmp_base, check=True)

    path_build = path_tmp_base.joinpath("_build")
    path_html = path_build.joinpath("html")
    path_index = path_html.joinpath("index.html")
    assert path_index.exists()

    # Check interact links for both ipynb and myst-nb
    for path in ["section1/ntbk.ipynb", "section1/ntbkmd.md"]:
        path_ntbk = path_html.joinpath(*path.split("/"))
        ntbk_text = path_ntbk.with_suffix(".html").read_text()
        assert (
            f"https://mybinder.org/v2/gh/ExecutableBookProject/sphinx-book-theme/master?urlpath=lab/tree/TESTPATH/{path}"  # noqa E501
            in ntbk_text
        )
        assert (
            f"https://datahub.berkeley.edu/hub/user-redirect/git-pull?repo=https://github.com/ExecutableBookProject/sphinx-book-theme&urlpath=lab/tree/sphinx-book-theme/TESTPATH/{path}"  # noqa E501
            in ntbk_text
        )

    # Check for correct kernel name in jupyter notebooks
    kernels_expected = {
        "section1/ntbk.ipynb": "python3",
        "section1/ntbk_octave.ipynb": "octave",
        "section1/ntbk_julia.ipynb": "julia-1.4",
    }
    for path, kernel in kernels_expected.items():
        path_ntbk = path_html.joinpath(*path.split("/"))
        ntbk_text = path_ntbk.with_suffix(".html").read_text()
        assert 'kernelName: "{}",'.format(kernel) in ntbk_text

    # Check a few components that should be true on each page
    path_index = path_html.joinpath("index.html")
    index_text = path_index.read_text()
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
    rmtree(path_build)

    # Check navbar numbering
    cmd = cmd_base + ["-D", "html_theme_options.number_toc_sections=True"]
    run(cmd, cwd=path_tmp_base, check=True)
    path_ntbk = path_html.joinpath("section1", "ntbk.html")
    ntbk_text = BeautifulSoup(path_ntbk.read_text(), "html.parser")
    navbar = ntbk_text.find("nav", id="bd-docs-nav")
    # Pages and sub-pages should be numbered
    assert "1. Page 1</a>" in str(navbar)
    assert "3.1 Section 1 page1</a>" in str(navbar)

    rmtree(path_build)

    # "home_page_in_toc": True,
    cmd = cmd_base + ["-D", "html_theme_options.home_page_in_toc=True"]
    run(cmd, cwd=path_tmp_base, check=True)
    ntbk_text = BeautifulSoup(path_ntbk.read_text(), "html.parser")
    navbar = ntbk_text.find("nav", id="bd-docs-nav")
    assert "Index</a>" in str(navbar)
    rmtree(path_build)

    # "single_page": True
    cmd = cmd_base + ["-D", "html_theme_options.single_page=True"]
    run(cmd, cwd=path_tmp_base, check=True)
    ntbk_text = BeautifulSoup(path_ntbk.read_text(), "html.parser")
    sidebar = ntbk_text.find("div", id="site-navigation")
    assert len(sidebar.find_all("div")) == 0
    rmtree(path_build)

    # opengraph is generated when baseurl is given
    baseurl = "https://blah.com/foo/"
    path_logo = path_tests.parent.joinpath("docs", "_static", "logo.png")
    cmd = cmd_base + ["-D", f"html_baseurl={baseurl}", "-D", f"html_logo={path_logo}"]
    run(cmd, cwd=path_tmp_base, check=True)
    ntbk_text = BeautifulSoup(path_ntbk.read_text(), "html.parser")
    header = ntbk_text.find("head")
    assert (
        '<meta content="https://blah.com/foo/section1/ntbk.html" property="og:url">'
        in str(header)
    )
    assert (
        '<meta content="https://blah.com/foo/_static/logo.png" property="og:image"/>'
        in str(header)
    )
    rmtree(path_build)

    # Test edit button
    cmd = cmd_base + ["-D", "html_theme_options.use_edit_page_button=True"]
    run(cmd, cwd=path_tmp_base, check=True)
    ntbk_text = path_ntbk.read_text()
    assert (
        '<a class="edit-button" href="https://github.com/ExecutableBookProject/sphinx-book-theme/edit/master/TESTPATH/section1/ntbk.ipynb">'  # noqa E501
        in ntbk_text
    )
    rmtree(path_build)

    # Explicitly expanded sections are expanded when not active
    cmd = cmd_base + ["-D", "html_theme_options.expand_sections=section1/index"]
    run(cmd, cwd=path_tmp_base, check=True)
    ntbk_text = BeautifulSoup(path_ntbk.read_text(), "html.parser")
    sidebar = ntbk_text.find_all(attrs={"class": "bd-sidebar"})[0]
    assert "Section 1 page1</a>" in str(sidebar)
    rmtree(path_build)
