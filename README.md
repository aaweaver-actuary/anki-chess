
# Chess Anki MoveTrainer-Style Toolkit

This repository provides:
1. PGN to Anki CSV conversion (lines + branches exploded).
2. A front card template with an interactive JavaScript chessboard that **enforces guessing the entire line**.
3. A minimal add-on bridge to **auto-fail** on first mistake and **auto-pass** on completion.

## Usage

Convert PGN to CSV:
```bash
python -m pgn2anki.cli examples/repertoire.pgn out.csv --title "My Repertoire" --max-plies 30
```

Import `out.csv` into Anki using fields `Title`, `FEN`, `SAN_SEQ_JSON` and the templates in `anki_template/`.

Optional: Copy `addon/` into Anki's `addons21/` to enable auto-fail/auto-pass via `pycmd`.

## Testing
```bash
pytest -q
```

## Notes
- No dependency on python-chess in tests. FEN defaults to "start".
- For tactics, set `FEN` to the puzzle start and `SAN_SEQ_JSON` to the exact solution SAN sequence.
