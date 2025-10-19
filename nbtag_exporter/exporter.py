"""
exporter.py
===========

Export selected (tagged) cells from a Jupyter notebook to a Python script.

This module exposes a single public API:

- ``export_tagged(output, tags, notebook)``:
  Write a ``.py`` file that contains only the cells from the given notebook whose
  metadata includes **any** of the specified tags.

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

    # Keep only cells tagged "export" from MyNotebook.ipynb
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

    def __init__(self, **kwargs):
        super().__init__(template_name="python/plain", **kwargs)

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
