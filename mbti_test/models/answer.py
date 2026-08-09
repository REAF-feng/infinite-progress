from dataclasses import dataclass

@dataclass
class Answer:
    question_id: int
    value: int
    timestamp_ms: float = 0.0
