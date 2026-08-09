'''
MBTI - Core Scoring Engine

Provides the central scoring pipeline:
  1. Raw dimension scores from answers
  2. Dimension percentages
  3. Type-code determination
  4. Two-stage cognitive-function scores
  5. Preference-strength classification
  6. Function-stack labels
'''

from typing import Dict, List, Optional, Tuple

from models import MBTIResult, Answer, Question
from config import (
    DICHOTOMIES,
    QUESTIONS_PER_DICHOTOMY,
    FUNCTION_BASE_SCORES,
    FUNCTION_ACTIVATION_RANGE,
    PREFERENCE_SLIGHT,
    PREFERENCE_MODERATE,
)

# ---------------------------------------------------------------------------
# Function stacks for all 16 MBTI types (conscious + shadow)
# ---------------------------------------------------------------------------

FUNCTION_STACKS: Dict[str, List[str]] = {
    'INTJ': ['Ni', 'Te', 'Fi', 'Se', 'Ne', 'Ti', 'Fe', 'Si'],
    'INTP': ['Ti', 'Ne', 'Si', 'Fe', 'Te', 'Ni', 'Se', 'Fi'],
    'ENTJ': ['Te', 'Ni', 'Se', 'Fi', 'Ti', 'Ne', 'Si', 'Fe'],
    'ENTP': ['Ne', 'Ti', 'Fe', 'Si', 'Ni', 'Te', 'Fi', 'Se'],
    'INFJ': ['Ni', 'Fe', 'Ti', 'Se', 'Ne', 'Fi', 'Te', 'Si'],
    'INFP': ['Fi', 'Ne', 'Si', 'Te', 'Fe', 'Ni', 'Se', 'Ti'],
    'ENFJ': ['Fe', 'Ni', 'Se', 'Ti', 'Fi', 'Ne', 'Si', 'Te'],
    'ENFP': ['Ne', 'Fi', 'Te', 'Si', 'Ni', 'Fe', 'Ti', 'Se'],
    'ISTJ': ['Si', 'Te', 'Fi', 'Ne', 'Se', 'Ti', 'Fe', 'Ni'],
    'ISFJ': ['Si', 'Fe', 'Ti', 'Ne', 'Se', 'Fi', 'Te', 'Ni'],
    'ESTJ': ['Te', 'Si', 'Ne', 'Fi', 'Ti', 'Se', 'Ni', 'Fe'],
    'ESFJ': ['Fe', 'Si', 'Ne', 'Ti', 'Fi', 'Se', 'Ni', 'Te'],
    'ISTP': ['Ti', 'Se', 'Ni', 'Fe', 'Te', 'Si', 'Ne', 'Fi'],
    'ISFP': ['Fi', 'Se', 'Ni', 'Te', 'Fe', 'Si', 'Ne', 'Ti'],
    'ESTP': ['Se', 'Ti', 'Fe', 'Ni', 'Si', 'Te', 'Fi', 'Ne'],
    'ESFP': ['Se', 'Fi', 'Te', 'Ni', 'Si', 'Fe', 'Ti', 'Ne'],
}

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def run_full_scoring(
    answers: List[Answer],
    questions: List[Question],
    validation_result: Optional[Dict] = None,
) -> MBTIResult:
    '''
    Run the complete scoring pipeline and return a fully-populated MBTIResult.

    Parameters
    ----------
    answers : list[Answer]
        All answers submitted by the test-taker.
    questions : list[Question]
        Full question bank used in the test.
    validation_result : dict or None
        Dict produced by the validation module containing:
            'passed'             -> bool
            'details'            -> dict
            'consistency_score'  -> float

    Returns
    -------
    MBTIResult
        Complete result dataclass ready for report generation.
    '''
    if validation_result is None:
        validation_result = {}

    # 1. Raw dimension scores
    dim_scores = calculate_dimension_scores(answers, questions)

    # 2. Percentage breakdown per pole
    dim_pcts = calculate_dimension_percentages(dim_scores, questions)

    # 3. Four-letter type code
    type_code = determine_type_code(dim_scores)

    # 4. Function stack for this type
    function_stack = FUNCTION_STACKS.get(type_code, [])

    # 5. Two-stage function scores
    func_scores = calculate_function_scores(type_code, dim_scores)

    # 6. Human-readable labels for each position
    func_labels = _build_function_labels(function_stack)

    return MBTIResult(
        type_code=type_code,
        dimension_scores=dim_scores,
        dimension_percentages=dim_pcts,
        function_scores=func_scores,
        function_stack=function_stack,
        function_labels=func_labels,
        validation_passed=validation_result.get('passed', True),
        validation_details=validation_result.get('details', {}),
        consistency_score=validation_result.get('consistency_score', 0.0),
        answers=answers,
    )


