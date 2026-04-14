"""
Email Generation Assistant — Core Generator
============================================
Advanced Prompting Technique: Triple-Layer Prompting
  1. Role-Playing  — Claude acts as a Senior Business Communication Specialist
  2. Few-Shot       — Three annotated example emails embedded in the system prompt
  3. Chain-of-Thought (CoT) — Claude reasons through intent→facts→tone before writing
"""

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

# ---------------------------------------------------------------------------
# Few-shot examples embedded in the system prompt
# ---------------------------------------------------------------------------
FEW_SHOT_EXAMPLES = """
=== EXAMPLE 1 ===
Intent: Follow up after a sales meeting
Key Facts:
  - Met on Tuesday at 2pm
  - Discussed the Enterprise plan ($5,000/month)
  - Client mentioned budget approval needed by end of Q3
  - Agreed to send a detailed proposal
Tone: Formal

Subject: Follow-Up: Enterprise Plan Proposal — [Your Company]

Dear [Client Name],

Thank you for taking the time to meet with me on Tuesday afternoon. I greatly enjoyed our conversation and learning more about [Client Company]'s goals.

As discussed, I am pleased to attach our detailed proposal for the Enterprise Plan at $5,000 per month. Given your mention of a Q3 budget approval timeline, I wanted to ensure you have all the information needed to move forward with confidence.

I would be happy to address any questions or arrange a follow-up call at your convenience. Please do not hesitate to reach out.

Best regards,
[Your Name]

=== EXAMPLE 2 ===
Intent: Request for project update from a colleague
Key Facts:
  - Project name: "Phoenix Redesign"
  - Deadline: Friday
  - Need design mockups and dev status
  - Team standup is Thursday at 10am
Tone: Casual

Subject: Quick Update on Phoenix Redesign?

Hey [Colleague],

Hope your week is going well! Just wanted to check in on the Phoenix Redesign before our Thursday standup at 10am.

Could you share where things stand with the design mockups and dev progress? Knowing the status ahead of Friday's deadline would really help us plan the session.

Thanks so much — let me know if you need anything from my end!

Cheers,
[Your Name]

=== EXAMPLE 3 ===
Intent: Notify team of a critical system outage
Key Facts:
  - Payment service is down since 3:15 PM
  - Affects all checkout flows
  - Engineering team is investigating
  - ETA for fix: 2 hours
  - Customers should use manual invoicing as workaround
Tone: Urgent

Subject: URGENT: Payment Service Outage — Action Required

Team,

Please be advised that our payment service has been down since 3:15 PM today, affecting all checkout flows across the platform.

Our engineering team is actively investigating the root cause and we estimate a resolution within 2 hours. In the meantime, please direct affected customers to use manual invoicing as a temporary workaround.

We will provide updates every 30 minutes. Your prompt attention to this matter is critical.

Thank you,
[Your Name]
"""

# ---------------------------------------------------------------------------
# System prompt (Role-Playing + Few-Shot injected)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = f"""You are a Senior Business Communication Specialist with 15 years of experience writing professional emails across corporate, startup, and nonprofit environments. You have a deep understanding of how tone, structure, and word choice impact business relationships.

Your task is to generate a single, polished professional email given:
  • Intent — the core purpose of the email
  • Key Facts — specific information that MUST appear in the email
  • Tone — the desired communication style

Here are three high-quality reference emails to guide your output:

{FEW_SHOT_EXAMPLES}

---

STRICT RULES:
1. You MUST include every key fact provided. Do not omit any.
2. Match the requested tone precisely. "Formal" means no contractions; "Casual" allows friendly language; "Urgent" uses direct, action-oriented language.
3. Always include a clear Subject line.
4. Structure: Subject → Greeting → Body (facts woven in naturally) → Closing.
5. Keep the email concise but complete — no padding, no fluff.
6. Output ONLY the final email. Do not include commentary or meta-text.
"""

# ---------------------------------------------------------------------------
# CoT wrapper — injected as user message prefix
# ---------------------------------------------------------------------------
COT_PREFIX = """Before writing the email, briefly think through:
  [STEP 1 — Intent]: What is the single most important goal of this email?
  [STEP 2 — Facts]:  Which facts are highest priority and how should they be sequenced?
  [STEP 3 — Tone]:   What specific word choices and structural decisions will nail the requested tone?
  [STEP 4 — Draft]:  Now write the complete email.

---

"""


def generate_email(
    intent: str,
    key_facts: list[str],
    tone: str,
    model: str = "claude-opus-4-6",
    use_advanced_prompting: bool = True,
) -> dict:
    """
    Generate a professional email using the Anthropic Claude API.

    Args:
        intent:                 Core purpose of the email.
        key_facts:              List of bullet-point facts to include.
        tone:                   Desired tone (e.g. "formal", "casual", "urgent").
        model:                  Claude model ID.
        use_advanced_prompting: If True, uses Role-Playing + Few-Shot + CoT.
                                If False, uses a simple baseline prompt.

    Returns:
        dict with keys: "email_text", "model", "input_tokens", "output_tokens"
    """
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    facts_formatted = "\n".join(f"  - {f}" for f in key_facts)

    if use_advanced_prompting:
        system = SYSTEM_PROMPT
        user_content = (
            COT_PREFIX
            + f"Intent: {intent}\n\n"
            + f"Key Facts:\n{facts_formatted}\n\n"
            + f"Tone: {tone}"
        )
    else:
        # Baseline: simple zero-shot prompt, no persona, no examples
        system = "You are a helpful assistant that writes professional emails."
        user_content = (
            f"Write a professional email.\n\n"
            f"Intent: {intent}\n\n"
            f"Key Facts:\n{facts_formatted}\n\n"
            f"Tone: {tone}\n\n"
            f"Include a Subject line and keep it concise."
        )

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": user_content}],
    )

    email_text = response.content[0].text

    # Strip CoT reasoning — keep only the email (after the last "---" separator)
    if use_advanced_prompting and "---" in email_text:
        parts = email_text.split("---")
        # The last non-empty segment is the actual email
        email_text = parts[-1].strip()

    return {
        "email_text": email_text,
        "model": model,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }


# ---------------------------------------------------------------------------
# Quick demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    result = generate_email(
        intent="Request a project deadline extension",
        key_facts=[
            "Original deadline is November 15th",
            "Need 2 extra weeks due to unexpected API integration issues",
            "Current progress is 70% complete",
            "Team has resolved the blocker as of today",
        ],
        tone="Formal",
    )
    print("=" * 60)
    print(f"Model: {result['model']}")
    print(f"Tokens — Input: {result['input_tokens']}  Output: {result['output_tokens']}")
    print("=" * 60)
    print(result["email_text"])
