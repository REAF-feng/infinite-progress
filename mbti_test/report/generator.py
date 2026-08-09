"""Report generator - assembles expert analysis from type profiles and function data."""
from data.type_profiles import TYPE_PROFILES
from data.function_descriptions import FUNCTION_DETAIL, FUNCTION_ORDER_LABELS
from report.text_blocks import FUNCTION_STRENGTH, DISCLAIMER, STRESS_RESPONSE


def generate_full_report(result):
    type_code = result.type_code
    profile = TYPE_PROFILES.get(type_code, TYPE_PROFILES.get("INTJ", {}))
    return {
        "core_traits": _build_core_traits(result, profile),
        "function_analysis": _build_function_analysis(result, profile),
        "strengths": _build_strengths(result, profile),
        "weaknesses": _build_weaknesses(result, profile),
        "careers": _build_careers(result, profile),
        "relationships": _build_relationships(result, profile),
        "growth": _build_growth(result, profile),
    }


def _build_core_traits(result, profile):
    tc = result.type_code
    nn = profile.get("nickname", tc)
    brief = profile.get("brief", "")
    dom = profile.get("dominant_desc", "")
    aux = profile.get("auxiliary_desc", "")
    traits = profile.get("core_traits", [])
    keywords = profile.get("keywords", [])

    lines = []
    lines.append(f"人格类型: {tc} - {nn}")
    lines.append(f"核心画像: {brief}")
    lines.append("")
    lines.append("【认知功能架构】")
    lines.append(f"  主导: {dom}")
    lines.append(f"  辅助: {aux}")
    lines.append("")
    lines.append("【底层行为模式】")
    for i, t in enumerate(traits, 1):
        lines.append(f"  {i}. {t}")
    lines.append("")
    lines.append(f"【核心关键词】{' / '.join(keywords)}")
    lines.append("")

    # Dimension percentages
    lines.append("【四维度偏好分析】")
    dim_names = {"EI": "精力获取方式", "SN": "信息接收方式",
                 "TF": "决策判断方式", "JP": "生活态度取向"}
    for dim_key, dim_name in dim_names.items():
        pcts = result.dimension_percentages.get(dim_key, {})
        if pcts:
            k1, k2 = list(pcts.keys())
            lines.append(f"  {dim_name}: {k1}={pcts[k1]}% / {k2}={pcts[k2]}%")
    return "\n".join(lines)


def _build_function_analysis(result, profile):
    lines = []
    lines.append("你的荣格八维认知功能得分及排序如下:")
    lines.append("")

    sorted_funcs = result.function_stack
    for i, func in enumerate(sorted_funcs):
        score = result.function_scores.get(func, 0)
        label = result.function_labels.get(func, "")
        pos_name = FUNCTION_ORDER_LABELS[i] if i < len(FUNCTION_ORDER_LABELS) else ""
        lines.append(f"  {i+1}. {func} - {score:.1f}/100")
        lines.append(f"     {label if label else pos_name}")
        lines.append("")

    lines.append("【各功能运作详析】")
    for func in sorted_funcs[:4]:
        score = result.function_scores.get(func, 0)
        detail = FUNCTION_DETAIL.get(func, {})
        name = detail.get("name", func)
        essence = detail.get("essence", "")

        level = "high" if score > 65 else ("mid" if score > 35 else "low")
        personalized = FUNCTION_STRENGTH.get(func, {}).get(level, "")

        lines.append(f"  [{func}] {name} (得分: {score:.1f})")
        lines.append(f"  本质: {essence}")
        lines.append(f"  个性化解读: {personalized}")
        lines.append("")

    # Stress warning
    if len(sorted_funcs) >= 4:
        infer = sorted_funcs[3]
        inf_detail = FUNCTION_DETAIL.get(infer, {})
        lines.append(f"【劣势功能警示 - {infer}】")
        lines.append(STRESS_RESPONSE)
        lines.append(f"你的劣势功能 {infer} 在压力下可能出现: {inf_detail.get('weakness', '')}")
        lines.append(f"发展建议: {inf_detail.get('development', '')}")
        lines.append("")

    return "\n".join(lines)