def calculate_dimension_scores(
    answers: List[Answer],
    questions: List[Question],
) -> Dict[str, float]:
    '''
    Compute raw scores for each of the four dichotomies (EI, SN, TF, JP).

    Each answer's Likert value (0-4) is centred at zero (subtract 2),
    multiplied by the question's direction and weight, then accumulated
    into the appropriate dichotomy bucket. Validation items are skipped.
    '''
    scores: Dict[str, float] = {d: 0.0 for d in DICHOTOMIES}
    q_map: Dict[int, Question] = {q.id: q for q in questions}

    for answer in answers:
        q = q_map.get(answer.question_id)
        if q is None or q.is_validation:
            continue
        contribution = (answer.value - 2) * q.direction * q.weight
        scores[q.dichotomy] += contribution

    return scores


def calculate_dimension_percentages(
    dimension_scores: Dict[str, float],
    questions: List[Question],
) -> Dict[str, Dict[str, float]]:
    '''
    Convert raw dimension scores into percentage pairs for each pole.

    Example return value for EI when the score is positive (leaning E):
        {'EI': {'E': 62.5, 'I': 37.5}}

    The percentage is clamped to [0, 100] and is computed relative to the
    maximum possible absolute score for that dichotomy (accounting for weights).
    '''
    # Compute per-dichotomy max-possible absolute score
    max_by_dichotomy: Dict[str, float] = {d: 0.0 for d in DICHOTOMIES}
    for q in questions:
        if q.is_validation:
            continue
        max_by_dichotomy[q.dichotomy] += 2.0 * q.weight

    percentages: Dict[str, Dict[str, float]] = {}

    for dichotomy in DICHOTOMIES:
        score = dimension_scores.get(dichotomy, 0.0)
        max_possible = max_by_dichotomy.get(dichotomy, 1.0)
        if max_possible <= 0.0:
            max_possible = 1.0

        first = dichotomy[0]
        second = dichotomy[1]

        if score >= 0:
            pct = min(100.0, 50.0 + (score / max_possible) * 50.0)
            percentages[dichotomy] = {first: pct, second: 100.0 - pct}
        else:
            pct = min(100.0, 50.0 + (abs(score) / max_possible) * 50.0)
            percentages[dichotomy] = {second: pct, first: 100.0 - pct}

    return percentages


def determine_type_code(
    dimension_scores: Dict[str, float],
) -> str:
    '''
    Determine the four-letter MBTI code from raw dimension scores.

    A non-negative score picks the first letter of the dichotomy pair;
    a negative score picks the second.
    '''
    code_parts: List[str] = []
    for dichotomy in DICHOTOMIES:
        if dimension_scores.get(dichotomy, 0.0) >= 0:
            code_parts.append(dichotomy[0])
        else:
            code_parts.append(dichotomy[1])
    return ''.join(code_parts)


def get_preference_strength(score: float) -> str:
    '''
    Classify the strength of a dimensional preference.

    Returns one of:
        'slight'   — absolute score < PREFERENCE_SLIGHT
        'moderate' — between PREFERENCE_SLIGHT and PREFERENCE_MODERATE
        'clear'    — at or above PREFERENCE_MODERATE
    '''
    abs_score = abs(score)
    if abs_score < PREFERENCE_SLIGHT:
        return 'slight'
    if abs_score < PREFERENCE_MODERATE:
        return 'moderate'
    return 'clear'


