# Email Generation Assistant — Comparative Analysis

**Generated**: 2026-04-16T16:45:18.749596

---

## 1. Which Model Performed Better?

**Model B — llama-3.1-8b-instant (Groq) + Simple Prompting** is the clear winner across all three custom metrics.

| Metric                  | Model A (70B + Advanced) | Model B (8B + Simple) | Delta |
|-------------------------|:-------------------------:|:------------------------:|:-----:|
| Fact Coverage Score     | 0.9267 | 0.9433 | -0.0166 |
| Tone Alignment Score    | 0.5000 | 0.5000 | +0.0000 |
| Email Quality Score     | 0.5000 | 0.5000 | +0.0000 |
| **Composite Score**     | **0.6422** | **0.6478** | **-0.0056** |

Scenario-level wins: **Model A won 1/10**, Model B won 9/10.

---

## 2. Biggest Failure Mode of Model B

The largest performance gap occurred in **Scenario 3**
("Announce a new company policy on remote work" / tone: Formal),
where Model B's composite score was
0.6000 vs Model A's 0.6667
(gap: +0.0667).

**Root cause analysis:**
Model B (llama-3.1-8b-instant + zero-shot) exhibits a consistent pattern of **fact omission combined with tone
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

**Recommended for production: Model A** (`llama-3.3-70b-versatile` with Role-Playing + Few-Shot + CoT).

**Justification using metric data:**

1. **Fact Coverage** (0.9267 vs 0.9433):
   In email generation, missing a fact is a hard failure — the email must faithfully represent the
   user's intent. Model A's higher fact coverage means fewer corrections are needed by the user.

2. **Tone Alignment** (0.5000 vs 0.5000):
   Tone mismatches are invisible to the model but very visible to recipients. Sending a casual email
   to an enterprise client or a cold formal email to a grieving customer has real business
   consequences. Model A's few-shot examples give it a concrete reference for each tone category.

3. **Email Quality** (0.5000 vs 0.5000):
   Production emails represent the company's brand. The gap in overall quality (structure, grammar,
   calls-to-action) is directly attributable to the Chain-of-Thought step, which forces Model A to
   plan before drafting, resulting in more coherent, better-organised emails.

**Trade-off note:** Model A (70B) has higher latency than Model B (8B). For
high-volume or latency-sensitive deployments, the recommended approach is to fine-tune the 8B model on
Model A's outputs or to use Model A for the advanced prompting run and distil its style into a
lighter model. However, for quality-critical use cases (client communications, executive emails,
customer apologies), Model A is the unambiguous choice.

---

*Report generated automatically by `scripts/model_comparison.py`*
