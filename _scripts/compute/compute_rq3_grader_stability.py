#!/usr/bin/env python3
"""
RQ3: Grader behavior consistency across Claude/GPT/Gemini-generated state machines.

Reads grading_results__generated-by-*__graded-by-*.tsv files and computes:
  - Score distributions per generator/grader/element type
  - Per-grader stability (baseline vs. comparison generator deltas)
  - Cross-grader rankings by score-1 rate

Outputs (written to _Figures/data/rq3/):
  rq3_grading_score_distribution.csv
  rq3_per_grader_stability.csv
  rq3_cross_grader_rankings.csv

Usage:
  python compute_rq3_grader_stability.py                         # writes CSVs to default out-dir
  python compute_rq3_grader_stability.py --out-dir /custom/path  # override output directory
  python compute_rq3_grader_stability.py --print                 # print Markdown tables to stdout only
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

from _xlsx_utils import (
    BASE_DIR,
    RQ3_BASELINE_GENERATOR,
    RQ3_COMPARISON_GENERATORS,
    RQ3_GENERATORS,
    SCORES,
    TYPES,
    as_float,
    canonical_model_name,
    fmt,
    generator_from_tsv,
    grader_from_tsv,
    md_table,
    write_csv,
)

DEFAULT_OUT_DIR = BASE_DIR / "_Figures" / "data" / "rq3"


# ── TSV loading ───────────────────────────────────────────────────────────────

def score_distribution(
    tsv_files: list[Path],
) -> dict[tuple[str, str, str], Counter[float]]:
    dist: dict[tuple[str, str, str], Counter[float]] = defaultdict(Counter)
    for path in tsv_files:
        generator = canonical_model_name(generator_from_tsv(path))
        grader = canonical_model_name(grader_from_tsv(path))
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row in reader:
                model_element = (row.get("Type") or row.get("type") or "").strip()
                grade = as_float((row.get("Grading") or row.get("grading") or "").strip())
                if model_element and grade in SCORES:
                    dist[(generator, grader, model_element)][grade] += 1
                    dist[(generator, grader, "Overall Score")][grade] += 1
    return dist


def _rq3_files(root: Path) -> list[Path]:
    files = sorted(
        root.glob(
            "*/Grading/2 stage/6-examples/Generated Files/grading_results__generated-by-*__graded-by-*.tsv"
        )
    )
    return [
        p for p in files
        if canonical_model_name(generator_from_tsv(p)) in RQ3_GENERATORS
    ]


# ── Summarize functions ───────────────────────────────────────────────────────

def summarize_rq3(root: Path) -> list[dict[str, object]]:
    dist = score_distribution(_rq3_files(root))
    rows = []
    for (generator, grader, model_element), counts in sorted(dist.items()):
        if model_element not in TYPES:
            continue
        total = sum(counts.values())
        rows.append(
            {
                "generator": generator,
                "grader": grader,
                "model_element": model_element,
                "items": total,
                "score_0_count": counts[0.0],
                "score_0_5_count": counts[0.5],
                "score_1_count": counts[1.0],
                "score_0_pct": counts[0.0] / total if total else None,
                "score_0_5_pct": counts[0.5] / total if total else None,
                "score_1_pct": counts[1.0] / total if total else None,
            }
        )
    return rows


def _rq3_lookup(root: Path) -> dict[tuple[str, str, str], dict[str, object]]:
    return {
        (str(r["generator"]), str(r["grader"]), str(r["model_element"])): r
        for r in summarize_rq3(root)
    }


def summarize_rq3_per_grader_stability(root: Path) -> list[dict[str, object]]:
    lookup = _rq3_lookup(root)
    graders = sorted({grader for _, grader, _ in lookup})
    rows = []
    for grader in graders:
        for model_element in TYPES:
            baseline = lookup.get((RQ3_BASELINE_GENERATOR, grader, model_element))
            if baseline is None:
                continue
            for comparison_generator in RQ3_COMPARISON_GENERATORS:
                comparison = lookup.get((comparison_generator, grader, model_element))
                if comparison is None:
                    continue
                rows.append(
                    {
                        "grader": grader,
                        "model_element": model_element,
                        "baseline_generator": RQ3_BASELINE_GENERATOR,
                        "comparison_generator": comparison_generator,
                        "baseline_score_0_pct": baseline["score_0_pct"],
                        "baseline_score_0_5_pct": baseline["score_0_5_pct"],
                        "baseline_score_1_pct": baseline["score_1_pct"],
                        "comparison_score_0_pct": comparison["score_0_pct"],
                        "comparison_score_0_5_pct": comparison["score_0_5_pct"],
                        "comparison_score_1_pct": comparison["score_1_pct"],
                        "delta_score_0_pct": comparison["score_0_pct"] - baseline["score_0_pct"],
                        "delta_score_0_5_pct": comparison["score_0_5_pct"] - baseline["score_0_5_pct"],
                        "delta_score_1_pct": comparison["score_1_pct"] - baseline["score_1_pct"],
                    }
                )
    return rows


def summarize_rq3_cross_grader_rankings(root: Path) -> list[dict[str, object]]:
    lookup = _rq3_lookup(root)
    rows = []
    for generator in sorted({gen for gen, _, _ in lookup}):
        for model_element in TYPES:
            candidates = [
                row for (row_gen, _, row_el), row in lookup.items()
                if row_gen == generator and row_el == model_element
            ]
            candidates.sort(key=lambda r: (-r["score_1_pct"], str(r["grader"])))
            previous_score = None
            previous_rank = 0
            for index, row in enumerate(candidates, start=1):
                score = row["score_1_pct"]
                rank = previous_rank if previous_score == score else index
                previous_score = score
                previous_rank = rank
                rows.append(
                    {
                        "generator": generator,
                        "model_element": model_element,
                        "grader": row["grader"],
                        "score_1_pct": score,
                        "rank_by_score_1": rank,
                    }
                )
    return rows


# ── Markdown ──────────────────────────────────────────────────────────────────

def rq3_markdown(root: Path) -> str:
    distribution_rows = [
        [
            str(r["generator"]), str(r["grader"]), str(r["model_element"]),
            str(r["items"]), fmt(r["score_0_pct"]), fmt(r["score_0_5_pct"]), fmt(r["score_1_pct"]),
        ]
        for r in summarize_rq3(root)
    ]

    stability_rows = [
        [
            str(r["grader"]), str(r["comparison_generator"]),
            fmt(r["baseline_score_1_pct"]), fmt(r["comparison_score_1_pct"]), fmt(r["delta_score_1_pct"]),
            fmt(r["baseline_score_0_5_pct"]), fmt(r["comparison_score_0_5_pct"]), fmt(r["delta_score_0_5_pct"]),
        ]
        for r in summarize_rq3_per_grader_stability(root)
        if r["model_element"] == "Overall Score"
    ]

    ranking_rows = [
        [str(r["generator"]), str(r["grader"]), fmt(r["score_1_pct"]), str(r["rank_by_score_1"])]
        for r in summarize_rq3_cross_grader_rankings(root)
        if r["model_element"] == "Overall Score"
    ]

    note = (
        "RQ3 tests whether grader behavior patterns observed on Claude-generated "
        "state machines persist when the generated inputs change to GPT-5.5 and "
        "Gemini 3.1 Pro Preview outputs. Claude-generated state machines are the "
        "baseline condition; GPT-5.5- and Gemini-generated state machines are "
        "comparison conditions. These tables use only LLM-assigned score "
        "distributions and do not evaluate GPT/Gemini generation quality because "
        "human ground truth is not available for those generated state machines."
    )
    return "\n\n".join(
        [
            note,
            "**Score distributions**",
            md_table(
                ["Generator", "Grader", "Model element", "Items", "Score 0", "Score 0.5", "Score 1"],
                distribution_rows,
            ),
            "**Per-grader stability (Overall Score)**",
            md_table(
                ["Grader", "Comparison generator", "Baseline %1", "Comparison %1", "Delta %1",
                 "Baseline %0.5", "Comparison %0.5", "Delta %0.5"],
                stability_rows,
            ),
            "**Cross-grader rankings by %1 (Overall Score)**",
            md_table(["Generator", "Grader", "Score 1", "Rank"], ranking_rows),
        ]
    )


# ── Write ─────────────────────────────────────────────────────────────────────

def write_rq3(root: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        out_dir / "rq3_grading_score_distribution.csv",
        ["generator", "grader", "model_element", "items",
         "score_0_count", "score_0_5_count", "score_1_count",
         "score_0_pct", "score_0_5_pct", "score_1_pct"],
        summarize_rq3(root),
    )
    write_csv(
        out_dir / "rq3_per_grader_stability.csv",
        ["grader", "model_element", "baseline_generator", "comparison_generator",
         "baseline_score_0_pct", "baseline_score_0_5_pct", "baseline_score_1_pct",
         "comparison_score_0_pct", "comparison_score_0_5_pct", "comparison_score_1_pct",
         "delta_score_0_pct", "delta_score_0_5_pct", "delta_score_1_pct"],
        summarize_rq3_per_grader_stability(root),
    )
    write_csv(
        out_dir / "rq3_cross_grader_rankings.csv",
        ["generator", "model_element", "grader", "score_1_pct", "rank_by_score_1"],
        summarize_rq3_cross_grader_rankings(root),
    )
    print(f"RQ3 CSVs written to: {out_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize RQ3 grader stability.")
    parser.add_argument("--root", type=Path, default=BASE_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--print", action="store_true", help="Print Markdown tables to stdout.")
    args = parser.parse_args()

    if args.print:
        print("## RQ3: Grader Behavior Consistency Across Generated Inputs\n")
        print(rq3_markdown(args.root))
    else:
        write_rq3(args.root, args.out_dir)


if __name__ == "__main__":
    main()
