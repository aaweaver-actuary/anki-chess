from anki_chess.pgn2anki import parser


def test_tokenize_empty_string_returns_empty_list():
    assert parser._tokenize("") == [], (
        "Tokenizing empty string should return empty list."
    )


def test_tokenize_only_whitespace_returns_empty_list():
    assert parser._tokenize("   \n\t  ") == [], (
        "Tokenizing whitespace-only string should return empty list."
    )


def test_tokenize_single_move():
    assert parser._tokenize("e4") == ["e4"], (
        "Tokenizing single move should return ['e4']."
    )


def test_tokenize_parentheses():
    assert parser._tokenize("(") == ["("], "Tokenizing '(' should return ['(']."
    assert parser._tokenize(")") == [")"], "Tokenizing ')' should return [')']."
    assert parser._tokenize("e4 ( e5 )") == ["e4", "(", "e5", ")"], (
        "Tokenizing with parentheses should split correctly."
    )


def test_tokenize_flush_buffer_adds_token():
    tokens = []
    buff = "e4"
    parser._tokenize_flush_buffer(buff, tokens)
    assert tokens == ["e4"], f"Flush buffer should add 'e4' to tokens, got {tokens}"


def test_tokenize_step_handles_parenthesis():
    tokens = []
    buff = "e4"
    buff, tokens = parser._tokenize_step("(", buff, tokens)
    assert tokens == ["e4", "("], (
        f"Step with '(' should flush buffer and add parenthesis, got {tokens}"
    )
    assert buff == "", f"Buffer should be reset after parenthesis, got '{buff}'"


def test_tokenize_step_handles_whitespace():
    tokens = []
    buff = "e4"
    buff, tokens = parser._tokenize_step(" ", buff, tokens)
    assert tokens == ["e4"], f"Step with whitespace should flush buffer, got {tokens}"
    assert buff == "", f"Buffer should be reset after whitespace, got '{buff}'"


def test_tokenize_step_handles_other():
    tokens = []
    buff = "e"
    buff, tokens = parser._tokenize_step("4", buff, tokens)
    assert buff == "e4", f"Step with other char should append to buffer, got '{buff}'"
    assert tokens == [], f"Tokens should remain unchanged, got {tokens}"


def test_prep_pgn_for_tokenization_removes_headers_comments_nags():
    pgn = '[Event "Test"]\n1. e4 $1 {comment} ;semi\n1-0'
    result = parser._prep_pgn_for_tokenization(pgn)
    assert "[Event" not in result, "Headers should be removed."
    assert "$1" not in result, "NAGs should be removed."
    assert "comment" not in result, "Curly brace comments should be removed."
    assert "semi" not in result, "Semicolon comments should be removed."


def test_is_whitespace_character_true_false():
    assert parser._is_whitespace_character(" ") is True
    assert parser._is_whitespace_character("\n") is True
    assert parser._is_whitespace_character("e") is False


def test_contains_non_whitespace_characters_true_false():
    assert parser._contains_non_whitespace_characters("e4") is True
    assert parser._contains_non_whitespace_characters("   ") is False


def test_is_parenthesis_character_true_false():
    assert parser._is_parenthesis_character("(") is True
    assert parser._is_parenthesis_character(")") is True
    assert parser._is_parenthesis_character("e") is False
