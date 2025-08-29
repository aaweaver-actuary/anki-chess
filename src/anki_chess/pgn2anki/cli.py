from __future__ import annotations
import argparse
import pathlib
from .parser import parse_pgn_to_lines
from .emitter import emit_csv


def _add_max_plies_argument(ap):
    ap.add_argument("--max-plies", type=int, default=None)
    return ap


def _add_title_argument(ap):
    ap.add_argument("--title", type=str, default=None)
    return ap


def _add_output_csv_argument(ap):
    ap.add_argument("output_csv", type=pathlib.Path)
    return ap


def _add_input_pgn_argument(ap):
    ap.add_argument("input_pgn", type=pathlib.Path)
    return ap


def _initialize_argument_parser():
    ap = argparse.ArgumentParser()
    ap = _add_input_pgn_argument(ap)
    ap = _add_output_csv_argument(ap)
    ap = _add_title_argument(ap)
    ap = _add_max_plies_argument(ap)
    return ap


def _load_pgn_content(args):
    return args.input_pgn.read_text(encoding="utf-8")


def main(argv=None):
    ap = _initialize_argument_parser()
    args = ap.parse_args(argv)
    pgn_text = _load_pgn_content(args)
    lines = parse_pgn_to_lines(pgn_text, max_plies=args.max_plies, title=args.title)
    with args.output_csv.open("w", encoding="utf-8", newline="") as fp:
        emit_csv(lines, fp)
    print(f"Wrote {len(lines)} lines to {args.output_csv}")


if __name__ == "__main__":
    main()  # pragma: no cover