def _build_strengths(result, profile):
    lines = []
    strengths = profile.get("strengths", [])
    lines.append("【核心天赋领域】")
    for i, s in enumerate(strengths, 1):
        lines.append(f"  {i}. {s}")
    lines.append("")

    sorted_funcs = result.function_stack
    if len(sorted_funcs) >= 2:
        dom_func = sorted_funcs[0]
        aux_func = sorted_funcs[1]
        dom_d = FUNCTION_DETAIL.get(dom_func, {})
        aux_d = FUNCTION_DETAIL.get(aux_func, {})
        lines.append(f"你的主导功能 {dom_func} 与辅助功能 {aux_func} 的组合赋予你独特的认知优势:")
        lines.append(f"  {dom_d.get('strength', '')}")
        lines.append(f"  {aux_d.get('strength', '')}")
    return "\n".join(lines)


def _build_weaknesses(result, profile):
    lines = []
    weaknesses = profile.get("weaknesses", [])
    lines.append("【认知盲区与内在挑战】")
    for i, w in enumerate(weaknesses, 1):
        lines.append(f"  {i}. {w}")
    lines.append("")

    lines.append("【内耗来源分析】")
    lines.append("  1. 当环境要求你频繁使用劣势功能时")
    lines.append("  2. 当你的核心价值观受到挑战时")
    lines.append("  3. 长期处于与自身认知偏好对立的环境中")
    return "\n".join(lines)


def _build_careers(result, profile):
    lines = []
    careers = profile.get("careers", [])
    lines.append("【推荐职业赛道】")
    lines.append(f"  基于你的 {result.type_code} 人格类型, 以下领域与你的天然认知偏好高度匹配:")
    for i, c in enumerate(careers, 1):
        lines.append(f"  {i}. {c}")
    lines.append("")
    lines.append("【适配工作环境特征】")
    lines.append("  - 能够发挥你主导功能优势的专业领域")
    lines.append("  - 重视能力和成果而非关系和资历的组织文化")
    lines.append("  - 有明确目标和反馈机制的工作结构")
    return "\n".join(lines)


def _build_relationships(result, profile):
    lines = []
    rel_text = profile.get("relationships", "")
    lines.append("【人际交往特征】")
    lines.append(f"  {rel_text}")
    lines.append("")
    lines.append("【沟通风格与深层需求】")
    lines.append(f"  你在关系中寻求的是理解、深度和真实的连接。")
    lines.append(f"  在亲密关系中，你需要伴侣理解你独特的认知方式。")
    return "\n".join(lines)


def _build_growth(result, profile):
    lines = []
    growth = profile.get("growth", [])
    lines.append("【核心成长路径】")
    for i, g in enumerate(growth, 1):
        lines.append(f"  {i}. {g}")
    lines.append("")

    sorted_funcs = result.function_stack
    if len(sorted_funcs) >= 4:
        infer = sorted_funcs[3]
        inf_detail = FUNCTION_DETAIL.get(infer, {})
        lines.append("【劣势功能发展专项训练】")
        lines.append(f"  你的劣势功能 {infer} 是成长的关键突破口:")
        lines.append(f"  {inf_detail.get('development', '')}")
        lines.append("")

    lines.append("【30天自我觉察练习】")
    lines.append("  第1周: 每天记录3次使用劣势功能的情境")
    lines.append("  第2周: 在低压环境中刻意练习劣势功能")
    lines.append("  第3周: 在安全关系中练习情感表达或逻辑分析")
    lines.append("  第4周: 回顾变化并记录认知灵活性上的进步")
    lines.append("")
    lines.append(DISCLAIMER)
    return "\n".join(lines)
