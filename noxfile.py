import logging
import os
import subprocess
import time
from contextlib import contextmanager

import nox

nox.options.reuse_existing_virtualenvs = True  # make the overall workflow faster


@contextmanager
def in_the_background(session, executable_name, *args):
    logging.info(" ".join([executable_name, *args]))

    executable = os.path.join(session.virtualenv.bin, executable_name)
    command = [executable, *args]

    with subprocess.Popen(command):
        time.sleep(1)  # give a second for any initial output
        yield


@nox.session(python=["3.6", "3.7", "3.8"])
def tests(session):
    """Enforce code-style with appropriately configured linters."""
    session.install(".[sphinx,testing]")
    session.run("pytest", *session.posargs)


@nox.session
def lint(session):
    """Enforce code-style with appropriately configured linters."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session(name="compile-scss")
def compile_scss(session):
    """Compile .scss files into the correct .css file."""
    session.install("boussole")
    session.run("boussole", "compile", "--config", ".boussole.json")


@nox.session
def docs(session):
    """Build documentation for this project."""
    session.install(".[sphinx]")
    session.run(
        "sphinx-build", "-nW", "--keep-going", "-b", "html", "docs", "docs/_build/html"
    )

    session.notify("compile-scss")


@nox.session(name="docs-live")
def docs_live(session):
    """Serve documentation for this project, with live-reloading for development."""
    session.install("-e", ".[sphinx]", "boussole", "sphinx-autobuild")

    background_command = ["boussole", "watch", "--config", ".boussole.json"]
    with in_the_background(session, *background_command):
        # fmt: off
        session.run(
            "sphinx-autobuild",
            # scss files are handled by boussole
            "--ignore", "*.scss",
            "--re-ignore", "_build/.*",
            # regenerate for all modifications in sphinx_book_theme/
            "--watch", "sphinx_book_theme",
            # open the browser after 5 seconds
            "--open-browser",
            # sphinx-build arguments
            "-a", "-n", "-b", "html", "docs", "docs/_build/html",
        )
        # fmt: on
