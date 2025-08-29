import pytest
from anki_chess.pgn2anki.parser import parse_pgn_to_lines


def test_parse_empty_pgn_returns_empty_list():
    lines = parse_pgn_to_lines("")
    assert lines == [], f"Expected empty list for empty PGN, got {lines}"


def test_parse_whitespace_only_pgn_returns_empty_list():
    lines = parse_pgn_to_lines("   \n\t  ")
    assert lines == [], f"Expected empty list for whitespace-only PGN, got {lines}"


def test_parse_pgn_with_only_headers_returns_empty_list():
    lines = parse_pgn_to_lines('[Event "Test"]\n[Site "Test"]')
    assert lines == [], f"Expected empty list for PGN with only headers, got {lines}"


def test_parse_pgn_with_only_comments_returns_empty_list():
    lines = parse_pgn_to_lines("{This is a comment} ;another")
    assert lines == [], f"Expected empty list for PGN with only comments, got {lines}"


def test_parse_pgn_with_only_nags_returns_empty_list():
    lines = parse_pgn_to_lines("$1 $2 $3")
    assert lines == [], f"Expected empty list for PGN with only NAGs, got {lines}"


def test_parse_pgn_with_deeply_nested_variations():
    pgn = "1. e4 (1... e5 (1... c5 (1... d6))) 2. Nf3"
    lines = parse_pgn_to_lines(pgn)
    assert any("d6" in seq for seq in [x.san_seq for x in lines]), (
        f"Expected 'd6' in some line, got {[x.san_seq for x in lines]}"
    )


def test_parse_pgn_with_cycle_does_not_crash():
    # Artificial cycle: create a node that is its own child
    from anki_chess.pgn2anki.node import Node

    root = Node("e4")
    root.children.append(root)
    out = []
    try:
        from anki_chess.pgn2anki import parser as parser_mod

        parser_mod._extract_lines_dfs(root, [], out)
    except RecursionError:  # pragma: no cover
        assert False, (
            "Cycle in move tree should not cause RecursionError."
        )  # pragma: no cover
    assert out == [], f"Cycle should not produce any lines, got {out}"


@pytest.fixture
def ruy_lopez_pgn():
    return "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0"


@pytest.fixture
def ruy_lopez_lines(ruy_lopez_pgn):
    return parse_pgn_to_lines(ruy_lopez_pgn, title="Ruy Lopez")


def test_parse_simple_mainline_returns_one_line(ruy_lopez_lines):
    lines = ruy_lopez_lines
    assert len(lines) == 1, f"Expected 1 line, got {len(lines)}: {lines}"


def test_parse_simple_mainline_title_startswith_ruy_lopez(ruy_lopez_lines):
    title = ruy_lopez_lines[0].title
    assert title.startswith("Ruy Lopez"), (
        f"Title does not start with 'Ruy Lopez': got '{title}'"
    )


def test_parse_simple_mainline_san_sequence_is_correct(ruy_lopez_lines):
    expected_seq = ["e4", "e5", "Nf3", "Nc6"]
    actual_seq = ruy_lopez_lines[0].san_seq[:4]
    assert actual_seq == expected_seq, (
        f"SAN sequence mismatch: expected {expected_seq}, got {actual_seq}"
    )


@pytest.fixture
def indian_defenses_pgn():
    return "1. d4 Nf6 (1... d5 2. c4) 2. c4 e6 (2... g6) 1/2-1/2"


@pytest.fixture
def indian_defenses_lines(indian_defenses_pgn):
    return parse_pgn_to_lines(indian_defenses_pgn, title="Indian Defenses")


def test_parse_variation_returns_at_least_three_lines(indian_defenses_lines):
    lines = indian_defenses_lines
    assert len(lines) >= 3, f"Expected at least 3 lines, got {len(lines)}: {lines}"


def test_parse_variation_has_line_starting_with_d4(indian_defenses_lines):
    has_d4 = any(x.san_seq[0] == "d4" for x in indian_defenses_lines)
    assert has_d4, (
        f"No line starts with 'd4': {[x.san_seq for x in indian_defenses_lines]}"
    )
