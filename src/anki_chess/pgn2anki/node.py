from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Node:
    san: str | None
    children: list["Node"]

    def __init__(self, san: str | None):
        self.san = san
        self.children = []
