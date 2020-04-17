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

    # Check a few components that should be true on each page
    path_index = path_html.joinpath("index.html")
    index_text = path_index.read_text()
    # Index should *not* be in navbar
    assert "Index</a>" not in index_text
    # Captions make it into navbar
    assert '<p class="margin-caption">My caption</p>' in index_text
    # Explicitly expanded sections are expanded when not active
    assert "Section 1 page1</a>" in index_text
    rmtree(path_build)

    # Check navbar numbering
    cmd = cmd_base + ["-D", "html_theme_options.number_toc_sections=True"]
    run(cmd, cwd=path_tmp_base, check=True)
    path_ntbk = path_html.joinpath("section1", "ntbk.html")
    ntbk_text = path_ntbk.read_text()
    # Pages and sub-pages should be numbered
    assert "1. Page 1</a>" in ntbk_text
    assert "1. Section 1 page1</a>" in ntbk_text
    rmtree(path_build)

    # "home_page_in_toc": True,
    cmd = cmd_base + ["-D", "html_theme_options.home_page_in_toc=True"]
    run(cmd, cwd=path_tmp_base, check=True)
    ntbk_text = path_ntbk.read_text()
    assert "Index</a>" in ntbk_text
    rmtree(path_build)

    # "single_page": True
    cmd = cmd_base + ["-D", "html_theme_options.single_page=True"]
    run(cmd, cwd=path_tmp_base, check=True)
    ntbk_text = path_ntbk.read_text()
    assert 'id="site-navigation"' not in ntbk_text
    rmtree(path_build)
