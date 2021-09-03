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

# Test thebe

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

## From pygments.css

```
# From http://toolness.github.io/brocco/
  var codeMirrorStyleMap = {
    "cm-keyword": "k",
    "cm-atom": "kc",
    "cm-number": "m",
    "cm-comment": "c",
    "cm-string": "s2",
    "cm-string-2": "s2",
    "cm-tag": "nt",
    "cm-attribute": "na"
  };

```


<script language="javascript">
    window.addEventListener('load', () => {
        initThebeSBT()
    }
    );
</script>
