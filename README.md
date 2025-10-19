# nbtag-exporter

`nbtag-exporter` exports **only selected (tagged) cells** from a Jupyter notebook into a clean `.py` script.

It provides a single, notebook-friendly API that keeps cells containing the tags you specify and writes the result to a Python file.

---

## Features

- 🔖 **Export by tag (include-only)** – keep cells that have any of the provided tags (e.g., `"export"`).
- 🧩 **Simple one-call API** – usable directly inside a notebook.

> Note: This package **does not** currently implement “exclude by tag,” CLI entry points, or automatic notebook detection. Pass the notebook path explicitly.

---

## Example

Tag one or more cells in Jupyter with `"export"`, then run:

```python
from nbtag_exporter import export_tagged
export_tagged(output="selected_cells.py", tags=["export"], notebook="MyNotebook.ipynb")
```

Result → a Python file containing only those tagged cells.

---

## Installation

```bash
pip install "git+https://github.com/alejandrodgb/nbtagexporter.git@main"
```

---

## Notes

- If your notebook uses IPython magics (`%time`, `!pip`, etc.), you may see a warning from `nbconvert`.  
  Install IPython to enable syntax transformation:

  ```bash
  pip install ipython
  ```

---

## License

MIT License — free to use, modify, and distribute.  
Provided “as is,” without warranty or liability.
