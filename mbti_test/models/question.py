from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Question:
    id: int
    text: str
    dichotomy: str
    direction: int
    weight: float = 1.0
    functions: List[str] = field(default_factory=list)
    is_validation: bool = False
    validation_pair_id: Optional[int] = None
