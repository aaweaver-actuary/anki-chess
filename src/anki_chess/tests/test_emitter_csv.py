import io
import csv
import json
import pytest
from anki_chess.pgn2anki.parser import parse_pgn_to_lines
from anki_chess.pgn2anki.emitter import emit_csv


@pytest.fixture
def pgn():
    return "1. e4 e5 2. Nf3 Nc6 *"


@pytest.fixture
def lines(pgn):
    return parse_pgn_to_lines(pgn, title="TestLine")


@pytest.fixture
def csv_rows(lines):
    buf = io.StringIO()
    emit_csv(lines, buf)
    buf.seek(0)
    return list(csv.reader(buf))


def test_emit_csv_writes_header_row(csv_rows):
    expected = ["Title", "FEN", "SAN_SEQ_JSON"]
    actual = csv_rows[0]
    assert actual == expected, f"Header row mismatch: expected {expected}, got {actual}"


def test_emit_csv_writes_title_in_first_data_row(csv_rows):
    title = csv_rows[1][0]
    assert title.startswith("TestLine"), (
        f"First data row title does not start with 'TestLine': got '{title}'"
    )


def test_emit_csv_writes_correct_san_sequence_json(csv_rows):
    seq = json.loads(csv_rows[1][2])
    expected_seq = ["e4", "e5", "Nf3", "Nc6"]
    actual_seq = seq[:4]
    assert actual_seq == expected_seq, (
        f"SAN sequence mismatch: expected {expected_seq}, got {actual_seq}"
    )


def test_emit_csv_returns_start_when_chess_none(monkeypatch, lines):
    import anki_chess.pgn2anki.emitter as emitter_mod

    monkeypatch.setattr(emitter_mod, "chess", None)
    buf = io.StringIO()
    emit_csv(lines, buf)
    buf.seek(0)
    rows = list(csv.reader(buf))
    fen = rows[1][1]
    assert fen == "start", f"Expected FEN to be 'start' when chess is None, got '{fen}'"
