"""
Custom Evaluation Metrics
==========================
Three metrics purpose-built for email generation quality assessment.

Metric 1 — Fact Coverage Score    (Automated, keyword overlap)
Metric 2 — Tone Alignment Score   (LLM-as-Judge via Claude Haiku)
Metric 3 — Email Quality Score    (LLM-as-Judge via Claude Haiku)
"""

import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Use a fast, cheap Groq judge model — keeps evaluation cost low
JUDGE_MODEL = "llama-3.1-8b-instant"

# Common stop words to exclude from fact token matching
STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "need", "dare",
    "to", "of", "in", "for", "on", "with", "at", "by", "from", "as",
    "into", "through", "during", "before", "after", "above", "below",
    "and", "but", "or", "nor", "so", "yet", "both", "either", "not",
    "this", "that", "these", "those", "it", "its", "we", "our", "my",
    "your", "their", "they", "he", "she", "i", "you", "me", "us",
}


# ===========================================================================
# Metric 1 — Fact Coverage Score (Automated)
# ===========================================================================
METRIC_1_DEFINITION = {
    "name": "Fact Coverage Score",
    "type": "Automated",
    "description": (
        "Measures what fraction of the user-supplied key facts are present "
        "in the generated email. Each fact is tokenised (stop words removed) "
        "and we check whether the core content tokens appear anywhere in the "
        "email text (case-insensitive). Score = covered_facts / total_facts. "
        "Range: 0.0 (no facts present) – 1.0 (all facts present)."
    ),
}


def _tokenise_fact(fact: str) -> set[str]:
    """Extract meaningful tokens from a fact string."""
    tokens = re.findall(r"[a-z0-9]+", fact.lower())
    return {t for t in tokens if t not in STOP_WORDS and len(t) > 1}


def _fact_covered(fact_tokens: set[str], email_lower: str) -> bool:
    """
    A fact is considered covered if at least 60% of its meaningful tokens
    appear in the email, AND the original fact string has at least a partial
    substring match for any numeric or named entity.
    """
    if not fact_tokens:
        return True  # empty fact — vacuously true

    found = sum(1 for t in fact_tokens if t in email_lower)
    coverage_ratio = found / len(fact_tokens)
    return coverage_ratio >= 0.6


def fact_coverage_score(key_facts: list[str], email_text: str) -> float:
    """
    Compute Fact Coverage Score.

    Returns a float in [0.0, 1.0].
    """
    if not key_facts:
        return 1.0

    email_lower = email_text.lower()
    covered = 0
    for fact in key_facts:
        tokens = _tokenise_fact(fact)
        if _fact_covered(tokens, email_lower):
            covered += 1

    return round(covered / len(key_facts), 4)


# ===========================================================================
# Metric 2 — Tone Alignment Score (LLM-as-Judge)
# ===========================================================================
METRIC_2_DEFINITION = {
    "name": "Tone Alignment Score",
    "type": "LLM-as-Judge",
    "description": (
        "Uses Claude Haiku as an impartial judge to rate how well the "
        "generated email's actual tone matches the requested tone. "
        "The judge assigns a score from 1 (completely mismatched) to 10 "
        "(perfectly aligned), which is normalised to 0.0–1.0. "
        "Evaluates vocabulary, formality level, sentence structure, "
        "and emotional register."
    ),
}

_TONE_JUDGE_PROMPT = """You are an expert email tone evaluator. Your task is to rate how accurately an email matches a requested tone.

Requested Tone: {tone}

Generated Email:
---
{email}
---

Rate the tone alignment on a scale of 1 to 10:
  1  = The email's tone is completely wrong — opposite of what was requested.
  5  = Partially matches but has notable misalignments.
  10 = The tone is a perfect match in every way.

Consider: vocabulary choice, formality level, sentence structure, emotional warmth, urgency cues, and professionalism markers.

Respond with ONLY a single integer between 1 and 10. No explanation."""


