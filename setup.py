from setuptools import setup, find_packages
import os
import os.path as op
from glob import glob
from pathlib import Path

version = [
    line
    for line in Path("sphinx_book_theme/__init__.py").read_text().split()
    if "__version__" in line
]
version = version[0].split(" = ")[-1]

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
    long_description=open("./README.md", "r").read(),
    long_description_content_type="text/markdown",
    license="BSD",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "docutils>=0.15",
        "sphinx",
        "click",
        "setuptools",
        "libsass",
        (
            "pandas_sphinx_theme @ "
            "https://github.com/pandas-dev/pydata-bootstrap-sphinx-theme/archive/master.zip"
        ),
    ],
    extras_require={
        "sphinx": [
            "folium",
            "numpy",
            "matplotlib",
            "ipywidgets",
            "pandas",
            "nbclient",
            (
                "myst_parser @ "
                "https://github.com/ExecutableBookProject/myst_parser/archive/master.zip"
            ),
            (
                "myst_nb @ "
                "https://github.com/ExecutableBookProject/myst-nb/archive/master.zip"
            ),
        ],
        "testing": ["coverage", "pytest>=3.6,<4", "pytest-cov", "beautifulsoup4"],
    },
    entry_points={"sphinx.html_themes": ["sphinx_book_theme = sphinx_book_theme"]},
    package_data={
        "sphinx_book_theme": ["theme.conf", "*.html", "static/*", "static/images/*"]
    },
    include_package_data=True,
)
