from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


OUT = Path("docs/kiran_15_min_demo_brief.pdf")


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.6 * inch,
        title="15-Minute Demo Plan - Requirements Gap Analysis Agent",
    )
    styles = build_styles()
    story = []

    story.append(Paragraph("15-Minute Demo Plan", styles["TitleCustom"]))
    story.append(Paragraph("Requirements Gap Analysis Agent in PyCharm", styles["SubtitleCustom"]))
    story.append(
        callout(
            styles,
            "Message for Kiran",
            "In our 15-minute call, I will show a working product-grade AI pipeline that analyzes large business and engineering transcripts, finds requirement coverage gaps, and generates a verified report.",
        )
    )
    story.append(Spacer(1, 8))

    story.append(Paragraph("What I Will Show", styles["H1"]))
    story.append(
        bullets(
            styles,
            [
                "A PyCharm-ready Python project for requirements gap analysis.",
                "Qwen3:8B through Ollama for local LLM reasoning.",
                "BAAI/bge-m3 for open-source semantic embeddings.",
                "Large transcript mode with chunking, retrieval, focused analysis, and report generation.",
            ],
        )
    )

    story.append(Paragraph("Why This Is Useful", styles["H1"]))
    story.append(
        Paragraph(
            "Business teams describe requirements in meetings, while engineering teams describe implementation decisions separately. The product compares both sides and identifies what is covered, partially covered, deferred, or missing.",
            styles["Body"],
        )
    )

    story.append(Paragraph("End-to-End Pipeline", styles["H1"]))
    data = [
        ["Stage", "What happens"],
        ["1. Load", "Read business and engineering transcripts."],
        ["2. Chunk", "Split large transcripts into overlapping chunks to avoid context overflow."],
        ["3. Extract", "Use Qwen to extract requirements and engineering solutions as structured JSON."],
        ["4. Merge", "Deduplicate repeated items from overlapping chunks."],
        ["5. Retrieve", "Use BGE-M3 embeddings to retrieve top-k candidate solutions for each requirement."],
        ["6. Analyze", "Use Qwen for focused gap analysis over only relevant evidence."],
        ["7. Verify", "Use Qwen critic verification to reduce false positives."],
        ["8. Report", "Write final Markdown or JSON gap reports."],
    ]
    story.append(table(data, [1.35 * inch, 5.25 * inch], styles))

    story.append(Paragraph("What Makes It Product-Grade", styles["H1"]))
    story.append(
        bullets(
            styles,
            [
                "Config-driven model selection and local open-source execution.",
                "Modular layers: schemas, parsers, chunking, agents, retrieval, merge, reporting.",
                "Tests for chunking, deduplication, retrieval, LLM parsing, and pipeline behavior.",
                "Scalable design: current local vector index can later be replaced by Qdrant or Supabase pgvector.",
            ],
        )
    )

    story.append(Paragraph("Demo Command", styles["H1"]))
    story.append(
        code(
            styles,
            "python main.py --mode large --config configs/qwen_local.yaml --business transcripts/eval_business --engineering transcripts/eval_engineering --output piyush/eval_large_qwen.md --format markdown",
        )
    )

    story.append(
        callout(
            styles,
            "Main takeaway",
            "This is not just a prompt. It is an end-to-end AI system with transcript processing, open-source LLM extraction, embedding retrieval, focused reasoning, critic verification, and report generation.",
        )
    )

    doc.build(story)
    print(OUT)


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=22, leading=27, textColor=colors.HexColor("#1F4D78"), alignment=TA_CENTER, spaceAfter=4))
    styles.add(ParagraphStyle("SubtitleCustom", parent=styles["Normal"], fontName="Helvetica", fontSize=12, leading=15, textColor=colors.HexColor("#555555"), alignment=TA_CENTER, spaceAfter=14))
    styles.add(ParagraphStyle("H1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=colors.HexColor("#2E74B5"), spaceBefore=8, spaceAfter=5))
    styles.add(ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.2, textColor=colors.HexColor("#1F2937"), spaceAfter=5))
    styles.add(ParagraphStyle("CodeBlock", parent=styles["Code"], fontName="Courier", fontSize=7.2, leading=9, textColor=colors.HexColor("#111827")))
    return styles


def bullets(styles, items):
    return ListFlowable([ListItem(Paragraph(item, styles["Body"]), leftIndent=12) for item in items], bulletType="bullet", leftIndent=16, bulletFontSize=6)


def callout(styles, title, body):
    t = Table([[Paragraph(f"<b>{title}</b><br/>{body}", styles["Body"])]], colWidths=[6.6 * inch])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F6F9")), ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8E0EA")), ("PADDING", (0, 0), (-1, -1), 8)]))
    return t


def table(data, widths, styles):
    rows = [[Paragraph(str(cell), styles["Body"]) for cell in row] for row in data]
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF5")), ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C8D0DA")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("PADDING", (0, 0), (-1, -1), 5)]))
    return t


def code(styles, text):
    t = Table([[Paragraph(text, styles["CodeBlock"])]], colWidths=[6.6 * inch])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F4F7")), ("BOX", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")), ("PADDING", (0, 0), (-1, -1), 6)]))
    return t


if __name__ == "__main__":
    main()
