"""Export report as TXT file."""
from datetime import datetime

def export_txt(result, report_sections, filepath):
    lines = []
    lines.append("=" * 62)
    lines.append("  MBTI Personality Test - Expert Analysis Report")
    lines.append("=" * 62)
    lines.append("")
    lines.append(f"  Export Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"  Type: {result.type_code} - {result.type_nickname}")
    lines.append(f"  Consistency: {result.consistency_score:.2f}")
    lines.append("")

    lines.append("-" * 62)
    lines.append("  Dimension Scores")
    lines.append("-" * 62)
    for dim in ["EI", "SN", "TF", "JP"]:
        pcts = result.dimension_percentages.get(dim, {})
        if pcts:
            k1, k2 = list(pcts.keys())
            lines.append(f"  {dim}: {k1}={pcts[k1]}% | {k2}={pcts[k2]}%")
    lines.append("")

    lines.append("-" * 62)
    lines.append("  Cognitive Function Scores")
    lines.append("-" * 62)
    for i, func in enumerate(result.function_stack):
        score = result.function_scores.get(func, 0)
        bar = "#" * int(score / 5) + "-" * (20 - int(score / 5))
        label = result.function_labels.get(func, "")
        lines.append(f"  {i+1}. {func}  {bar}  {score:.1f}  ({label})")
    lines.append("")

    titles = {"core_traits": "1. Core Traits", "function_analysis": "2. Function Analysis",
              "strengths": "3. Strengths", "weaknesses": "4. Weaknesses & Stress",
              "careers": "5. Career Fit", "relationships": "6. Relationships",
              "growth": "7. Growth Plan"}
    for key, title in titles.items():
        lines.append("")
        lines.append("=" * 62)
        lines.append(f"  {title}")
        lines.append("=" * 62)
        lines.append("")
        lines.append(report_sections.get(key, ""))

    lines.append("")
    lines.append("=" * 62)
    lines.append("  * This report is for reference only, not clinical diagnosis")
    lines.append("=" * 62)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
