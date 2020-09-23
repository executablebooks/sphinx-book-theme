import json
import os
from pathlib import Path
import subprocess

if __name__ == "__main__":
    folder = Path(__file__).parent

    # remove exising
    for path in (folder / "locales").glob("**/booktheme.po"):
        path.unlink()

    # compile po
    for path in (folder / "jsons").glob("*.json"):
        data = json.loads(path.read_text("utf8"))
        assert data[0]["symbol"] == "en"
        english = data[0]["text"]
        for item in data[1:]:
            language = item["symbol"]
            out_path = folder / "locales" / language / "LC_MESSAGES" / "booktheme.po"
            if not out_path.parent.exists():
                out_path.parent.mkdir(parents=True)
            if not out_path.exists():
                out_path.write_text(
                    f"""
msgid ""
msgstr ""
"Project-Id-Version: Sphinx-Book-Theme\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Language: {language}\\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\\n"
"""
                )

            with out_path.open("a") as f:
                f.write("\n")
                f.write(f'msgid "{english}"\n')
                text = item["text"].replace('"', '\\"')
                f.write(f'msgstr "{text}"\n')

    # remove mo
    for path in (folder / "locales").glob("**/booktheme.po"):
        print(path)
        subprocess.check_call(
            [
                "msgfmt",
                os.path.abspath(path),
                "-o",
                os.path.abspath(path.parent / "booktheme.mo"),
            ]
        )
