'''
Anti-cheat module for MBTI test.

Validates answer integrity by detecting rushed responses,
suspicious answer patterns, and cross-dimension inconsistencies.
'''

from config import (
    MIN_RESPONSE_TIME_MS,
    RUSHED_THRESHOLD_PCT,
    CONSISTENCY_PASS_THRESHOLD,
    MAX_CONSECUTIVE_SAME,
    LIKERT_MIN,
    LIKERT_MAX,
    DICHOTOMIES,
)


def validate_answers(answers, questions):
    '''
    Main validation entry point.

    Args:
        answers: list of Answer objects (question_id, value, timestamp_ms).
        questions: list of Question objects (id, dichotomy, direction, ...).

    Returns:
        dict with keys:
            passed (bool)
            warnings (list[str])
            details (dict)
            consistency_score (float, 0.0-1.0)
    '''
    rushed = _check_rushed_answers(answers)
    pattern = _check_answer_pattern(answers)
    cv = _check_cross_validation(answers, questions)
    consistency = _calculate_consistency(rushed, pattern, cv)

    warnings = []

    if rushed['flagged']:
        warnings.append(
            f'{rushed["rushed_pct"]}% of answers completed too quickly '
            f'({rushed["rushed_count"]} of {rushed["total_count"]})'
        )

    if pattern['straight_line']:
        warnings.append(
            f'All answers identical (value={pattern["details"]["all_same_value"]})'
        )
    elif pattern['alternating']:
        warnings.append(
            'Answers follow an alternating pattern suggestive of random selection'
        )
    elif pattern['long_streak']:
        streak = pattern['details']['max_streak']
        warnings.append(
            f'A run of {streak} consecutive identical answers was detected'
        )

    if not cv['pass']:
        low_dims = [
            d for d, r in cv['dimensions'].items()
            if r['consistency'] < CONSISTENCY_PASS_THRESHOLD
        ]
        warnings.append(
            f'Low cross-validation consistency in dimensions: {", ".join(low_dims)}'
        )

    passed = (
        not rushed['flagged']
        and not pattern['straight_line']
        and not pattern['alternating']
        and not pattern['long_streak']
        and cv['pass']
    )

    return {
        'passed': passed,
        'warnings': warnings,
        'details': {
            'rushed': rushed,
            'pattern': pattern,
            'cross_validation': cv,
        },
        'consistency_score': consistency,
    }


def _check_rushed_answers(answers):
    '''
    Detect answers submitted abnormally fast.

    An answer is considered rushed when its timestamp_ms is positive
    (present) but below MIN_RESPONSE_TIME_MS.

    Returns:
        dict with rushed_count, total_count, rushed_pct,
             rushed_ids (question ids), and flagged (bool).
    '''
    if not answers:
        return {
            'rushed_count': 0,
            'total_count': 0,
            'rushed_pct': 0.0,
            'rushed_ids': [],
            'flagged': False,
        }

    rushed_ids = []
    for a in answers:
        if a.timestamp_ms > 0 and a.timestamp_ms < MIN_RESPONSE_TIME_MS:
            rushed_ids.append(a.question_id)

    total = len(answers)
    count = len(rushed_ids)
    pct = (count / total * 100) if total > 0 else 0.0

    return {
        'rushed_count': count,
        'total_count': total,
        'rushed_pct': round(pct, 1),
        'rushed_ids': rushed_ids,
        'flagged': pct > RUSHED_THRESHOLD_PCT,
    }