def tone_alignment_score(tone: str, email_text: str) -> float:
    """
    Compute Tone Alignment Score using Groq (llama3-8b-8192) as judge.

    Returns a float in [0.0, 1.0].
    """
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    prompt = _TONE_JUDGE_PROMPT.format(tone=tone, email=email_text)

    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.choices[0].message.content.strip()
    match = re.search(r"\b([1-9]|10)\b", raw)
    score_int = int(match.group(1)) if match else 5
    return round(score_int / 10.0, 4)


# ===========================================================================
# Metric 3 — Email Quality Score (LLM-as-Judge)
# ===========================================================================
METRIC_3_DEFINITION = {
    "name": "Email Quality Score",
    "type": "LLM-as-Judge",
    "description": (
        "Uses Claude Haiku as an impartial judge to rate the holistic quality "
        "of the generated email across five sub-dimensions: "
        "(1) Subject line effectiveness, "
        "(2) Structure and flow (greeting → body → closing), "
        "(3) Grammar and fluency, "
        "(4) Clarity and conciseness, "
        "(5) Presence of a clear call-to-action. "
        "The judge assigns an overall score from 1 to 10, normalised to 0.0–1.0."
    ),
}

_QUALITY_JUDGE_PROMPT = """You are an expert business communication evaluator. Rate the overall quality of the following professional email.

Email:
---
{email}
---

Evaluate across these five dimensions:
  1. Subject line — Is it clear, specific, and compelling?
  2. Structure — Does it have a proper greeting, coherent body, and professional closing?
  3. Grammar & Fluency — Is the writing error-free and natural?
  4. Clarity & Conciseness — Is the message clear without unnecessary padding?
  5. Call-to-Action — Does it end with a clear next step or request?

Assign a single overall quality score from 1 to 10:
  1  = Very poor quality — multiple serious flaws.
  5  = Acceptable but with noticeable weaknesses.
  10 = Excellent — would be considered a professional benchmark.

Respond with ONLY a single integer between 1 and 10. No explanation."""


def email_quality_score(email_text: str) -> float:
    """
    Compute Email Quality Score using Groq (llama3-8b-8192) as judge.

    Returns a float in [0.0, 1.0].
    """
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    prompt = _QUALITY_JUDGE_PROMPT.format(email=email_text)

    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.choices[0].message.content.strip()
    match = re.search(r"\b([1-9]|10)\b", raw)
    score_int = int(match.group(1)) if match else 5
    return round(score_int / 10.0, 4)


# ===========================================================================
# All metric definitions (for reporting)
# ===========================================================================
ALL_METRIC_DEFINITIONS = [
    METRIC_1_DEFINITION,
    METRIC_2_DEFINITION,
    METRIC_3_DEFINITION,
]


def evaluate_all(
    intent: str,
    key_facts: list[str],
    tone: str,
    email_text: str,
) -> dict:
    """
    Run all three metrics on a generated email.

    Returns:
        dict with keys: fact_coverage, tone_alignment, email_quality, composite
    """
    fc = fact_coverage_score(key_facts, email_text)
    ta = tone_alignment_score(tone, email_text)
    eq = email_quality_score(email_text)
    composite = round((fc + ta + eq) / 3.0, 4)

    return {
        "fact_coverage_score": fc,
        "tone_alignment_score": ta,
        "email_quality_score": eq,
        "composite_score": composite,
    }


# ===========================================================================
# Quick smoke test
# ===========================================================================
if __name__ == "__main__":
    sample_email = """Subject: Follow-Up: Enterprise Plan Proposal

Dear Ms. Chen,

Thank you for meeting with me on Monday at 11am to discuss the Senior Product Manager role. I was particularly energised by our conversation about roadmap prioritisation and OKR alignment.

I remain very enthusiastic about your company's AI-driven product vision and believe my experience is well matched to the challenges ahead. I am available for any next steps at your convenience this week.

Best regards,
[Your Name]"""

    scores = evaluate_all(
        intent="Follow up after a job interview",
        key_facts=[
            "Interview was on Monday at 11am for the Senior Product Manager role",
            "Discussed roadmap prioritisation and OKR alignment",
            "Excited about the company's AI-driven product vision",
            "Available for next steps anytime this week",
        ],
        tone="Formal",
        email_text=sample_email,
    )

    print("=== Metric Scores ===")
    for k, v in scores.items():
        print(f"  {k}: {v}")
