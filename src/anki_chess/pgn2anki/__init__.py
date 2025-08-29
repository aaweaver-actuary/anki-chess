"""
PGN to Anki CSV tooling for MT-style line drilling.

This package extracts linear lines (including branches) from PGN and emits
CSV rows ready to import into an Anki note type that uses an interactive board.
"""

__all__ = ["parse_pgn_to_lines", "emit_csv", "Line"]
from .parser import parse_pgn_to_lines, Line
from .emitter import emit_csv
