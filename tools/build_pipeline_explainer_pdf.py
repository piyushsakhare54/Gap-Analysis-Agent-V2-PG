from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUT_DIR = Path("docs")
PDF_PATH = OUT_DIR / "requirements_gap_pipeline_interview_guide.pdf"


BLUE = colors.HexColor("#2E74B5")
DARK_BLUE = colors.HexColor("#1F4D78")
LIGHT_BLUE = colors.HexColor("#E8EEF5")
LIGHT_GRAY = colors.HexColor("#F2F4F7")
INK = colors.HexColor("#1F2937")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.55 * inch,
        title="Requirements Gap Analysis Agent - Interview Guide",
    )
    styles = build_styles()
    story = []

    story.extend(title_page(styles))
    story.append(PageBreak())
    story.extend(problem_and_architecture(styles))
    story.append(PageBreak())
    story.extend(stage_walkthrough(styles))
    story.append(PageBreak())
    story.extend(qwen_mode_and_script(styles))
    story.append(PageBreak())
    story.extend(strengths_commands_and_close(styles))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(PDF_PATH)


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleCustom",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=30,
            textColor=DARK_BLUE,
            alignment=TA_CENTER,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubtitleCustom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#555555"),
            alignment=TA_CENTER,
            spaceAfter=20,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1Custom",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=BLUE,
            spaceBefore=4,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2Custom",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=16,
            textColor=DARK_BLUE,
            spaceBefore=8,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.4,
            leading=12,
            textColor=INK,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=10,
            textColor=INK,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeCustom",
            parent=styles["Code"],
            fontName="Courier",
            fontSize=7.3,
            leading=9.4,
            textColor=colors.HexColor("#111827"),
        )
    )
    return styles


def title_page(styles):
    return [
        Spacer(1, 0.55 * inch),
        Paragraph("Requirements Gap Analysis Agent", styles["TitleCustom"]),
        Paragraph("End-to-End Pipeline Interview Guide", styles["SubtitleCustom"]),
        callout(
            styles,
            "One-line explanation",
            "This system reads business and engineering transcripts, extracts requirements and solutions, retrieves the most relevant implementation evidence with open-source embeddings, then uses a local open-source LLM such as Qwen3-32B to analyze and verify gaps.",
        ),
        Spacer(1, 0.25 * inch),
        Paragraph("What you can say in an interview", styles["H1Custom"]),
        bullet_list(
            styles,
            [
                "I designed the pipeline for long real-world transcripts, not only short demo text.",
                "The system uses chunking to avoid LLM context overflow.",
                "It uses BAAI/bge-m3 embeddings for semantic retrieval.",
                "It uses Qwen3-32B through Ollama for extraction, gap analysis, and critic verification when qwen_local.yaml is selected.",
                "The output is a structured GapReport that can be written to Markdown, JSON, or JSONL.",
            ],
        ),
    ]


def problem_and_architecture(styles):
    story = [Paragraph("1. What Problem This Solves", styles["H1Custom"])]
    story.append(
        Paragraph(
            "Business teams describe expectations in meetings, while engineering teams describe what was implemented, deferred, or scoped out. The agent turns both sides into structured evidence and produces a verified requirements gap report.",
            styles["BodyCustom"],
        )
    )
    story.append(Spacer(1, 8))
    story.append(Paragraph("2. High-Level Architecture", styles["H1Custom"]))
    data = [
        ["Input", "Step 1", "Step 2", "Step 3 / Output"],
        ["Business transcripts", "Parser", "Chunker", "Qwen requirement extraction"],
        ["Engineering transcripts", "Parser", "Chunker", "Qwen solution extraction"],
        ["Extracted candidates", "Deduplication", "BGE-M3 embeddings", "Top-k retrieval"],
        ["Requirement + candidates", "Qwen focused gap analysis", "Qwen critic", "Report writers"],
    ]
    story.append(styled_table(data, [1.45 * inch, 1.45 * inch, 1.45 * inch, 2.1 * inch], header_fill=LIGHT_BLUE, font_size=8.3))
    story.append(Spacer(1, 8))
    story.append(
        callout(
            styles,
            "Core idea",
            "Do not compare every requirement with every engineering statement. Retrieve the most relevant candidate solutions first, then let Qwen reason over a focused evidence set.",
        )
    )
    story.append(Paragraph("3. Data Objects", styles["H1Custom"]))
    data = [
        ["Object", "Meaning"],
        ["Transcript", "One source file with speaker-tagged lines and original line numbers."],
        ["Chunk", "A small overlapping transcript window used for safe LLM calls."],
        ["Requirement", "A business need with statement, quote, line range, constraints, notes, and confidence."],
        ["Solution", "An engineering implementation or scope statement with tech stack, deferred work, and limits."],
        ["RetrievalMatch", "A cosine similarity match between one requirement and one solution."],
        ["Gap", "A verified finding: unaddressed, partial, or covered; only non-covered gaps are reported."],
    ]
    story.append(styled_table(data, [1.55 * inch, 4.9 * inch], header_fill=LIGHT_GRAY, font_size=8.2))
    return story


