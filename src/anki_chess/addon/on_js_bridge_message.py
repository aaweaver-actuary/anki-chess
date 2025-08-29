from aqt import mw


def _mark_card_as_failed():
    mw.reviewer._answerCard(1)


def _mark_card_as_passed():
    mw.reviewer._answerCard(3)


def on_js_bridge_message(
    is_message_handled: tuple[bool, object],
    incoming_js_bridge_message: str,
    context: object,
):
    """Handle messages from the JavaScript bridge.

    Description
    -----------
    Handle messages from the JavaScript bridge. If the message is "fail_line", it will mark the current card as failed. If the message is "pass_line", it will mark the current card as passed.
    """
    if incoming_js_bridge_message == "fail_line":
        _mark_card_as_failed()
        return (True, None)
    elif incoming_js_bridge_message == "pass_line":
        _mark_card_as_passed()
        return (True, None)
    return (is_message_handled[0], None)
