from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EvalSummary:
    total: int
    correct: int
    invalid_outputs: int
    retries: int

    @property
    def accuracy(self) -> float:
        return (self.correct / self.total) if self.total else 0.0

    @property
    def invalid_rate(self) -> float:
        return (self.invalid_outputs / self.total) if self.total else 0.0

    @property
    def retry_rate(self) -> float:
        return (self.retries / self.total) if self.total else 0.0
