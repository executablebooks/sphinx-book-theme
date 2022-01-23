# Book Theme translations

This folder contains code and translations for supporting multiple languages with Sphinx.
See [the Sphinx internationalization documentation](https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-internationalization) for more details.

## Structure of this folder

- `jsons/` contains a collection of JSON files that were originally created with [the smodin.io language translator](https://smodin.me/translate-one-text-into-multiple-languages)
- `locales/` contains Sphinx locale files that were auto-converted from the files in `jsons/` by `_convert.py`
- `_convert.py` is a helper script to auto-generate Sphinx locale files from the JSONs in `jsons/`.

## Workflow of translations

Here's a short workflow of how to add a new translation, assuming that you are translating using the [smodin.io service](https://smodin.io/translate-one-text-into-multiple-languages).

1. Go to [the smodin.io service](https://smodin.io/translate-one-text-into-multiple-languages)
2. Select as many languages as you like.
3. Type in the phrase you'd like to translate.
4. Click `TRANSLATE` and then `Download JSON`.
5. This will download a JSON file with a bunch of `language-code: translated-phrase` mappings.
6. Put this JSON in the `jsons/` folder, and rename it to be the phrase you've translated in English.
   So if the original phrase is `My phrase`, you should name the file `My phrase.json`.
7. Run [the `prettier` formatter](https://prettier.io/) on this JSON to split it into multiple lines (this makes it easier to read and edit if translations should be updated)

   ```bash
   prettier sphinx_book_theme/translations/jsons/<message name>.json
   ```

8. Run `python sphinx_book_theme/translations/_convert.py`
9. This will generate the locale files (`.mo`) that Sphinx uses in its translation machinery, and put them in `locales/<language-code>/LC_MESSAGES/<msg>.mo`.

Sphinx should now know how to translate this message!

## To update a translation

To update a translation, you may go to the phase you'd like to modify in `jsons/`, then find the entry for the language you'd like to update, and change its value.
Finally, run `python sphinx_book_theme/translations/_convert.py` and this will update the `.mo` files.
