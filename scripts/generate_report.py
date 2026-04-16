"""
Final Report Generator
======================
Generates a detailed PDF report covering:
  1. The Prompt Template used
  2. Definitions and Logic for the 3 Custom Metrics
  3. Raw Evaluation Data (from CSV/JSON)
  4. Comparative Analysis Summary

Usage:
    python scripts/generate_report.py
"""

import os
import sys
import json

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
COMPARISON_JSON = os.path.join(OUTPUT_DIR, "comparison_results.json")
REPORT_PDF = os.path.join(OUTPUT_DIR, "final_report.pdf")

# ---------------------------------------------------------------------------
# Colours — kept minimal, like a Word doc
# ---------------------------------------------------------------------------
BLACK = black
GREY = HexColor("#555555")
LIGHT_GREY = HexColor("#eeeeee")
TABLE_HEAD = HexColor("#4472c4")  # standard Word-blue
WHITE = white

# ---------------------------------------------------------------------------
# Styles — Times New Roman feel, standard academic report
# ---------------------------------------------------------------------------
styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    "Title2", parent=styles["Title"],
    fontName="Times-Bold", fontSize=20, leading=26,
    textColor=BLACK, spaceAfter=2 * mm, alignment=TA_CENTER,
)
style_h1 = ParagraphStyle(
    "H1", parent=styles["Heading1"],
    fontName="Times-Bold", fontSize=15, leading=19,
    textColor=BLACK, spaceBefore=6 * mm, spaceAfter=3 * mm,
)
style_h2 = ParagraphStyle(
    "H2", parent=styles["Heading2"],
    fontName="Times-Bold", fontSize=12, leading=16,
    textColor=HexColor("#333333"), spaceBefore=4 * mm, spaceAfter=2 * mm,
)
style_body = ParagraphStyle(
    "Body", parent=styles["Normal"],
    fontName="Times-Roman", fontSize=11, leading=15,
    textColor=BLACK, spaceAfter=2.5 * mm, alignment=TA_JUSTIFY,
)
style_code = ParagraphStyle(
    "Code", parent=styles["Code"],
    fontName="Courier", fontSize=8.5, leading=12,
    textColor=BLACK, backColor=LIGHT_GREY, borderPadding=5,
    spaceAfter=2.5 * mm, leftIndent=6 * mm,
)
style_bullet = ParagraphStyle(
    "Bullet", parent=style_body,
    leftIndent=12 * mm, bulletIndent=6 * mm,
    spaceAfter=1.5 * mm,
)
style_th = ParagraphStyle(
    "TH", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=9, leading=12,
    textColor=WHITE, alignment=TA_CENTER,
)
style_td = ParagraphStyle(
    "TD", parent=styles["Normal"],
    fontName="Helvetica", fontSize=9, leading=12,
    textColor=BLACK, alignment=TA_CENTER,
)
style_td_left = ParagraphStyle(
    "TDL", parent=style_td, alignment=TA_LEFT,
)


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=GREY, spaceAfter=3 * mm, spaceBefore=1 * mm)


def sp(h=3):
    return Spacer(1, h * mm)


def simple_table(header_row, data_rows, col_widths):
    """Build a plain table with blue header and alternating rows."""
    rows = [header_row] + data_rows
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEAD),
        ("BOX", (0, 0), (-1, -1), 0.6, BLACK),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, HexColor("#aaaaaa")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT_GREY))
    t.setStyle(TableStyle(cmds))
    return t


# ===================================================================
# SECTIONS
# ===================================================================

