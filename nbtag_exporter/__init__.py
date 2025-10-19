
"""
nbtag_exporter
==============

A lightweight extension for Jupyter notebooks that integrates with nbconvert to 
export only selected, tagged cells into clean Python scripts.

This package provides two main components:
- `TagPythonExporter`: a subclass of `nbconvert.PythonExporter` that filters notebook
  cells based on include/exclude tags.
- `export_tagged()`: a convenience function callable from within any Jupyter notebook
  to export specific tagged cells directly to a `.py` file with one command.

Example
-------
In a notebook:

    from nbtag_exporter import export_tagged

    # Export all cells tagged 'export' to selected_cells.py
    export_tagged(output="selected_cells.py", tags=["export"])

The exporter can also be used through the nbconvert CLI:

    jupyter nbconvert --to tagpy --TagPythonExporter.include_tags='["export"]' notebook.ipynb

License
-------
MIT License — free to use, modify, and distribute with no warranty or liability.
"""

from .exporter import export_tagged, TagPythonExporter

__all__ = ["export_tagged", "TagPythonExporter"]
