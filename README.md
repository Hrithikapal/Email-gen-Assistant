# Email Generation Assistant

An AI-powered email generation assistant built with the Groq API. This project demonstrates advanced prompt engineering techniques and a custom evaluation framework to measure email quality across two competing strategies.

## Project Structure

```
email-gen-assistant/
├── src/
│   ├── email_generator.py   # Core email generator with advanced prompting
│   ├── test_scenarios.py    # 10 test scenarios + human reference emails
│   ├── metrics.py           # 3 custom evaluation metrics (judge: qwen/qwen3-32b)
│   └── evaluator.py         # Evaluation runner & report generator (used by model_comparison.py)
├── scripts/
│   └── model_comparison.py  # Compare Model A vs Model B (main entry point)
├── outputs/                 # Generated evaluation reports (CSV + JSON + Markdown)
├── .env.example             # Environment variable template
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd email-gen-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

## Usage

### Generate a single email

```bash
python src/email_generator.py
```

### Run the model comparison (Model A vs Model B)

```bash
python scripts/model_comparison.py
```

This runs all 10 test scenarios through both models, scores them using 3 custom metrics, and produces:
- `outputs/evaluation_model_a.json` / `.csv` — Model A results
- `outputs/evaluation_model_b.json` / `.csv` — Model B results
- `outputs/comparison_results.json` / `.csv` — Side-by-side comparison
- `outputs/analysis_report.md` — Full analysis report

---

## Advanced Prompt Engineering Technique

This project uses a **Triple-Layer Prompting** approach combining:

1. **Role-Playing**: The LLM is instructed to act as a "Senior Business Communication Specialist" — this grounds its output style, vocabulary, and professional standards.

2. **Few-Shot Examples**: Three annotated example emails (formal, casual, urgent) are embedded in the system prompt. These demonstrate expected structure, tone calibration, and fact integration before the model ever sees the actual request.

3. **Chain-of-Thought (CoT)**: The model is asked to briefly think through intent → key facts → tone → structure before writing. This structured reasoning step consistently reduces fact omissions and tone drift.

---

## Custom Evaluation Metrics

### Metric 1 — Fact Coverage Score (Automated)
**Definition**: Measures what fraction of the user-supplied key facts are semantically present in the generated email.

**Logic**:
- Each key fact is split into meaningful tokens (stop words removed).
- For every fact, we check if its core tokens appear in the email body (case-insensitive substring + overlap scoring).
- Score = (facts found) / (total facts), range 0.0–1.0.

**Why this matters**: The primary job of an email assistant is to faithfully include the information the user provides. A beautiful email that omits critical facts is a failure.

---

### Metric 2 — Tone Alignment Score (LLM-as-Judge)
**Definition**: Measures how well the email's actual tone matches the requested tone.

**Logic**:
- Qwen3 32B (`qwen/qwen3-32b` via Groq) is used as an impartial judge.
- It reads the generated email + requested tone and scores 1–10.
- Score is normalised to 0.0–1.0.

**Why this matters**: Tone mismatch is a subtle but high-stakes failure. A "formal" email written casually can damage professional relationships.

---

### Metric 3 — Email Quality Score (LLM-as-Judge)
**Definition**: Holistic quality rating covering structure, grammar, clarity, subject line effectiveness, and call-to-action presence.

**Logic**:
- Qwen3 32B (`qwen/qwen3-32b` via Groq) rates the email on a 1–10 scale across five sub-dimensions.
- Score is normalised to 0.0–1.0.

**Why this matters**: Even fact-complete, tone-correct emails can fail if they are poorly structured, have grammatical errors, or lack a clear call-to-action.

---

## Model Comparison Summary

See `outputs/comparison_results.csv` for raw data and `outputs/analysis_report.md` for the full single-page analysis.

**Models tested**:
- **Model A**: `llama-3.3-70b-versatile` (Groq) — Role-Playing + Few-Shot + Chain-of-Thought prompting
- **Model B**: `llama-3.1-8b-instant` (Groq) — Simple zero-shot prompting (baseline)

**Judge model**: `qwen/qwen3-32b` (Groq) — A neutral model from a different family (Qwen, not Llama) to avoid evaluation bias