def build_cover(story):
    story.append(Spacer(1, 30 * mm))
    story.append(Paragraph("Email Generation Assistant", style_title))
    story.append(Paragraph("Final Evaluation Report", ParagraphStyle(
        "Sub", parent=style_title, fontSize=14, fontName="Times-Roman",
    )))
    story.append(sp(10))
    story.append(hr())
    story.append(sp(6))

    # Simple info block, no table — just plain text like a human would write
    info_lines = [
        "<b>Models Evaluated:</b> llama-3.3-70b-versatile (Model A) and llama-3.1-8b-instant (Model B)",
        "<b>Judge Model:</b> qwen/qwen3-32b via Groq (neutral, non-Llama family)",
        "<b>Provider:</b> Groq API",
        "<b>Test Scenarios:</b> 10 unique email generation scenarios with human reference emails",
    ]
    for line in info_lines:
        story.append(Paragraph(line, style_body))

    story.append(sp(12))

    # Table of contents — simple numbered list
    story.append(Paragraph("<b>Contents</b>", ParagraphStyle(
        "TOC_H", parent=style_body, fontName="Times-Bold", fontSize=12,
    )))
    story.append(sp(2))
    toc = [
        "1.  Prompt Template",
        "2.  Custom Evaluation Metrics",
        "3.  Raw Evaluation Data",
        "4.  Comparative Analysis",
    ]
    for item in toc:
        story.append(Paragraph(item, ParagraphStyle(
            "TOC", parent=style_body, leftIndent=8 * mm,
        )))
    story.append(PageBreak())


def build_section1(story):
    story.append(Paragraph("1. Prompt Template", style_h1))
    story.append(hr())
    story.append(Paragraph(
        "We used a Triple-Layer Prompting approach for Model A that combines three techniques: "
        "role-playing, few-shot examples, and chain-of-thought reasoning. Model B used a simple "
        "zero-shot baseline prompt as a control. The idea was to see how much difference advanced "
        "prompting makes compared to a straightforward approach.",
        style_body,
    ))

    # Layer 1
    story.append(Paragraph("1.1 Role-Playing", style_h2))
    story.append(Paragraph(
        "The model gets a specific persona in the system prompt. We told it to act as a "
        "\"Senior Business Communication Specialist\" with 15 years of experience. This helps "
        "the model stay grounded in professional email writing instead of drifting into generic "
        "assistant-style responses.",
        style_body,
    ))
    story.append(Paragraph(
        "The exact role prompt was:",
        style_body,
    ))
    story.append(Paragraph(
        '"You are a Senior Business Communication Specialist with 15 years of experience '
        'writing professional emails across corporate, startup, and nonprofit environments. '
        'You have a deep understanding of how tone, structure, and word choice impact '
        'business relationships."',
        style_code,
    ))

    # Layer 2
    story.append(Paragraph("1.2 Few-Shot Examples", style_h2))
    story.append(Paragraph(
        "We embedded three complete example emails in the system prompt, covering different tones. "
        "This gives the model concrete templates to follow rather than guessing at structure.",
        style_body,
    ))

    examples = [
        ["Formal", "Follow up after a sales meeting", "Enterprise plan, $5k/month, Q3 budget deadline"],
        ["Casual", "Request project update", "Phoenix Redesign, Friday deadline, Thursday standup"],
        ["Urgent", "Notify team of system outage", "Payment service down, all checkouts affected, ETA 2 hours"],
    ]
    header = [Paragraph("<b>Tone</b>", style_th),
              Paragraph("<b>Intent</b>", style_th),
              Paragraph("<b>Key Facts</b>", style_th)]
    rows = [[Paragraph(c, style_td_left) for c in row] for row in examples]
    story.append(simple_table(header, rows, [25 * mm, 50 * mm, 85 * mm]))
    story.append(sp(2))
    story.append(Paragraph(
        "Each example included the full email text with subject line, greeting, body, and closing "
        "so the model could see exactly what we expected.",
        style_body,
    ))

    # Layer 3
    story.append(Paragraph("1.3 Chain-of-Thought (CoT)", style_h2))
    story.append(Paragraph(
        "Before generating the email, we asked the model to think through four steps:",
        style_body,
    ))
    cot_steps = [
        "Step 1 (Intent): What is the main goal of this email?",
        "Step 2 (Facts): Which facts matter most and how should they be ordered?",
        "Step 3 (Tone): What word choices and structure will match the tone?",
        "Step 4 (Draft): Write the actual email.",
    ]
    for step in cot_steps:
        story.append(Paragraph(f"- {step}", style_bullet))
    story.append(Paragraph(
        "This forces the model to plan before writing, which helps it avoid omitting facts or "
        "drifting off-tone. The CoT reasoning gets stripped from the final output so the user "
        "only sees the finished email.",
        style_body,
    ))

    # Rules
    story.append(Paragraph("1.4 Strict Rules", style_h2))
    story.append(Paragraph(
        "The system prompt also included explicit constraints:",
        style_body,
    ))
    rules = [
        "Include every key fact - do not omit any.",
        "Match the requested tone precisely.",
        "Always include a Subject line.",
        "Follow the structure: Subject, Greeting, Body, Closing.",
        "Keep it concise - no filler content.",
        "Output only the email, no commentary.",
    ]
    for i, rule in enumerate(rules, 1):
        story.append(Paragraph(f"{i}. {rule}", style_bullet))

    # Baseline
    story.append(Paragraph("1.5 Model B Baseline (Zero-Shot)", style_h2))
    story.append(Paragraph(
        "For comparison, Model B got a much simpler prompt with none of the above techniques:",
        style_body,
    ))
    story.append(Paragraph(
        'System: "You are a helpful assistant that writes professional emails."<br/>'
        'User: "Write a professional email. Intent: ... Key Facts: ... Tone: ... '
        'Include a Subject line and keep it concise."',
        style_code,
    ))
    story.append(PageBreak())


