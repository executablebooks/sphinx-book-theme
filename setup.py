from setuptools import setup, find_packages
from pathlib import Path

lines = Path("sphinx_book_theme").joinpath("__init__.py")
for line in lines.read_text().split("\n"):
    if line.startswith("__version__ ="):
        version = line.split(" = ")[-1].strip('"')
        break

setup(
    name="sphinx-book-theme",
    version=version,
    python_requires=">=3.6",
    author="Project Jupyter Contributors",
    author_email="jupyter@googlegroups.com",
    url="https://jupyterbook.org/",
    project_urls={
        "Documentation": "https://jupyterbook.org",
        "Funding": "https://jupyter.org/about",
        "Source": "https://github.com/jupyter/jupyter-book/",
        "Tracker": "https://github.com/jupyter/jupyter-book/issues",
    },
    # this should be a whitespace separated string of keywords, not a list
    keywords="reproducible science environments scholarship notebook",
    description="Jupyter Book: Create an online book with Jupyter Notebooks",
    long_description=Path("./README.md").read_text(),
    long_description_content_type="text/markdown",
    license="BSD",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "docutils>=0.15",
        "sphinx",
        "click",
        "pydata-sphinx-theme~=0.4.0",
        "beautifulsoup4",
        'importlib-resources~=3.0.0; python_version < "3.7"',
    ],
    extras_require={
        "code_style": ["pre-commit~=2.7.0"],
        "sphinx": [
            "folium",
            "numpy",
            "matplotlib",
            "ipywidgets",
            "pandas",
            "nbclient",
            "myst-nb~=0.10.1",
            "sphinx-togglebutton>=0.2.1",
            "sphinx-copybutton",
            "plotly",
            "sphinxcontrib-bibtex",
            "sphinx-thebe",
        ],
        "testing": [
            "myst_nb~=0.10.1",
            "sphinx_thebe",
            "coverage",
            "pytest~=6.0.1",
            "pytest-cov",
            "pytest-regressions~=2.0.1",
        ],
        "live-dev": ["sphinx-autobuild", "web-compile~=0.2.1"],
    },
    entry_points={"sphinx.html_themes": ["sphinx_book_theme = sphinx_book_theme"]},
    include_package_data=True,
)