def stage_walkthrough(styles):
    story = [Paragraph("4. Each Pipeline Stage", styles["H1Custom"])]
    stages = [
        ("1", "Load transcripts", "Reads .txt, .md, and .jsonl files recursively.", "Keeps source path, speaker, and line numbers."),
        ("2", "Chunk transcripts", "Splits long files into overlapping windows.", "Avoids context overflow and preserves nearby context."),
        ("3", "Extract requirements", "Qwen turns business chunks into structured Requirement objects.", "Makes messy conversation machine-readable."),
        ("4", "Extract solutions", "Qwen turns engineering chunks into structured Solution objects.", "Captures built, deferred, and out-of-scope work."),
        ("5", "Deduplicate", "Merges repeated items caused by overlap.", "Keeps the report clean and readable."),
        ("6", "Embed text", "BGE-M3 converts requirements and solutions into vectors.", "Enables semantic search instead of keyword-only matching."),
        ("7", "Retrieve top-k", "For each requirement, find the top 5 likely solutions.", "Sends Qwen only focused evidence."),
        ("8", "Analyze gaps", "Qwen compares one requirement with candidate solutions.", "Classifies unaddressed or partial coverage."),
        ("9", "Critic verify", "Qwen reviews candidate gaps for false positives.", "Improves trust in the final report."),
        ("10", "Write report", "Outputs Markdown, JSON, or JSONL.", "Makes results useful for teams and review."),
    ]
    data = [["#", "Stage", "What happens", "Why it matters"], *stages]
    story.append(styled_table(data, [0.35 * inch, 1.2 * inch, 2.45 * inch, 2.45 * inch], header_fill=LIGHT_BLUE, font_size=7.6))
    return story


def qwen_mode_and_script(styles):
    story = [Paragraph("5. Standard Mode vs Large Qwen Mode", styles["H1Custom"])]
    data = [
        ["Area", "Standard mode", "Large Qwen mode"],
        ["Command", "Default when --mode is omitted", "--mode large --config configs/qwen_local.yaml"],
        ["Best for", "Small tests and fallback demo", "Large transcript datasets"],
        ["Extraction", "Heuristic in default config", "Qwen3-32B through Ollama"],
        ["Embeddings", "Hashing fallback", "BAAI/bge-m3"],
        ["Gap reasoning", "Deterministic rules", "Qwen focused comparison"],
        ["Failure behavior", "Always runnable", "Fails clearly if Qwen is unavailable"],
    ]
    story.append(styled_table(data, [1.25 * inch, 2.35 * inch, 2.85 * inch], header_fill=LIGHT_GRAY, font_size=8.0))
    story.append(Spacer(1, 8))
    story.append(Paragraph("6. Interview Script", styles["H1Custom"]))
    story.append(
        callout(
            styles,
            "30-second answer",
            "I built a requirements gap analysis agent for long transcripts. It chunks business and engineering conversations, uses Qwen to extract structured requirements and solutions, deduplicates overlap, embeds the items with BGE-M3, retrieves top-k matching solutions for each requirement, and then asks Qwen to perform focused gap analysis and critic verification before writing a report.",
        )
    )
    story.append(Paragraph("If asked why chunking is needed", styles["H2Custom"]))
    story.append(bullet_list(styles, ["LLMs have context limits.", "Long transcripts can exceed those limits.", "Overlap prevents losing context at chunk boundaries."]))
    story.append(Paragraph("If asked why embeddings are needed", styles["H2Custom"]))
    story.append(bullet_list(styles, ["They avoid comparing every requirement to every solution.", "They retrieve semantically related evidence.", "They reduce cost, latency, and irrelevant context."]))
    story.append(Paragraph("If asked what is open source", styles["H2Custom"]))
    story.append(bullet_list(styles, ["Qwen3-32B is used locally through Ollama.", "BAAI/bge-m3 is used through sentence-transformers.", "The cosine vector index is implemented locally, so FAISS is optional."]))
    return story