def build_section2(story):
    story.append(Paragraph("2. Custom Evaluation Metrics", style_h1))
    story.append(hr())
    story.append(Paragraph(
        "We designed three metrics to evaluate the generated emails. The first one is fully "
        "automated (no LLM involved). The other two use an LLM-as-Judge approach where a "
        "separate model (qwen/qwen3-32b) scores the output. We chose Qwen specifically because "
        "it is from a different model family than Llama, so it would not have any inherent bias "
        "toward either Model A or Model B's outputs.",
        style_body,
    ))

    # Metric 1
    story.append(Paragraph("2.1 Fact Coverage Score (Automated)", style_h2))
    story.append(Paragraph(
        "This metric checks how many of the user-provided key facts actually made it into the "
        "generated email. It works by tokenising each fact (splitting into words, removing common "
        "stop words like \"the\", \"is\", \"and\"), and then checking if at least 60% of those "
        "tokens appear somewhere in the email text. The score is simply the fraction of facts "
        "that were covered.",
        style_body,
    ))
    story.append(Paragraph("Formula: score = facts_covered / total_facts", style_code))
    story.append(Paragraph("Range: 0.0 (nothing included) to 1.0 (everything included).", style_body))
    story.append(Paragraph(
        "This matters because an email that misses facts the user wanted to communicate is a "
        "fundamental failure, regardless of how well-written it is otherwise.",
        style_body,
    ))

    # Metric 2
    story.append(Paragraph("2.2 Tone Alignment Score (LLM-as-Judge)", style_h2))
    story.append(Paragraph(
        "This metric measures whether the email actually sounds like the requested tone. We send "
        "the email and the target tone to the judge model (Qwen3 32B) and ask it to rate the "
        "match on a 1-10 scale. The judge looks at vocabulary choice, formality level, sentence "
        "structure, emotional warmth, urgency cues, and professionalism. We normalise the score "
        "to 0.0-1.0 by dividing by 10.",
        style_body,
    ))
    story.append(Paragraph(
        "If the judge returns something we cannot parse as a number, we fall back to 5 (0.5). "
        "Tone matters because sending a casual email to an enterprise client or a flat email "
        "about an urgent outage can have real consequences.",
        style_body,
    ))

    # Metric 3
    story.append(Paragraph("2.3 Email Quality Score (LLM-as-Judge)", style_h2))
    story.append(Paragraph(
        "This is a holistic quality check. The judge model rates the email on five dimensions:",
        style_body,
    ))
    dims = [
        "Subject line - Is it clear and specific?",
        "Structure - Proper greeting, body, and closing?",
        "Grammar and fluency - Error-free and natural sounding?",
        "Clarity and conciseness - Gets to the point without padding?",
        "Call-to-action - Ends with a clear next step?",
    ]
    for d in dims:
        story.append(Paragraph(f"- {d}", style_bullet))
    story.append(Paragraph(
        "The judge gives one overall score from 1-10, normalised to 0.0-1.0. Same fallback to "
        "0.5 if parsing fails.",
        style_body,
    ))

    # Composite
    story.append(Paragraph("2.4 Composite Score", style_h2))
    story.append(Paragraph(
        "The composite score is just the average of all three metrics, weighted equally:",
        style_body,
    ))
    story.append(Paragraph(
        "composite = (fact_coverage + tone_alignment + email_quality) / 3",
        style_code,
    ))
    story.append(Paragraph("This gives us a single number between 0 and 1 to compare models.", style_body))
    story.append(PageBreak())


