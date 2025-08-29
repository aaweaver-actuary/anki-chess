from dataclasses import dataclass


@dataclass
class MockCard:
    id: int
    last_action: str | None = None


class MockReviewer:
    def __init__(self):
        self.card = MockCard(id=42)
        self.actions = []

    def _answerCard(self, ease: int) -> None:
        self.actions.append(("answer", ease))
        self.card.last_action = f"ease_{ease}"


class ReviewerController:
    def __init__(self, reviewer):
        self.reviewer = reviewer

    def handle_command(self, cmd: str) -> str:
        if cmd == "fail_line":
            self.reviewer._answerCard(1)
            return "failed"
        elif cmd == "pass_line":
            self.reviewer._answerCard(3)
            return "passed"
        return "ignored"
