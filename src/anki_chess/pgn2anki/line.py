from __future__ import annotations
from typing import List
from dataclasses import dataclass


@dataclass
class Line:
    title: str
    san_seq: List[str]
