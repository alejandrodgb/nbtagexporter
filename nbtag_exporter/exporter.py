"""
exporter.py
===========

Implements the core logic for the ``nbtag_exporter`` package.

This module provides:

1. **TagPythonExporter**
   A subclass of :class:`nbconvert.exporters.PythonExporter` that filters Jupyter
   notebook cells based on their metadata tags. It can include or exclude cells
   depending on configuration, enabling selective export of code or markdown
   content.

2. **export_tagged()**
   A high-level utility function designed for direct use within Jupyter notebooks.
   It automatically reads a notebook (either the current one or a specified file),
   applies tag-based filtering using ``TagPythonExporter``, and writes the result
   to a clean Python script.

Example
-------
Exporting selected cells from a notebook:

    from nbtag_exporter import export_tagged

    # Export all cells tagged "export" into a standalone script
    export_tagged(output="selected_cells.py", tags=["export"])

Or through the nbconvert CLI:

    jupyter nbconvert --to tagpy --TagPythonExporter.include_tags='["export"]' notebook.ipynb

Functions
---------
export_tagged(output, tags, notebook=None)
    Export only cells that contain specified tags to a .py file.

Classes
-------
TagPythonExporter
    Extends nbconvert.PythonExporter to include or exclude notebook cells by tag.

Notes
-----
- ``TagPythonExporter`` can be registered as a custom nbconvert exporter
  via entry points under ``[project.entry-points."nbconvert.exporters"]``.
- The helper ``export_tagged()`` optionally uses ``ipynbname`` to detect
  the current notebook path.
- All exports are plain Python text — outputs and execution state are stripped.

License
-------
MIT License — free to use, modify, and distribute with no warranty or liability.
"""


from __future__ import annotations
from pathlib import Path
from typing import Iterable, Literal, Sequence

from traitlets import List as TList, Unicode, default
from nbconvert.exporters import PythonExporter
from nbformat import read as nb_read
from nbformat.notebooknode import NotebookNode


class TagPythonExporter(PythonExporter):
    """
    nbconvert exporter that:
      - if include_tags is set: keeps ONLY cells having any of those tags
      - else if exclude_tags is set: drops cells having any of those tags
      - else: passes through all cells
    """
    include_tags = TList(Unicode(), help="Tags to include").tag(config=True)
    exclude_tags = TList(Unicode(), help="Tags to exclude").tag(config=True)

    @default("file_extension")
    def _file_extension_default(self) -> Literal[".py"]:
        return ".py"

    def from_notebook_node(self, nb: NotebookNode, resources=None, **kw):
        nb2 = NotebookNode(nb)
        nb2.cells = list(nb.cells or [])

        if self.include_tags:
            inc = set(self.include_tags)
            nb2.cells = [c for c in nb2.cells
                         if inc & set(c.get("metadata", {}).get("tags", []))]
        elif self.exclude_tags:
            exc = set(self.exclude_tags)
            nb2.cells = [c for c in nb2.cells
                         if not exc & set(c.get("metadata", {}).get("tags", []))]

        return super().from_notebook_node(nb2, resources=resources, **kw)


def _detect_notebook_path() -> Path | None:
    """
    Best-effort detection of the current notebook path.
    Requires optional dependency 'ipynbname'.
    """
    try:
        import ipynbname  # type: ignore
    except ModuleNotFoundError:
        return None

    try:
        return Path(ipynbname.path())
    except (OSError, RuntimeError, ValueError):
        return None


def _normalize_tags(tags: str | Iterable[str]) -> list[str]:
    if isinstance(tags, str):
        return [tags]
    return list(tags)


def export_tagged(
    output: str | Path,
    tags: str | Sequence[str],
    notebook: str | Path | None = None,
) -> Path:
    """
    Export selected cells from a notebook to a Python script, keeping only cells
    that contain any of the provided tags.

    Parameters
    ----------
    output : str | Path
        Destination .py file path.
    tags : str | Sequence[str]
        Tag or tags to include.
    notebook : str | Path | None
        Path to the source .ipynb. If None, tries to detect the current notebook.

    Returns
    -------
    Path
        The path to the written .py file.

    Raises
    ------
    FileNotFoundError
        If the notebook path cannot be determined or does not exist.
    """
    tags_list = _normalize_tags(tags)

    nb_path = Path(
        notebook) if notebook is not None else _detect_notebook_path()
    if nb_path is None or not nb_path.exists():
        raise FileNotFoundError(
            "Notebook path not found. Pass `notebook=...` explicitly or install "
            "the optional dependency `ipynbname` (pip install nbtag-exporter[auto]) "
            "to enable auto-detection."
        )

    nb_node = nb_read(nb_path, as_version=4)

    exporter = TagPythonExporter()
    exporter.include_tags = tags_list

    body, _ = exporter.from_notebook_node(nb_node)
    out_path = Path(output)
    out_path.write_text(body, encoding="utf-8")
    return out_path