def _check_answer_pattern(answers):
    '''
    Detect suspicious answer sequences:
      - straight_line: every answer is the same Likert value.
      - long_streak: run of identical values >= MAX_CONSECUTIVE_SAME.
      - alternating: perfect binary oscillation between two values.

    Returns:
        dict with boolean flags and a details sub-dict.
    '''
    sorted_answers = sorted(answers, key=lambda a: a.question_id)
    values = [a.value for a in sorted_answers]
    n = len(values)

    result = {
        'straight_line': False,
        'long_streak': False,
        'alternating': False,
        'details': {},
    }

    if n == 0:
        return result

    unique = set(values)

    # --- straight line ---
    if len(unique) == 1:
        result['straight_line'] = True
        result['details'] = {
            'all_same_value': values[0],
            'max_streak': n,
        }
        return result

    # --- long streak ---
    max_streak = 1
    cur = 1
    for i in range(1, n):
        if values[i] == values[i - 1]:
            cur += 1
            if cur > max_streak:
                max_streak = cur
        else:
            cur = 1

    has_long_streak = max_streak >= MAX_CONSECUTIVE_SAME

    # --- alternating ---
    is_alternating = False
    alt_data = {}
    if len(unique) == 2 and n >= 4:
        v_a, v_b = sorted(unique)
        perfect = True
        for i in range(n - 1):
            if not ((values[i] == v_a and values[i + 1] == v_b) or
                    (values[i] == v_b and values[i + 1] == v_a)):
                perfect = False
                break
        if perfect:
            is_alternating = True
            alt_data = {
                'alternating_values': [v_a, v_b],
                'perfect': True,
            }

    result['long_streak'] = has_long_streak
    result['alternating'] = is_alternating
    result['details'] = {
        'max_streak': max_streak,
        'unique_values': len(unique),
    }
    result['details'].update(alt_data)

    return result


def _check_cross_validation(answers, questions):
    '''
    Measure consistency within each MBTI dichotomy by comparing
    forward-direction answers (direction=+1) against inverted
    reverse-direction answers (direction=-1).

    For each dimension:
      - Forward mean  = average raw Likert value of forward questions.
      - Rev-inv mean  = average of (LIKERT_MAX - raw) for reverse questions.
      - Consistency   = 1 - |forward_mean - rev_inv_mean| / LIKERT_MAX

    Returns:
        dict with overall score, per-dimension breakdown, and pass flag.
    '''
    answer_map = {a.question_id: a.value for a in answers if a.value is not None}
    question_map = {q.id: q for q in questions}

    dim_results = {}

    for dim in DICHOTOMIES:
        forward_vals = []
        reverse_vals = []

        for q in questions:
            if q.dichotomy != dim:
                continue
            if q.id not in answer_map:
                continue
            val = answer_map[q.id]
            if q.direction == 1:
                forward_vals.append(val)
            else:
                reverse_vals.append(val)

        if forward_vals and reverse_vals:
            mean_fwd = sum(forward_vals) / len(forward_vals)
            mean_rev_inv = sum(LIKERT_MAX - v for v in reverse_vals) / len(reverse_vals)
            diff = abs(mean_fwd - mean_rev_inv) / LIKERT_MAX
            consistency = 1.0 - diff
        else:
            consistency = 1.0

        f_mean = round(sum(forward_vals) / len(forward_vals), 2) if forward_vals else None
        r_mean = round(sum(reverse_vals) / len(reverse_vals), 2) if reverse_vals else None

        dim_results[dim] = {
            'consistency': round(consistency, 4),
            'forward_mean': f_mean,
            'reverse_mean_raw': r_mean,
        }

    overall = (
        sum(r['consistency'] for r in dim_results.values()) / len(dim_results)
        if dim_results
        else 1.0
    )

    return {
        'overall': round(overall, 4),
        'dimensions': dim_results,
        'pass': overall >= CONSISTENCY_PASS_THRESHOLD,
    }


def _calculate_consistency(rushed_result, pattern_result, cv_result):
    '''
    Combine sub-scores into a single 0.0-1.0 consistency score.

    Weights:
      - rushed score:         30%
      - pattern score:        30%
      - cross-validation:     40%

    Returns:
        float in [0.0, 1.0].
    '''
    # Rushed component
    rushed_pct = rushed_result['rushed_pct']
    rushed_score = max(0.0, 1.0 - rushed_pct / 100.0)

    # Pattern component
    pattern_score = 1.0
    if pattern_result['straight_line']:
        pattern_score = 0.0
    elif pattern_result['alternating']:
        pattern_score = 0.1
    elif pattern_result['long_streak']:
        streak = pattern_result['details']['max_streak']
        over = streak - MAX_CONSECUTIVE_SAME
        pattern_score = max(0.0, 1.0 - over * 0.15)

    # Cross-validation component
    cv_score = cv_result['overall']

    consistency = 0.3 * rushed_score + 0.3 * pattern_score + 0.4 * cv_score
    return round(min(1.0, max(0.0, consistency)), 4)