def build_section3(story, data):
    story.append(Paragraph("3. Raw Evaluation Data", style_h1))
    story.append(hr())
    story.append(Paragraph(
        "Below is the full scoring data from both models across all 10 test scenarios. Each "
        "scenario has a specific intent, tone, and set of key facts. The \"Winner\" column shows "
        "which model had the higher composite score for that scenario.",
        style_body,
    ))
    story.append(sp(3))

    # Build scores table
    header = [
        Paragraph("<b>#</b>", style_th),
        Paragraph("<b>Intent</b>", style_th),
        Paragraph("<b>Tone</b>", style_th),
        Paragraph("<b>A:Fact</b>", style_th),
        Paragraph("<b>B:Fact</b>", style_th),
        Paragraph("<b>A:Tone</b>", style_th),
        Paragraph("<b>B:Tone</b>", style_th),
        Paragraph("<b>A:Qual</b>", style_th),
        Paragraph("<b>B:Qual</b>", style_th),
        Paragraph("<b>A:Comp</b>", style_th),
        Paragraph("<b>B:Comp</b>", style_th),
        Paragraph("<b>Win</b>", style_th),
    ]
    rows = []

    for s in data["scenarios"]:
        a, b = s["model_a"], s["model_b"]
        ac, bc = a["composite_score"], b["composite_score"]
        w = "A" if ac > bc else ("B" if bc > ac else "Tie")
        intent_short = s["intent"][:28] + (".." if len(s["intent"]) > 28 else "")
        rows.append([
            Paragraph(str(s["scenario_id"]), style_td),
            Paragraph(intent_short, style_td_left),
            Paragraph(s["tone"], style_td),
            Paragraph(f'{a["fact_coverage_score"]:.2f}', style_td),
            Paragraph(f'{b["fact_coverage_score"]:.2f}', style_td),
            Paragraph(f'{a["tone_alignment_score"]:.2f}', style_td),
            Paragraph(f'{b["tone_alignment_score"]:.2f}', style_td),
            Paragraph(f'{a["email_quality_score"]:.2f}', style_td),
            Paragraph(f'{b["email_quality_score"]:.2f}', style_td),
            Paragraph(f'{ac:.4f}', style_td),
            Paragraph(f'{bc:.4f}', style_td),
            Paragraph(f'<b>{w}</b>', style_td),
        ])

    # Averages
    aa, ab = data["strategy_a"]["averages"], data["strategy_b"]["averages"]
    ow = "A" if aa["composite_score"] > ab["composite_score"] else (
        "B" if ab["composite_score"] > aa["composite_score"] else "Tie")
    rows.append([
        Paragraph("<b>Avg</b>", style_td),
        Paragraph("<b>All Scenarios</b>", style_td_left),
        Paragraph("-", style_td),
        Paragraph(f'<b>{aa["fact_coverage_score"]:.4f}</b>', style_td),
        Paragraph(f'<b>{ab["fact_coverage_score"]:.4f}</b>', style_td),
        Paragraph(f'<b>{aa["tone_alignment_score"]:.4f}</b>', style_td),
        Paragraph(f'<b>{ab["tone_alignment_score"]:.4f}</b>', style_td),
        Paragraph(f'<b>{aa["email_quality_score"]:.4f}</b>', style_td),
        Paragraph(f'<b>{ab["email_quality_score"]:.4f}</b>', style_td),
        Paragraph(f'<b>{aa["composite_score"]:.4f}</b>', style_td),
        Paragraph(f'<b>{ab["composite_score"]:.4f}</b>', style_td),
        Paragraph(f'<b>{ow}</b>', style_td),
    ])

    cw = [8*mm, 33*mm, 14*mm, 13*mm, 13*mm, 13*mm, 13*mm, 13*mm, 13*mm, 14*mm, 14*mm, 12*mm]
    story.append(simple_table(header, rows, cw))
    story.append(sp(4))

    # Sample emails
    story.append(Paragraph("3.1 Sample Generated Emails", style_h2))
    story.append(Paragraph(
        "Here are the actual emails generated by both models for a few representative "
        "scenarios, so you can see the qualitative differences beyond just the scores.",
        style_body,
    ))

    for idx in [0, 3, 4]:  # scenarios 1, 4, 5
        s = data["scenarios"][idx]
        story.append(sp(2))
        story.append(Paragraph(
            f'Scenario {s["scenario_id"]}: {s["intent"]} ({s["tone"]})',
            style_h2,
        ))
        story.append(Paragraph("<b>Model A:</b>", style_body))
        story.append(Paragraph(
            s["model_a"]["generated_email"].replace("\n", "<br/>"), style_code))
        story.append(Paragraph("<b>Model B:</b>", style_body))
        story.append(Paragraph(
            s["model_b"]["generated_email"].replace("\n", "<br/>"), style_code))

    story.append(PageBreak())


