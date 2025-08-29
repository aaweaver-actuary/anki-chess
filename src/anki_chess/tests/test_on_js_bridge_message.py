import pytest
from unittest.mock import patch, MagicMock
from anki_chess.addon.on_js_bridge_message import (
    on_js_bridge_message,
    _mark_card_as_failed,
    _mark_card_as_passed,
)


@pytest.fixture
def mock_mw():
    with patch("anki_chess.addon.on_js_bridge_message.mw") as mw:
        mw.reviewer = MagicMock()
        yield mw


def test_mark_card_as_failed_calls_answerCard_with_1(mock_mw):
    _mark_card_as_failed()
    mock_mw.reviewer._answerCard.assert_called_once_with(1)


def test_mark_card_as_passed_calls_answerCard_with_3(mock_mw):
    _mark_card_as_passed()
    mock_mw.reviewer._answerCard.assert_called_once_with(3)


@pytest.mark.parametrize(
    "msg,expected_call,expected_return",
    [
        ("fail_line", 1, (True, None)),
        ("pass_line", 3, (True, None)),
    ],
)
def test_on_js_bridge_message_handles_known_messages(
    mock_mw, msg, expected_call, expected_return
):
    result = on_js_bridge_message((False, {}), msg, {})
    mock_mw.reviewer._answerCard.assert_called_once_with(expected_call)
    assert result == expected_return, (
        f"Unexpected return value for message '{msg}': got {result}, expected {expected_return}."
    )


def test_on_js_bridge_message_handles_unknown_message(mock_mw):
    result = on_js_bridge_message((False, {}), "other_message", {})
    mock_mw.reviewer._answerCard.assert_not_called()
    assert result == (False, None), (
        f"Unexpected return value for unknown message: got {result}, expected {(False, None)}"
    )
