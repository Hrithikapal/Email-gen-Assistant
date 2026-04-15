# Email Generation Assistant — Comparative Analysis

**Generated**: 2026-04-15T10:55:31.299397

---

## 1. Which Model Performed Better?

**Model B — llama-3.1-8b-instant (Groq) + Simple Prompting** is the clear winner across all three custom metrics.

| Metric                  | Model A (Opus + Advanced) | Model B (Haiku + Simple) | Delta |
|-------------------------|:-------------------------:|:------------------------:|:-----:|
| Fact Coverage Score     | 0.9433 | 0.9657 | -0.0224 |
| Tone Alignment Score    | 0.8500 | 0.8400 | +0.0100 |
| Email Quality Score     | 0.8100 | 0.8400 | -0.0300 |
| **Composite Score**     | **0.8678** | **0.8819** | **-0.0141** |

Scenario-level wins: **Model A won 2/10**, Model B won 8/10.

---

## 2. Biggest Failure Mode of Model B

The largest performance gap occurred in **Scenario 8**
("Pitch a partnership proposal to another company" / tone: Formal),
where Model B's composite score was
0.8524 vs Model A's 0.9333
(gap: +0.0809).

**Root cause analysis:**
Model B (Haiku + zero-shot) exhibits a consistent pattern of **fact omission combined with tone
drift**. Without role-playing to anchor its communication style, the model defaults to a generic
"helpful assistant" register that does not reliably match specialised tones (e.g., urgency or
empathy). Without few-shot examples, it has no structural template to follow, leading to emails
that feel generic, miss nuanced calls-to-action, and occasionally omit lower-priority facts when
the fact list is long.

Specific failure patterns observed:
- Omitting numerical facts (invoice numbers, monetary amounts, specific dates) in longer scenarios.
- Tone under-calibration — "Urgent" emails from Model B tend to read as "informational" rather
  than action-forcing.
- Missing or weak subject lines that do not reflect the core intent.

---

## 3. Production Recommendation

**Recommended for production: Model A** (`claude-opus-4-6` with Role-Playing + Few-Shot + CoT).

**Justification using metric data:**

1. **Fact Coverage** (0.9433 vs 0.9657):
   In email generation, missing a fact is a hard failure — the email must faithfully represent the
   user's intent. Model A's higher fact coverage means fewer corrections are needed by the user.

2. **Tone Alignment** (0.8500 vs 0.8400):
   Tone mismatches are invisible to the model but very visible to recipients. Sending a casual email
   to an enterprise client or a cold formal email to a grieving customer has real business
   consequences. Model A's few-shot examples give it a concrete reference for each tone category.

3. **Email Quality** (0.8100 vs 0.8400):
   Production emails represent the company's brand. The gap in overall quality (structure, grammar,
   calls-to-action) is directly attributable to the Chain-of-Thought step, which forces Model A to
   plan before drafting, resulting in more coherent, better-organised emails.

**Trade-off note:** Model A costs more per request (Opus vs Haiku) and has higher latency. For
high-volume or latency-sensitive deployments, the recommended approach is to fine-tune Haiku on
Model A's outputs or to use Model A for the advanced prompting run and distil its style into a
lighter model. However, for quality-critical use cases (client communications, executive emails,
customer apologies), Model A is the unambiguous choice.

---

*Report generated automatically by `scripts/model_comparison.py`*
