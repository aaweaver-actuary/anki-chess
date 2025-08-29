def test_emit_csv_writes_each_game_as_separate_row():
    # Use the actual danish.pgn file contents
    pgn = """[Event "TCEC 27 Premier 2024"]
[Site "tcec-chess.com INT"]
[Date "2024.12.06"]
[Round "30.3"]
[White "Stockfish dev-20241122-b7f17346"]
[Black "Obsidian 14.06"]
[Result "1/2-1/2"]
[WhiteElo "3677"]
[BlackElo "3555"]
[ECO "C21"]

1.e4 e5 2.d4 exd4 3.c3 dxc3 4.Bc4 cxb2 5.Bxb2 Bb4+ 6.Nc3 Nf6 7.Ne2 O-O 8.O-O c6
9.e5 Ng4 10.Ne4 Qh4 11.h3 Nxe5 12.N2g3 d5 13.Bxe5 dxc4 14.Qd4 c5 15.Qxc4 Be6
16.Qb5 Nc6 17.Bd6 Rfc8 18.a3 a6 19.Qe2 Ba5 20.Bxc5 Bc7 21.Rac1 Bd5 22.Bd6 Bxe4
23.Nxe4 Re8 24.Qb2 Qxe4 25.Bxc7 b5 26.Rfd1 h6 27.Qc3 Ne7 28.Qd4 Qxd4 29.Rxd4 Rec8
30.Rd7 Ng6 31.Rc3 h5 32.g3 h4 33.Kg2 f6 34.Ba5 hxg3 35.Kxg3 Ne5 36.Rxc8+ Rxc8
37.Ra7 Rc6 38.Bb4 Nc4 39.Kf4 a5 40.Bxa5 Nxa3  1/2-1/2

[Event "GBR-ch"]
[Site "London"]
[Date "1868.??.??"]
[Round "?"]
[White "Blackburne, Joseph Henry"]
[Black "Cuthbertson"]
[Result "1-0"]
[WhiteElo ""]
[BlackElo ""]
[ECO "C21"]

1.e4 e5 2.d4 exd4 3.c3 d5 4.e5 dxc3 5.bxc3 Nc6 6.Nf3 f6 7.Bb5 Bd7 8.Qxd5 Nge7
9.Qd3 a6 10.Bc4 Bg4 11.exf6 Qxd3 12.f7+ Kd8 13.Bxd3 Be6 14.Ng5 Bd5 15.c4 Ne5
16.cxd5 Nxd3+ 17.Kd2 Nc5 18.Ne6+ Nxe6 19.dxe6 Nd5 20.Bb2 Ke7 21.Re1 b6 22.Kc2 Nf4
23.Nc3 Nxe6 24.Nd5+ Kxf7 25.Rxe6 Bd6 26.Rae1 Rae8 27.Rxe8 Rxe8 28.Rxe8 Kxe8
29.Bxg7  1-0
"""
    lines = parse_pgn_to_lines(pgn, title="DanishTest")
    import io, csv

    buf = io.StringIO()
    emit_csv(lines, buf)
    buf.seek(0)
    rows = list(csv.reader(buf))
    data_rows = rows[1:]
    # Expect at least two data rows, one per game
    assert len(data_rows) >= 2, (
        f"Expected at least 2 data rows for games, got {len(data_rows)}"
    )


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


def test_emit_csv_writes_each_variation_as_separate_row():
    # PGN with a main line and a variation
    pgn = "1. e4 e5 2. Nf3 Nc6 (2... d6 3. d4 exd4) 3. Bb5 a6 *"
    lines = parse_pgn_to_lines(pgn, title="VarTest")
    buf = io.StringIO()
    emit_csv(lines, buf)
    buf.seek(0)
    rows = list(csv.reader(buf))
    # Expect at least two data rows: one for main line, one for variation
    data_rows = rows[1:]
    assert len(data_rows) >= 2, (
        f"Expected at least 2 data rows for variations, got {len(data_rows)}"
    )
