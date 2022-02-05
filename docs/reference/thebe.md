---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Thebe

Thebe (via `sphinx-thebe`) is a special-case for this theme because it is particularly useful for interactive notebook use-cases.
This page shows off major Thebe functionality and discusses some gotchas.

When this page loads, activate Thebe by clicking the {guilabel}`Live Code` button at the top.

## Code style

Thebe uses CodeMirror in the background, which uses different styles than pygments, which is used for static code syntax highlighting.

Static code:

```
import tempfile
import os
import time

def test_upper():
    assert True
    in_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
    out_file = tempfile.NamedTemporaryFile(delete=False)
    out_file.close()
    in_file.write("test123\nthetest")
    in_file.close()
    file_to_upper(in_file.name, out_file.name)
    with open(out_file.name, 'r') as f:
        data = f.read()
        assert data == "TEST123\nTHETEST"
    os.unlink(in_file.name)
    os.unlink(out_file.name)
```

Runnable thebe code:

```{code-cell}
import tempfile
import os
import time

def test_upper():
    assert True
    in_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
    out_file = tempfile.NamedTemporaryFile(delete=False)
    out_file.close()
    in_file.write("test123\nthetest")
    in_file.close()
    file_to_upper(in_file.name, out_file.name)
    with open(out_file.name, 'r') as f:
        data = f.read()
        assert data == "TEST123\nTHETEST"
    os.unlink(in_file.name)
    os.unlink(out_file.name)
```