def strengths_commands_and_close(styles):
    story = [Paragraph("7. Strengths, Tradeoffs, and Future Work", styles["H1Custom"])]
    data = [
        ["Strength", "Tradeoff", "Future improvement"],
        ["Scales beyond one context window", "More chunks means more model calls", "Batching and async processing"],
        ["Focused evidence is explainable", "Retrieval can miss weak matches", "Hybrid keyword + vector retrieval"],
        ["Structured schemas are testable", "LLM JSON can need validation", "Retry and repair loop"],
        ["Local open-source stack", "Qwen 32B needs strong hardware", "Model profiles: 8B, 14B, 32B"],
        ["Modular design", "No graph reasoning yet", "GNN or knowledge graph as future work"],
    ]
    story.append(styled_table(data, [2.05 * inch, 2.15 * inch, 2.25 * inch], header_fill=LIGHT_BLUE, font_size=7.7))
    story.append(Spacer(1, 8))
    story.append(Paragraph("8. Commands to Run", styles["H1Custom"]))
    commands = [
        ("Install dependencies", "pip install -r requirements.txt"),
        ("Pull Qwen model", "ollama pull qwen3:32b"),
        ("Run large Qwen mode", "python main.py --mode large --config configs/qwen_local.yaml --business transcripts/business --engineering transcripts/engineering --output reports/large_qwen_report.md --format markdown"),
        ("Run tests", "python -m pytest -q"),
    ]
    data = [["Action", "Terminal command"], *commands]
    story.append(styled_table(data, [1.45 * inch, 5.0 * inch], header_fill=LIGHT_GRAY, font_size=7.0, code_second_col=True))
    story.append(Spacer(1, 8))
    story.append(
        callout(
            styles,
            "Final closing line",
            "The key design decision is retrieval before reasoning: embeddings narrow the evidence, and Qwen reasons over focused pairs instead of the entire transcript corpus.",
        )
    )
    return story


def bullet_list(styles, items):
    return ListFlowable(
        [ListItem(Paragraph(item, styles["BodyCustom"]), leftIndent=12) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=16,
        bulletFontSize=6,
    )


def callout(styles, title, body):
    data = [[Paragraph(f"<b>{title}</b><br/>{body}", styles["BodyCustom"])]]
    table = Table(data, colWidths=[6.45 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F6F9")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8E0EA")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def styled_table(data, col_widths, header_fill, font_size=8.0, code_second_col=False):
    converted = []
    for row_index, row in enumerate(data):
        converted_row = []
        for col_index, value in enumerate(row):
            font = "Courier" if code_second_col and col_index == 1 and row_index > 0 else "Helvetica"
            style = ParagraphStyle(
                name=f"cell-{row_index}-{col_index}",
                fontName=font,
                fontSize=font_size,
                leading=font_size + 2,
                textColor=INK,
                alignment=TA_LEFT,
            )
            if row_index == 0:
                style.fontName = "Helvetica-Bold"
            converted_row.append(Paragraph(str(value), style))
        converted.append(converted_row)
    table = Table(converted, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), header_fill),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C8D0DA")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawCentredString(letter[0] / 2, 0.33 * inch, f"Requirements Gap Analysis Agent - Interview Guide | Page {doc.page}")
    canvas.restoreState()


if __name__ == "__main__":
    main()

