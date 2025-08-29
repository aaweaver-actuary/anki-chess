from __future__ import annotations
from typing import List, Tuple
import re

from .node import Node
from .line import Line
from .const import PGN_HEADER_REGEX, PGN_COMMENT_REGEX, PGN_MOVE_NUMBER_REGEX


def _tokenize(pgn: str) -> List[str]:
    s = _prep_pgn_for_tokenization(pgn)
    tokens = []
    buff = ""
    for ch in s:
        if _is_parenthesis_character(ch):
            if _contains_non_whitespace_characters(buff):
                tokens.append(buff.strip())
            tokens.append(ch)
            buff = ""
        elif _is_whitespace_character(ch):
            if _contains_non_whitespace_characters(buff):
                tokens.append(buff.strip())
                buff = ""
        else:
            buff += ch
    if _contains_non_whitespace_characters(buff):
        tokens.append(buff.strip())
    return tokens


def _is_whitespace_character(ch: str) -> bool:
    """Check if a character is a whitespace character."""
    return ch.isspace()


def _contains_non_whitespace_characters(buff: str) -> bool:
    """Check if the buffer contains non-whitespace characters."""
    return buff.strip() != ""


def _is_parenthesis_character(ch: str) -> bool:
    """Check if a character is a parenthesis character."""
    return ch in "()"


def _prep_pgn_for_tokenization(pgn: str) -> str:
    """Prepare PGN for tokenization by normalizing whitespace."""
    s = pgn
    s = _remove_headers_from_pgn(s)
    s = _remove_comments_from_pgn(s)
    s = _remove_semicolon_comments_from_pgn(s)
    s = _remove_numeric_annotation_glyphs_from_pgn(s)
    return s


def _remove_numeric_annotation_glyphs_from_pgn(s: str) -> str:
    """Remove numeric annotation glyphs from PGN.

    Description
    -----------
    Numeric annotation glyphs (e.g., $1, $2) are used in PGN to indicate
    variations or alternative moves. This function removes them from the
    PGN string.
    """
    return re.sub(r"\$\d+", " ", s)


def _remove_semicolon_comments_from_pgn(s: str) -> str:
    """Remove semicolon comments from PGN.

    Description
    -----------
    Semicolon comments (e.g., ; this is a comment) are used in PGN to
    provide commentary on the game. This function removes them from the
    PGN string.
    """
    return re.sub(r";[^\n]*", " ", s)


def _remove_comments_from_pgn(s: str) -> str:
    """Remove comments from PGN.

    Description
    -----------
    Comments (e.g., { this is a comment }) are used in PGN to provide
    commentary on the game. This function removes them from the
    PGN string.
    """
    return re.sub(PGN_COMMENT_REGEX, " ", s)


def _remove_headers_from_pgn(s: str) -> str:
    """Remove headers from PGN.

    Description
    -----------
    Headers (e.g., [Event "F/S Return Match"]) are used in PGN to provide
    metadata about the game. This function removes them from the
    PGN string.
    """
    return re.sub(PGN_HEADER_REGEX, "", s, flags=re.M)


def _is_token_a_move_number(tok: str) -> bool:
    """Check if a token is a move number."""
    return re.match(PGN_MOVE_NUMBER_REGEX, tok) is not None


def _is_token_a_game_result(tok: str) -> bool:
    """Check if a token is a game result (e.g. a white win, black win, draw, or ongoing)."""
    return tok in ("1-0", "0-1", "1/2-1/2", "*")


def _parse_moves(tokens: List[str], i: int = 0) -> Tuple[Node, int]:
    """Parse a list of tokens into a tree of moves.

    Description
    -----------
    This function takes a list of tokens representing moves in a chess game
    and organizes them into a tree structure, where each node represents a
    move and its variations.
    """
    root = Node(None)
    cur_parent_stack = [root]

    def add_move(san: str):
        parent = cur_parent_stack[-1]
        node = Node(san)
        parent.children.append(node)
        cur_parent_stack.append(node)

    n = len(tokens)
    while i < n:
        tok = tokens[i]
        if tok == "(":
            anchor = (
                cur_parent_stack[-2]
                if len(cur_parent_stack) > 1
                else cur_parent_stack[-1]
            )
            var_root, j = _parse_moves(tokens, i + 1)
            anchor.children.extend(var_root.children)
            i = j
            continue
        elif tok == ")":
            return root, i + 1
        elif _is_token_a_move_number(tok) or _is_token_a_game_result(tok):
            i += 1
            continue
        else:
            add_move(tok)
            i += 1
            continue
    return root, i


def _extract_lines_dfs(node: Node, prefix: List[str], out: List[List[str]]):
    if node.san is not None:
        prefix = prefix + [node.san]
    if not node.children:
        if prefix:
            out.append(prefix)
        return
    for ch in node.children:
        _extract_lines_dfs(ch, prefix, out)


def parse_pgn_to_lines(
    pgn_text: str, max_plies: int | None = None, title: str | None = None
) -> List[Line]:
    tokens = _tokenize(pgn_text)
    root, _ = _parse_moves(tokens, 0)
    seqs: List[List[str]] = []
    _extract_lines_dfs(root, [], seqs)
    lines: List[Line] = []
    if not seqs:
        return lines  # pragma: no cover
    base_title = title or "Repertoire Line"
    for idx, seq in enumerate(seqs, 1):
        s = seq if max_plies is None else seq[:max_plies]
        lines.append(Line(title=f"{base_title} #{idx}", san_seq=s))
    return lines
