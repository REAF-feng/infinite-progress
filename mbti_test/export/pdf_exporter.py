"""Export report as PDF using reportlab."""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def _register_cjk_font():
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                pdfmetrics.registerFont(TTFont("CJK", fp))
                return "CJK"
            except Exception:
                continue
    return "Helvetica"

def export_pdf(result, report_sections, filepath):
    font = _register_cjk_font()
    doc = SimpleDocTemplate(filepath, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm,
                            title=f"MBTI Report - {result.type_code}",
                            author="MBTI Personality Test v2.0")
    fn = font
    title_s = ParagraphStyle("T", fontName=fn, fontSize=26, leading=34,
                             textColor=HexColor("#0F3460"), alignment=TA_CENTER, spaceAfter=8)
    subtitle_s = ParagraphStyle("ST", fontName=fn, fontSize=14, leading=20,
                                textColor=HexColor("#636E72"), alignment=TA_CENTER, spaceAfter=20)
    heading_s = ParagraphStyle("H", fontName=fn, fontSize=16, leading=24,
                               textColor=HexColor("#0F3460"), spaceBefore=18, spaceAfter=10)
    body_s = ParagraphStyle("B", fontName=fn, fontSize=10, leading=17,
                            textColor=HexColor("#2D3436"), alignment=TA_JUSTIFY,
                            spaceAfter=6, firstLineIndent=20)
    small_s = ParagraphStyle("S", fontName=fn, fontSize=8, leading=12,
                             textColor=HexColor("#B2BEC3"), alignment=TA_CENTER)

    elements = []
    # Cover
    elements.append(Spacer(1, 4*cm))
    elements.append(Paragraph("MBTI Personality Test", title_s))
    elements.append(Paragraph("Expert Analysis Report", subtitle_s))
    elements.append(Spacer(1, 1.5*cm))
    elements.append(HRFlowable(width="80%", thickness=1, color=HexColor("#E94560")))
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph(f'<font size="48" color="#E94560"><b>{result.type_code}</b></font>',
                              ParagraphStyle("TB", fontName=fn, fontSize=48,
                                             textColor=HexColor("#E94560"), alignment=TA_CENTER)))
    elements.append(Paragraph(f"[{result.type_nickname}]",
                              ParagraphStyle("NN", fontName=fn, fontSize=22,
                                             textColor=HexColor("#2D3436"), alignment=TA_CENTER)))
    elements.append(Spacer(1, 1.5*cm))
    elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", body_s))
    elements.append(Paragraph(f"Consistency: {result.consistency_score:.2f}", body_s))
    elements.append(PageBreak())

    # Dimension scores
    elements.append(Paragraph("Dimension Scores", heading_s))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#E94560")))
    elements.append(Spacer(1, 0.5*cm))
    for dim_key in ["EI", "SN", "TF", "JP"]:
        pcts = result.dimension_percentages.get(dim_key, {})
        if pcts:
            k1, k2 = list(pcts.keys())
            v1, v2 = pcts[k1], pcts[k2]
            elements.append(Paragraph(f"<b>{dim_key}</b>: {k1}={v1}% | {k2}={v2}%", body_s))
    elements.append(PageBreak())

    # Function scores
    elements.append(Paragraph("Cognitive Function Scores", heading_s))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#E94560")))
    elements.append(Spacer(1, 0.5*cm))
    func_data = [["Function", "Score", "Level"]]
    for func in result.function_stack:
        score = result.function_scores.get(func, 0)
        label = result.function_labels.get(func, "")
        func_data.append([Paragraph(f"<b>{func}</b>", small_s),
                          Paragraph(f"{score:.1f}", small_s),
                          Paragraph(label[:20], small_s)])
    ft = Table(func_data, colWidths=[3*cm, 3*cm, 8*cm])
    ft.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#0F3460")),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#FFFFFF")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#E0E0E0")),
    ]))
    elements.append(ft)
    elements.append(PageBreak())

    # Report sections
    titles = {"core_traits": "1. Core Personality Traits",
              "function_analysis": "2. Cognitive Function Analysis",
              "strengths": "3. Strengths & Talents",
              "weaknesses": "4. Blind Spots & Stress Patterns",
              "careers": "5. Career Development",
              "relationships": "6. Relationships & Compatibility",
              "growth": "7. Self-Growth Plan"}
    for key, title in titles.items():
        elements.append(Paragraph(title, heading_s))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#E94560")))
        elements.append(Spacer(1, 0.3*cm))
        content = report_sections.get(key, "")
        for para in content.split("\n"):
            para = para.strip()
            if para and not para.startswith("=") and not para.startswith("-"):
                elements.append(Paragraph(para, body_s))
        elements.append(PageBreak())

    # Disclaimer
    elements.append(Spacer(1, 3*cm))
    elements.append(HRFlowable(width="80%", thickness=1, color=HexColor("#E94560")))
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph("Disclaimer", heading_s))
    elements.append(Paragraph(
        "This report is based on Jungian cognitive function theory and the MBTI framework. "
        "MBTI describes healthy personality preferences, not clinical diagnoses. "
        "Please use this report as a reference tool for self-exploration.",
        body_s))
    elements.append(Spacer(1, 2*cm))
    elements.append(Paragraph(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | MBTI v2.0", small_s))

    doc.build(elements)
