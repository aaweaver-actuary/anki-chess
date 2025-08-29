import pytest
import argparse
from unittest.mock import patch, MagicMock
from anki_chess.pgn2anki import cli


@pytest.fixture
def parser():
    return argparse.ArgumentParser()


def test_add_max_plies_argument_adds_max_plies(parser):
    ap = cli._add_max_plies_argument(parser)
    arg_names = [a.dest for a in ap._actions]
    assert "max_plies" in arg_names, (
        f"'max_plies' not found in parser actions: {arg_names}"
    )


def test_add_title_argument_adds_title(parser):
    ap = cli._add_title_argument(parser)
    arg_names = [a.dest for a in ap._actions]
    assert "title" in arg_names, f"'title' not found in parser actions: {arg_names}"


def test_add_input_pgn_argument_adds_input_pgn(parser):
    ap = cli._add_input_pgn_argument(parser)
    arg_names = [a.dest for a in ap._actions]
    assert "input_pgn" in arg_names, (
        f"'input_pgn' not found in parser actions: {arg_names}"
    )


def test_add_output_csv_argument_adds_output_csv(parser):
    ap = cli._add_output_csv_argument(parser)
    arg_names = [a.dest for a in ap._actions]
    assert "output_csv" in arg_names, (
        f"'output_csv' not found in parser actions: {arg_names}"
    )


def test_initialize_argument_parser_includes_all_expected_arguments():
    ap = cli._initialize_argument_parser()
    expected_args = {"input_pgn", "output_csv", "title", "max_plies"}
    actual_args = {a.dest for a in ap._actions if a.dest != "help"}
    assert expected_args.issubset(actual_args), (
        f"Parser missing expected arguments: expected {expected_args}, got {actual_args}"
    )


def test_load_pgn_content_reads_file_content(tmp_path):
    pgn_file = tmp_path / "test.pgn"
    expected_content = "1. e4 e5 *"
    pgn_file.write_text(expected_content, encoding="utf-8")
    args = MagicMock()
    args.input_pgn = pgn_file
    content = cli._load_pgn_content(args)
    assert content == expected_content, (
        f"PGN content mismatch: expected '{expected_content}', got '{content}'"
    )


def test_main_writes_csv_file(monkeypatch, tmp_path):
    pgn_file = tmp_path / "input.pgn"
    pgn_file.write_text("1. e4 e5 *", encoding="utf-8")
    output_file = tmp_path / "output.csv"
    fake_lines = [MagicMock(title="Test", san_seq=["e4", "e5"])]
    monkeypatch.setattr(cli, "parse_pgn_to_lines", lambda *a, **kw: fake_lines)
    monkeypatch.setattr(
        cli,
        "emit_csv",
        lambda lines, fp: fp.write('Title,FEN,SAN_SEQ_JSON\nTest,start,"[e4,e5]"\n'),
    )
    argv = [str(pgn_file), str(output_file)]
    with patch("builtins.print"):
        cli.main(argv)
    content = output_file.read_text(encoding="utf-8")
    assert content.startswith("Title,FEN,SAN_SEQ_JSON"), (
        f"CSV file content does not start with expected header. Got: {content[:50]}"
    )


def test_main_prints_summary(monkeypatch, tmp_path):
    pgn_file = tmp_path / "input.pgn"
    pgn_file.write_text("1. e4 e5 *", encoding="utf-8")
    output_file = tmp_path / "output.csv"
    fake_lines = [MagicMock(title="Test", san_seq=["e4", "e5"])]
    monkeypatch.setattr(cli, "parse_pgn_to_lines", lambda *a, **kw: fake_lines)
    monkeypatch.setattr(
        cli,
        "emit_csv",
        lambda lines, fp: fp.write('Title,FEN,SAN_SEQ_JSON\nTest,start,"[e4,e5]"\n'),
    )
    argv = [str(pgn_file), str(output_file)]
    with patch("builtins.print") as mock_print:
        cli.main(argv)
        assert mock_print.called, (
            "Expected main() to print a summary, but print was not called."
        )
