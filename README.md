# nbtag-exporter

`nbtag-exporter` is a lightweight extension for Jupyter that lets you export *only selected cells* from a notebook into a clean `.py` script.

It builds on top of **nbconvert** and allows you to include or exclude cells by tag. 
With a single function call, you can create maintainable, version-controllable Python scripts from your notebooks — ideal for packaging, testing, or production workflows.

---

## ✨ Features

- 🔖 **Export by tag** – keep only cells that match given tags (e.g., `"export"`).
- 🧩 **Single-command API** – from within a notebook:
  ```python
  from nbtag_exporter import export_tagged
  export_tagged(output="script.py", tags=["export"])
  ```
- 📂 **Automatic notebook detection** – optionally detects the current notebook path.
- ⚙️ **CLI and nbconvert integration** – usable via `jupyter nbconvert --to tagpy`.
- 💡 **No dependencies beyond nbconvert & nbformat**.

---

## 🛠️ Example

Tag one or more cells in Jupyter (via the **Tags** tool) with `"export"`, then run:

```python
from nbtag_exporter import export_tagged
export_tagged(output="selected_cells.py", tags=["export"])
```

Result → a Python file containing only those tagged cells.

---

## 📦 Installation

```bash
pip install nbtag-exporter
# or with optional auto-detection support
pip install nbtag-exporter[auto]
```

---

## ⚖️ License

MIT License – free to use, modify, and distribute.  
The software is provided **“as is”** without warranty of any kind or liability.
