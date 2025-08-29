from anki_chess.addon.controller import ReviewerController, MockReviewer


def test_fail_line_marks_again():
    r = MockReviewer()
    c = ReviewerController(r)
    s = c.handle_command("fail_line")
    assert s == "failed"
    assert r.actions == [("answer", 1)]
    assert r.card.last_action == "ease_1"


def test_pass_line_marks_good():
    r = MockReviewer()
    c = ReviewerController(r)
    s = c.handle_command("pass_line")
    assert s == "passed"
    assert r.actions == [("answer", 3)]
    assert r.card.last_action == "ease_3"


def test_ignored():
    r = MockReviewer()
    c = ReviewerController(r)
    s = c.handle_command("noop")
    assert s == "ignored"
    assert r.actions == []
