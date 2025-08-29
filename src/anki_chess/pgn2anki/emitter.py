from __future__ import annotations
from typing import Iterable, List
import csv
import json
import chess


def _compute_start_fen_for_line(san_seq: List[str]) -> str:
    if chess is None:
        return "start"
    board = chess.Board()
    return board.fen()


def emit_csv(lines: Iterable, fp) -> None:
    writer = csv.writer(fp)
    writer.writerow(["Title", "FEN", "SAN_SEQ_JSON"])
    for line in lines:
        fen = _compute_start_fen_for_line(line.san_seq)
        writer.writerow([line.title, fen, json.dumps(line.san_seq, ensure_ascii=False)])
