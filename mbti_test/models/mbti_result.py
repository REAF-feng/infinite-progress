from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class MBTIResult:
    type_code: str = ""
    type_nickname: str = ""
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    dimension_percentages: Dict[str, Dict[str, float]] = field(default_factory=dict)
    function_scores: Dict[str, float] = field(default_factory=dict)
    function_stack: List[str] = field(default_factory=list)
    function_labels: Dict[str, str] = field(default_factory=dict)
    validation_passed: bool = True
    validation_details: Dict = field(default_factory=dict)
    consistency_score: float = 0.0
    report_sections: Dict[str, str] = field(default_factory=dict)
    answers: List = field(default_factory=list)
    completion_time_seconds: int = 0