def calculate_function_scores(
    type_code: str,
    dimension_scores: Dict[str, float],
) -> Dict[str, float]:
    '''
    Two-stage cognitive-function score calculation.

    Stage 1 — Theoretical base
        Assigns a fixed base score per stack position using
        FUNCTION_BASE_SCORES (dominant=85, auxiliary=70, …, shadow_inferior=8).

    Stage 2 — Activation offset
        Adjusts each function score based on how much the test-taker's actual
        dimension preferences *activate* that function.

        For a function with orientation O ∈ {E, I} and axis A ∈ {N, S, T, F}:
            - orientation alignment = how strongly the person's EI score
              matches O
            - axis alignment       = how strongly the person's SN or TF score
              matches A

        The two alignments are averaged, scaled by FUNCTION_ACTIVATION_RANGE,
        and added to the base score.  Final scores are clamped to [0, 100].
    '''
    stack = FUNCTION_STACKS.get(type_code, [])
    if not stack:
        return {}

    # -- Stage 1: Theoretical base -------------------------------------------
    position_keys = [
        'dominant', 'auxiliary', 'tertiary', 'inferior',
        'shadow_dominant', 'shadow_auxiliary', 'shadow_tertiary', 'shadow_inferior',
    ]
    base_scores: Dict[str, float] = {}
    for i, func in enumerate(stack):
        base_scores[func] = FUNCTION_BASE_SCORES.get(position_keys[i], 0.0)

    # -- Stage 2: Activation offset ------------------------------------------
    # Normalise each dimension score to [-1, 1] via QUESTIONS_PER_DICHOTOMY
    max_possible = QUESTIONS_PER_DICHOTOMY * 2.0
    dim_norm: Dict[str, float] = {}
    for d in DICHOTOMIES:
        raw = dimension_scores.get(d, 0.0)
        clamped = max(-max_possible, min(max_possible, raw))
        dim_norm[d] = clamped / max_possible if max_possible > 0 else 0.0

    # Attribute lookup: function symbol -> (orientation, axis)
    func_attrs: Dict[str, Tuple[str, str]] = {
        'Ne': ('E', 'N'), 'Ni': ('I', 'N'),
        'Se': ('E', 'S'), 'Si': ('I', 'S'),
        'Te': ('E', 'T'), 'Ti': ('I', 'T'),
        'Fe': ('E', 'F'), 'Fi': ('I', 'F'),
    }

    result: Dict[str, float] = {}
    for func in stack:
        orient, axis = func_attrs.get(func, ('E', 'N'))

        # How much the person's E/I matches this function's orientation
        if orient == 'E':
            ei_align = dim_norm['EI']        # positive when person leans E
        else:
            ei_align = -dim_norm['EI']        # positive when person leans I

        # How much the person's SN/TF matches this function's axis
        if axis in ('N', 'S'):
            axis_align = dim_norm['SN'] if axis == 'N' else -dim_norm['SN']
        else:
            axis_align = dim_norm['TF'] if axis == 'T' else -dim_norm['TF']

        # Combined alignment in [-1, 1]
        alignment = max(-1.0, min(1.0, (ei_align + axis_align) / 2.0))
        offset = alignment * FUNCTION_ACTIVATION_RANGE

        # Final score: base + offset, clamped to [0, 100]
        raw_score = base_scores[func] + offset
        result[func] = max(0.0, min(100.0, raw_score))

    return result


def _build_function_labels(function_stack: List[str]) -> Dict[str, str]:
    '''
    Map each function symbol in the stack to its position label.

    Example:
        {'Ni': 'Dominant', 'Te': 'Auxiliary', 'Fi': 'Tertiary', …}
    '''
    order_labels = [
        'Dominant',
        'Auxiliary',
        'Tertiary',
        'Inferior',
        'Opposing Role',
        'Critical Parent',
        'Blindspot',
        'Demonstrative',
    ]
    return {
        func: order_labels[i]
        for i, func in enumerate(function_stack)
        if i < len(order_labels)
    }