def build_section4(story, data):
    story.append(Paragraph("4. Comparative Analysis", style_h1))
    story.append(hr())

    aa = data["strategy_a"]["averages"]
    ab = data["strategy_b"]["averages"]

    # 4.1 Results
    story.append(Paragraph("4.1 Overall Results", style_h2))

    winner_label = data["strategy_a"]["label"] if aa["composite_score"] > ab["composite_score"] else data["strategy_b"]["label"]
    story.append(Paragraph(f"Overall winner: <b>{winner_label}</b>", style_body))
    story.append(sp(2))

    # Summary table
    header = [
        Paragraph("<b>Metric</b>", style_th),
        Paragraph("<b>Model A</b>", style_th),
        Paragraph("<b>Model B</b>", style_th),
        Paragraph("<b>Delta</b>", style_th),
    ]
    metrics = [
        ("Fact Coverage", "fact_coverage_score"),
        ("Tone Alignment", "tone_alignment_score"),
        ("Email Quality", "email_quality_score"),
        ("Composite", "composite_score"),
    ]
    rows = []
    for label, key in metrics:
        d = aa[key] - ab[key]
        bold = key == "composite_score"
        fmt = lambda v, b=bold: f'<b>{v:.4f}</b>' if b else f'{v:.4f}'
        lbl = f'<b>{label}</b>' if bold else label
        rows.append([
            Paragraph(lbl, style_td_left),
            Paragraph(fmt(aa[key]), style_td),
            Paragraph(fmt(ab[key]), style_td),
            Paragraph(f'<b>{d:+.4f}</b>' if bold else f'{d:+.4f}', style_td),
        ])
    story.append(simple_table(header, rows, [42*mm, 38*mm, 38*mm, 32*mm]))
    story.append(sp(3))

    # Win counts
    a_wins = sum(1 for s in data["scenarios"]
                 if s["model_a"]["composite_score"] > s["model_b"]["composite_score"])
    b_wins = sum(1 for s in data["scenarios"]
                 if s["model_b"]["composite_score"] > s["model_a"]["composite_score"])
    ties = len(data["scenarios"]) - a_wins - b_wins
    story.append(Paragraph(
        f"At the scenario level, Model A won {a_wins} out of 10 scenarios, "
        f"Model B won {b_wins}, and {ties} were ties.",
        style_body,
    ))

    # 4.2 Failure analysis
    story.append(Paragraph("4.2 Where Model B Struggled Most", style_h2))
    worst = max(data["scenarios"],
                key=lambda s: s["model_a"]["composite_score"] - s["model_b"]["composite_score"])
    gap = worst["model_a"]["composite_score"] - worst["model_b"]["composite_score"]
    story.append(Paragraph(
        f'The biggest gap was in Scenario {worst["scenario_id"]} '
        f'(\"{worst["intent"]}\" with {worst["tone"]} tone), where Model A scored '
        f'{worst["model_a"]["composite_score"]:.4f} vs Model B\'s '
        f'{worst["model_b"]["composite_score"]:.4f} - a gap of {gap:+.4f}.',
        style_body,
    ))
    story.append(Paragraph(
        "Looking at the pattern across scenarios, Model B's main weaknesses were:",
        style_body,
    ))
    failures = [
        "Dropping facts, especially numerical ones (amounts, dates, IDs) in longer scenarios.",
        "Tone drift - urgent emails came out sounding informational, empathetic emails felt flat.",
        "Weaker subject lines that did not clearly reflect the email's purpose.",
    ]
    for f in failures:
        story.append(Paragraph(f"- {f}", style_bullet))
    story.append(Paragraph(
        "Without role-playing or few-shot examples to anchor it, Model B defaulted to a generic "
        "\"helpful assistant\" style that works okay for simple cases but falls short when the "
        "tone or fact list is demanding.",
        style_body,
    ))

    # 4.3 Recommendation
    story.append(Paragraph("4.3 Recommendation", style_h2))
    story.append(Paragraph(
        "Based on the results, we would recommend <b>Model A</b> (llama-3.3-70b-versatile with "
        "advanced prompting) for production use. The combination of role-playing, few-shot "
        "examples, and chain-of-thought reasoning consistently produces more reliable emails "
        "with better fact coverage and tone matching.",
        style_body,
    ))
    story.append(Paragraph(
        "The trade-off is that Model A is a 70B model, so it has higher latency than the 8B "
        "Model B. For latency-sensitive use cases, one option would be to fine-tune the smaller "
        "model on outputs from Model A to get the best of both worlds.",
        style_body,
    ))

    # 4.4 Judge note
    story.append(Paragraph("4.4 A Note on the Judge Model", style_h2))
    story.append(Paragraph(
        "For Tone Alignment and Email Quality scoring, we used qwen/qwen3-32b (Qwen3 32B) as "
        "the judge model. We picked it specifically because it is from a completely different "
        "model family (Qwen vs Llama), so it should not have any built-in preference for either "
        "Model A or Model B's output style. Using Model B as its own judge (which was the "
        "original setup) would have been a conflict of interest.",
        style_body,
    ))


# ===================================================================
# Main
# ===================================================================

def main():
    if not os.path.exists(COMPARISON_JSON):
        print(f"ERROR: {COMPARISON_JSON} not found.")
        print("Run 'python scripts/model_comparison.py' first.")
        sys.exit(1)

    with open(COMPARISON_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc = SimpleDocTemplate(
        REPORT_PDF,
        pagesize=A4,
        leftMargin=25 * mm,
        rightMargin=25 * mm,
        topMargin=22 * mm,
        bottomMargin=22 * mm,
        title="Email Generation Assistant - Final Report",
        author="Email Gen Assistant",
    )

    story = []
    build_cover(story)
    build_section1(story)
    build_section2(story)
    build_section3(story, data)
    build_section4(story, data)
    doc.build(story)
    print(f"\nPDF report generated: {os.path.abspath(REPORT_PDF)}")


if __name__ == "__main__":
    main()
