
"""
nbtag_exporter
==============

Export selected (tagged) cells from a Jupyter notebook to a Python script.

Public API
----------
export_tagged(output, tags, notebook)
    Write a ``.py`` file that contains only the cells from the given notebook
    whose metadata includes **any** of the specified tags.

Current scope
-------------
- **Include-by-tag only**: cells are kept if they contain any tag in ``tags``.
- **Explicit notebook path required**: pass the path via ``notebook=...``.
- **Plain Python output**: execution state and outputs are not included.

Not in scope
------------
- Excluding cells by tag
- Command-line / nbconvert entry points
- Automatic detection of the current notebook path

Example
-------
    from nbtag_exporter import export_tagged

    export_tagged(
        output="selected_cells.py",
        tags=["export"],
        notebook="MyNotebook.ipynb",
    )

Notes
-----
- If the source notebook uses IPython magics (e.g., ``%time``, ``!cmd``), nbconvert
  may warn that IPython is not installed. Install it to enable syntax transformation:

      pip install ipython

License
-------
MIT License — provided “as is,” without warranty or liability.
"""


from .exporter import export_tagged, TagPythonExporter

__all__ = ["export_tagged", "TagPythonExporter"]
