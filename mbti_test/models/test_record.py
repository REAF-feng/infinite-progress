from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import uuid

@dataclass
class TestRecord:
    id: str = ""
    timestamp: str = ""
    test_duration_seconds: int = 0
    answers: List[dict] = field(default_factory=list)
    result: Optional[dict] = None

    @classmethod
    def create_new(cls, answers: List, duration: int, result_dict: dict):
        return cls(
            id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            test_duration_seconds=duration,
            answers=answers,
            result=result_dict,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "test_duration_seconds": self.test_duration_seconds,
            "answers": self.answers,
            "result": self.result,
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            id=d.get("id", ""),
            timestamp=d.get("timestamp", ""),
            test_duration_seconds=d.get("test_duration_seconds", 0),
            answers=d.get("answers", []),
            result=d.get("result"),
        )
