# Changelog

## v0.0.38

## Enhancements made
👌 IMPROVE: Add missing aria-label to fullscreen button [#228](https://github.com/executablebooks/sphinx-book-theme/pull/228) ([@foster999](https://github.com/foster999))

👌 IMPROVE: declare parallel read safe [#225](https://github.com/executablebooks/sphinx-book-theme/pull/225) ([@rscohn2](https://github.com/rscohn2))

🐛 FIX: fixing dirhtml builds [#230](https://github.com/executablebooks/sphinx-book-theme/pull/230) ([@choldgraf](https://github.com/choldgraf))

🐛 FIX: fixing margin for code blocks [#229](https://github.com/executablebooks/sphinx-book-theme/pull/229) ([@choldgraf](https://github.com/choldgraf))


## v0.0.37

✨ NEW: Sphinx translations for all buttons and tooltips in major UI elements. See [the Sphinx i18n documentation](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language) for how to activate other languages. [#214](https://github.com/executablebooks/sphinx-book-theme/pull/214) ([@chrisjsewell](https://github.com/chrisjsewell))

⬆️  UPGRADE: pydata-sphinx-theme v0.4.0. See [the `pydata-sphinx-theme` changelog](https://github.com/pandas-dev/pydata-sphinx-theme/releases/tag/v0.4.0) for more information.

⬆️ UPGRADE: Use pyScss instead of libsass for scss compilation. This should make the theme more lightweight to install and develop locally. [#200](https://github.com/executablebooks/sphinx-book-theme/pull/200) ([@hason](https://github.com/hason))


### Contributors to this release
([GitHub contributors page for this release](https://github.com/executablebooks/sphinx-book-theme/graphs/contributors?from=2020-08-25&to=2020-09-28&type=c))

[@choldgraf](https://github.com/search?q=repo%3Aexecutablebooks%2Fsphinx-book-theme+involves%3Acholdgraf+updated%3A2020-08-25..2020-09-28&type=Issues) | [@chrisjsewell](https://github.com/search?q=repo%3Aexecutablebooks%2Fsphinx-book-theme+involves%3Achrisjsewell+updated%3A2020-08-25..2020-09-28&type=Issues) | [@fm75](https://github.com/search?q=repo%3Aexecutablebooks%2Fsphinx-book-theme+involves%3Afm75+updated%3A2020-08-25..2020-09-28&type=Issues) | [@hason](https://github.com/search?q=repo%3Aexecutablebooks%2Fsphinx-book-theme+involves%3Ahason+updated%3A2020-08-25..2020-09-28&type=Issues) | [@najuzilu](https://github.com/search?q=repo%3Aexecutablebooks%2Fsphinx-book-theme+involves%3Anajuzilu+updated%3A2020-08-25..2020-09-28&type=Issues) | [@nathancarter](https://github.com/search?q=repo%3Aexecutablebooks%2Fsphinx-book-theme+involves%3Anathancarter+updated%3A2020-08-25..2020-09-28&type=Issues) | [@pauleveritt](https://github.com/search?q=repo%3Aexecutablebooks%2Fsphinx-book-theme+involves%3Apauleveritt+updated%3A2020-08-25..2020-09-28&type=Issues) | [@pradyunsg](https://github.com/search?q=repo%3Aexecutablebooks%2Fsphinx-book-theme+involves%3Apradyunsg+updated%3A2020-08-25..2020-09-28&type=Issues) |

## v0.0.36 2020-08-25

👌 IMPROVED: The main theme change in this release, is the addition of CSS styling for definition lists, including those created by [sphinx.ext.autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html).
See [Definition and Field Lists](https://sphinx-book-theme.readthedocs.io/en/latest/reference/demo.html#definition-and-field-lists), and the [Python API documentation](https://sphinx-book-theme.readthedocs.io/en/latest/api/index.html).

🔧 MAINTENANCE: Under the hood, there has also been work undertaken to improve the development environment for working with the package. Thanks to [@pradyunsg](https://github.com/pradyunsg).

### Contributors to this release

[@chrisjsewell](https://github.com/chrisjsewell) | [@pradyunsg](https://github.com/pradyunsg)

## v0.0.34...v0.0.35
([full changelog](https://github.com/executablebooks/sphinx-book-theme/compare/v0.0.34...v0.0.35))

### Enhancements 👌

* Change "On this page" -> "Contents" [#159](https://github.com/executablebooks/sphinx-book-theme/pull/159) ([@pradyunsg](https://github.com/pradyunsg))
* Use consistent font size in toc [#157](https://github.com/executablebooks/sphinx-book-theme/pull/157) ([@pradyunsg](https://github.com/pradyunsg))
* Consistent font size in navigation [#156](https://github.com/executablebooks/sphinx-book-theme/pull/156) ([@pradyunsg](https://github.com/pradyunsg))

### Bugs fixed 🐛

* backref superscript [#171](https://github.com/executablebooks/sphinx-book-theme/pull/171) ([@AakashGfude](https://github.com/AakashGfude))
* Fixing sidebar overlap on narrow screens [#167](https://github.com/executablebooks/sphinx-book-theme/pull/167) ([@choldgraf](https://github.com/choldgraf))
* Fixing jupyterhub urls [#166](https://github.com/executablebooks/sphinx-book-theme/pull/166) ([@choldgraf](https://github.com/choldgraf))
* Create parent folders, when adding notebook to sources [#152](https://github.com/executablebooks/sphinx-book-theme/pull/152) ([@pradyunsg](https://github.com/pradyunsg))

### Documentation improvements 📚

* Adding contributing docs [#163](https://github.com/executablebooks/sphinx-book-theme/pull/163) ([@choldgraf](https://github.com/choldgraf))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/executablebooks/sphinx-book-theme/graphs/contributors?from=2020-08-05&to=2020-08-10&type=c))

[@AakashGfude](https://github.com/search?q=repo%3Aexecutablebooks%2Fsphinx-book-theme+involves%3AAakashGfude+updated%3A2020-08-05..2020-08-10&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Aexecutablebooks%2Fsphinx-book-theme+involves%3Acholdgraf+updated%3A2020-08-05..2020-08-10&type=Issues) | [@chrisjsewell](https://github.com/search?q=repo%3Aexecutablebooks%2Fsphinx-book-theme+involves%3Achrisjsewell+updated%3A2020-08-05..2020-08-10&type=Issues) | [@pradyunsg](https://github.com/search?q=repo%3Aexecutablebooks%2Fsphinx-book-theme+involves%3Apradyunsg+updated%3A2020-08-05..2020-08-10&type=Issues) | [@welcome](https://github.com/search?q=repo%3Aexecutablebooks%2Fsphinx-book-theme+involves%3Awelcome+updated%3A2020-08-05..2020-08-10&type=Issues)
