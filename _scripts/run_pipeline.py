#!/usr/bin/env python3
"""
Run the full evaluation pipeline in the correct dependency order.

Phase 1 – Data (compute CSVs):
  1. compute_rq1_generation_quality RQ1 generation quality metrics
  2. compute_rq2_grading_quality    RQ2 grading quality metrics
  3. compute_rq2_grading_results    RQ2 authoritative N/TP/FP/FN from raw sheets
  4. compute_rq3_grader_stability   RQ3 grader stability metrics
  5. compute_element_distribution   Ground-truth element counts per system
  6. compute_rq2_weighted_kappa     Linear weighted Cohen's kappa

Phase 2 – Checks (data integrity validation):
  7. check_cohens_kappa_consistency   Validates Sheet 2/3 vs Cohen's Kappa sheet
  8. check_interrater_consistency     Validates Sheet 2/3 vs Inter-rater sheet

Phase 3 – Figures:
  9.  generate_agreement_figures        Per-file and aggregated confusion matrix PNGs
  10. generate_paper_rq2_confusion_matrices Publication-ready global confusion matrices

Usage:
  python run_pipeline.py              # run all phases
  python run_pipeline.py --phase data
  python run_pipeline.py --phase checks
  python run_pipeline.py --phase figures
  python run_pipeline.py --skip-figures
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
BASE_DIR = SCRIPTS_DIR.parent
DATA_DIR = BASE_DIR / "_Figures" / "data"

PIPELINE: list[tuple[str, Path, list[str] | None]] = [
    # (label, script_path, extra_args)
    (
        "compute_rq1_generation_quality",
        SCRIPTS_DIR / "compute" / "compute_rq1_generation_quality.py",
        None,
    ),
    (
        "compute_rq2_grading_quality",
        SCRIPTS_DIR / "compute" / "compute_rq2_grading_quality.py",
        None,
    ),
    (
        "compute_rq2_grading_results",
        SCRIPTS_DIR / "compute" / "compute_rq2_grading_results.py",
        None,
    ),
    (
        "compute_rq3_grader_stability",
        SCRIPTS_DIR / "compute" / "compute_rq3_grader_stability.py",
        None,
    ),
    (
        "compute_element_distribution",
        SCRIPTS_DIR / "compute" / "compute_element_distribution.py",
        None,
    ),
    (
        "compute_rq2_weighted_kappa",
        SCRIPTS_DIR / "compute" / "compute_rq2_weighted_kappa.py",
        None,
    ),
    (
        "check_cohens_kappa_consistency",
        SCRIPTS_DIR / "checks" / "check_cohens_kappa_consistency.py",
        None,
    ),
    (
        "check_interrater_consistency",
        SCRIPTS_DIR / "checks" / "check_interrater_consistency.py",
        None,
    ),
    (
        "generate_agreement_figures",
        SCRIPTS_DIR / "generate" / "generate_agreement_figures.py",
        None,
    ),
    (
        "generate_paper_rq2_confusion_matrices",
        SCRIPTS_DIR / "generate" / "generate_paper_rq2_confusion_matrices.py",
        None,
    ),
]

PHASE_RANGES = {
    "data": slice(0, 6),
    "checks": slice(6, 8),
    "figures": slice(8, 10),
}


def run_script(label: str, script: Path, extra_args: list[str] | None = None) -> bool:
    """Run a single script, streaming its output. Return True on success."""
    cmd = [sys.executable, str(script)] + (extra_args or [])
    print(f"\n{'=' * 70}")
    print(f"  Running: {label}")
    print(f"  Script:  {script.relative_to(BASE_DIR)}")
    print("=" * 70)

    t0 = time.monotonic()
    result = subprocess.run(cmd, cwd=str(BASE_DIR))
    elapsed = time.monotonic() - t0

    status = "OK" if result.returncode == 0 else f"FAILED (exit {result.returncode})"
    print(f"\n  [{status}]  {label}  ({elapsed:.1f}s)")
    return result.returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the evaluation pipeline.")
    parser.add_argument(
        "--phase",
        choices=["data", "checks", "figures"],
        default=None,
        help="Run only one phase instead of all three.",
    )
    parser.add_argument(
        "--skip-figures",
        action="store_true",
        help="Run data + checks phases only (skip figure generation).",
    )
    args = parser.parse_args()

    if args.phase:
        steps = PIPELINE[PHASE_RANGES[args.phase]]
    elif args.skip_figures:
        steps = PIPELINE[:8]  # data + checks only
    else:
        steps = PIPELINE[:]

    results: dict[str, bool] = {}
    for label, script, extra in steps:
        ok = run_script(label, script, extra)
        results[label] = ok
        if not ok:
            print(f"\n  Pipeline halted: {label} failed.")
            break

    print(f"\n{'=' * 70}")
    print("  Pipeline summary")
    print("=" * 70)
    for label, ok in results.items():
        icon = "✓" if ok else "✗"
        print(f"  {icon}  {label}")
    skipped = [label for label, _, _ in steps if label not in results]
    for label in skipped:
        print(f"  -  {label}  (skipped)")

    if all(results.values()):
        print("\n  All steps completed successfully.")
    else:
        failed = [label for label, ok in results.items() if not ok]
        print(f"\n  Failed: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
