"""
Evaluation Runner
==================
Runs all 10 test scenarios through the email generator, scores each result
using the 3 custom metrics, and outputs structured reports (JSON + CSV).

Usage:
    python src/evaluator.py
"""

import os
import json
import csv
import time
from datetime import datetime
from dotenv import load_dotenv

from email_generator import generate_email
from test_scenarios import TEST_SCENARIOS
from metrics import evaluate_all, ALL_METRIC_DEFINITIONS

load_dotenv()

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")


def run_evaluation(
    model: str = "claude-opus-4-6",
    use_advanced_prompting: bool = True,
    output_tag: str = "model_a",
    provider: str = "anthropic",
) -> dict:
    """
    Run the full evaluation pipeline.

    Args:
        model:                  Model ID to generate emails.
        use_advanced_prompting: If True, uses Role-Playing + Few-Shot + CoT.
        output_tag:             Label appended to output filenames.
        provider:               "anthropic" or "groq".

    Returns:
        dict containing scenario results and aggregate stats.
    """
    print(f"\n{'='*60}")
    print(f"EVALUATION RUN: {output_tag.upper()}")
    print(f"Model: {model}  |  Advanced Prompting: {use_advanced_prompting}")
    print(f"{'='*60}\n")

    results = []
    total_scores = {
        "fact_coverage_score": 0.0,
        "tone_alignment_score": 0.0,
        "email_quality_score": 0.0,
        "composite_score": 0.0,
    }

    for scenario in TEST_SCENARIOS:
        sid = scenario["id"]
        print(f"[{sid:02d}/10] Generating email for: {scenario['intent'][:55]}...")

        # Step 1 — Generate email
        gen_result = generate_email(
            intent=scenario["intent"],
            key_facts=scenario["key_facts"],
            tone=scenario["tone"],
            model=model,
            use_advanced_prompting=use_advanced_prompting,
            provider=provider,
        )
        email_text = gen_result["email_text"]

        # Step 2 — Score with all 3 metrics
        print(f"         Scoring metrics...")
        scores = evaluate_all(
            intent=scenario["intent"],
            key_facts=scenario["key_facts"],
            tone=scenario["tone"],
            email_text=email_text,
        )

        # Step 3 — Accumulate
        for key in total_scores:
            total_scores[key] += scores[key]

        record = {
            "scenario_id": sid,
            "intent": scenario["intent"],
            "tone": scenario["tone"],
            "key_facts": scenario["key_facts"],
            "generated_email": email_text,
            "human_reference": scenario["human_reference"],
            "fact_coverage_score": scores["fact_coverage_score"],
            "tone_alignment_score": scores["tone_alignment_score"],
            "email_quality_score": scores["email_quality_score"],
            "composite_score": scores["composite_score"],
            "model": gen_result["model"],
            "input_tokens": gen_result["input_tokens"],
            "output_tokens": gen_result["output_tokens"],
        }
        results.append(record)

        print(
            f"         FC={scores['fact_coverage_score']:.2f}  "
            f"TA={scores['tone_alignment_score']:.2f}  "
            f"EQ={scores['email_quality_score']:.2f}  "
            f"Composite={scores['composite_score']:.2f}"
        )

        # Slight delay to avoid rate-limit issues
        time.sleep(1)

    n = len(TEST_SCENARIOS)
    averages = {k: round(v / n, 4) for k, v in total_scores.items()}

    print(f"\n{'='*60}")
    print("AVERAGE SCORES")
    print(f"  Fact Coverage    : {averages['fact_coverage_score']:.4f}")
    print(f"  Tone Alignment   : {averages['tone_alignment_score']:.4f}")
    print(f"  Email Quality    : {averages['email_quality_score']:.4f}")
    print(f"  COMPOSITE        : {averages['composite_score']:.4f}")
    print(f"{'='*60}\n")

    return {
        "run_tag": output_tag,
        "model": model,
        "use_advanced_prompting": use_advanced_prompting,
        "timestamp": datetime.utcnow().isoformat(),
        "metric_definitions": ALL_METRIC_DEFINITIONS,
        "results": results,
        "averages": averages,
    }


def save_json(data: dict, filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"JSON saved: {filepath}")


def save_csv(data: dict, filepath: str) -> None:
    """Save per-scenario scores as a flat CSV."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    fieldnames = [
        "scenario_id", "intent", "tone",
        "fact_coverage_score", "tone_alignment_score",
        "email_quality_score", "composite_score",
        "model", "input_tokens", "output_tokens",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in data["results"]:
            writer.writerow({k: r[k] for k in fieldnames})

        # Append averages row
        writer.writerow({
            "scenario_id": "AVERAGE",
            "intent": "-",
            "tone": "-",
            "fact_coverage_score": data["averages"]["fact_coverage_score"],
            "tone_alignment_score": data["averages"]["tone_alignment_score"],
            "email_quality_score": data["averages"]["email_quality_score"],
            "composite_score": data["averages"]["composite_score"],
            "model": data["model"],
            "input_tokens": "-",
            "output_tokens": "-",
        })

    print(f"CSV saved: {filepath}")


if __name__ == "__main__":
    tag = "model_a_opus_advanced"
    eval_data = run_evaluation(
        model="claude-opus-4-6",
        use_advanced_prompting=True,
        output_tag=tag,
    )

    json_path = os.path.join(OUTPUT_DIR, f"evaluation_{tag}.json")
    csv_path  = os.path.join(OUTPUT_DIR, f"evaluation_{tag}.csv")

    save_json(eval_data, json_path)
    save_csv(eval_data, csv_path)

    print("\nEvaluation complete.")
