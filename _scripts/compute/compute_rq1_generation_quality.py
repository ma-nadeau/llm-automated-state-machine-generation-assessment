#!/usr/bin/env python3
"""
RQ1: Human assessment of Claude-generated state machines.

Reads raw human scores from the 2nd sheet (Human Grading), column C, of every
*CombinedHumanGradingVsClaude4.5SonnetAutoGrading_Claude4.5SonnetGeneration.xlsx
workbook (all stages/shots), dynamically detects the split between expected
elements and additional (FP) elements, then computes weighted precision/recall/F1.

Weighted scoring:
  S  = sum of col-C scores for expected elements of a type  (weighted TP)
  TP = count of expected elements with score > 0            (binary TP count)
  FP = sum of col-C integer counts from additional-element rows (0, 1, 2, …)
  FN = count of expected elements with score == 0
  P  = S / (TP + FP),  R = S / (TP + FN),  F1 = 2PR/(P+R)

Outputs (written to _Figures/data/rq1/):
  rq1_generation_quality_summary.csv    — pooled counts + metrics per approach and element type
  rq1_generation_quality_by_example.csv — one row per (approach, project, element type)

Usage:
  python compute_rq1_generation_quality.py
  python compute_rq1_generation_quality.py --out-dir /custom/path
  python compute_rq1_generation_quality.py --print
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from _xlsx_utils import (
    BASE_DIR,
    TYPES,
    MetricRow,
    approach_from_path,
    fmt,
    iter_xlsx,
    md_table,
    parse_raw_grading_sheet,
    project_from_path,
    write_csv,
)

DEFAULT_OUT_DIR = BASE_DIR / "_Figures" / "data" / "rq1"

ELEMENT_TYPES = sorted(t for t in TYPES if t != "Overall Score")


def _compute_metrics(
    s: float, tp: float, fp: float, fn: float
) -> tuple[float | None, float | None, float | None]:
    precision = s / (tp + fp) if (tp + fp) > 0 else None
    recall = s / (tp + fn) if (tp + fn) > 0 else None
    if precision is not None and recall is not None and (precision + recall) > 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = None
    return precision, recall, f1


def load_human_metric_rows(root: Path) -> list[MetricRow]:
    files = sorted(iter_xlsx(root.glob(
        "*/Grading/*/*/"
        "*_CombinedHumanGradingVsClaude4.5SonnetAutoGrading_Claude4.5SonnetGeneration.xlsx"
    )))
    rows: list[MetricRow] = []
    for path in files:
        # Sheet index 1 = 2nd sheet = Human Grading
        type_data = parse_raw_grading_sheet(path, sheet_index=1)
        for label in ELEMENT_TYPES:
            d = type_data.get(label)
            if d is None:
                continue
            rows.append(
                MetricRow(
                    approach=approach_from_path(path),
                    project=project_from_path(path),
                    model_element=label,
                    n=d["N"],
                    tp=d["TP"],
                    fp=d["FP"],
                    fn=d["FN"],
                    s=d["S"],
                )
            )
    return rows


def summarize_rq1(root: Path) -> list[dict[str, object]]:
    metric_rows = load_human_metric_rows(root)
    grouped: dict[tuple[str, str], list[MetricRow]] = defaultdict(list)
    for row in metric_rows:
        grouped[(row.approach, row.model_element)].append(row)

    rows = []
    for approach in ("one-stage", "two-stage (3 examples)", "two-stage (6 examples)"):
        total_n = total_s = total_tp = total_fp = total_fn = 0.0
        approach_projects: set[str] = set()
        has_data = False

        for model_element in ELEMENT_TYPES:
            values = grouped.get((approach, model_element), [])
            if not values:
                continue
            has_data = True
            n  = sum(v.n  or 0 for v in values)
            s  = sum(v.s  or 0 for v in values)
            tp = sum(v.tp or 0 for v in values)
            fp = sum(v.fp or 0 for v in values)
            fn = sum(v.fn or 0 for v in values)
            precision, recall, f1 = _compute_metrics(s, tp, fp, fn)
            rows.append(
                {
                    "approach": approach,
                    "model_element": model_element,
                    "examples": len({v.project for v in values}),
                    "n": n,
                    "s": s,
                    "tp": tp,
                    "fp": fp,
                    "fn": fn,
                    "precision": round(precision, 3) if precision is not None else None,
                    "recall": round(recall, 3) if recall is not None else None,
                    "f1": round(f1, 3) if f1 is not None else None,
                }
            )
            total_n  += n
            total_s  += s
            total_tp += tp
            total_fp += fp
            total_fn += fn
            approach_projects.update(v.project for v in values)

        if has_data:
            precision, recall, f1 = _compute_metrics(total_s, total_tp, total_fp, total_fn)
            rows.append(
                {
                    "approach": approach,
                    "model_element": "Overall",
                    "examples": len(approach_projects),
                    "n": total_n,
                    "s": total_s,
                    "tp": total_tp,
                    "fp": total_fp,
                    "fn": total_fn,
                    "precision": round(precision, 3) if precision is not None else None,
                    "recall": round(recall, 3) if recall is not None else None,
                    "f1": round(f1, 3) if f1 is not None else None,
                }
            )
    return rows


def rq1_markdown(root: Path) -> str:
    table_rows = [
        [
            str(r["approach"]),
            str(r["model_element"]),
            str(r["examples"]),
            fmt(r["precision"]),
            fmt(r["recall"]),
            fmt(r["f1"]),
        ]
        for r in summarize_rq1(root)
    ]
    return md_table(
        ["Approach", "Model element", "Examples", "Precision", "Recall", "F1"],
        table_rows,
    )


def write_rq1(root: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        out_dir / "rq1_generation_quality_summary.csv",
        ["approach", "model_element", "examples", "n", "s", "tp", "fp", "fn", "precision", "recall", "f1"],
        summarize_rq1(root),
    )
    metric_rows = load_human_metric_rows(root)

    by_example_rows: list[dict[str, object]] = []
    totals: dict[tuple[str, str], dict[str, float]] = defaultdict(
        lambda: {"n": 0.0, "s": 0.0, "tp": 0.0, "fp": 0.0, "fn": 0.0}
    )
    for r in metric_rows:
        precision, recall, f1 = _compute_metrics(r.s or 0, r.tp or 0, r.fp or 0, r.fn or 0)
        by_example_rows.append(
            {
                "approach": r.approach,
                "project": r.project,
                "model_element": r.model_element,
                "n": r.n,
                "s": r.s,
                "tp": r.tp,
                "fp": r.fp,
                "fn": r.fn,
                "precision": round(precision, 3) if precision is not None else None,
                "recall": round(recall, 3) if recall is not None else None,
                "f1": round(f1, 3) if f1 is not None else None,
            }
        )
        key = (r.approach, r.project)
        t = totals[key]
        t["n"]  += r.n  or 0
        t["s"]  += r.s  or 0
        t["tp"] += r.tp or 0
        t["fp"] += r.fp or 0
        t["fn"] += r.fn or 0

    for (approach, project), t in sorted(totals.items()):
        precision, recall, f1 = _compute_metrics(t["s"], t["tp"], t["fp"], t["fn"])
        by_example_rows.append(
            {
                "approach": approach,
                "project": project,
                "model_element": "Overall",
                "n": t["n"],
                "s": t["s"],
                "tp": t["tp"],
                "fp": t["fp"],
                "fn": t["fn"],
                "precision": round(precision, 3) if precision is not None else None,
                "recall": round(recall, 3) if recall is not None else None,
                "f1": round(f1, 3) if f1 is not None else None,
            }
        )

    _BLIND_PROJECTS = {"SSC7", "Wumple"}
    _TWO_STAGE_6 = "two-stage (6 examples)"
    for group_label, predicate in [
        ("main examples", lambda p: p not in _BLIND_PROJECTS),
        ("blind test", lambda p: p in _BLIND_PROJECTS),
    ]:
        agg: dict[str, float] = {"n": 0.0, "s": 0.0, "tp": 0.0, "fp": 0.0, "fn": 0.0}
        for (approach, project), t in totals.items():
            if approach == _TWO_STAGE_6 and predicate(project):
                for k in agg:
                    agg[k] += t[k]
        precision, recall, f1 = _compute_metrics(agg["s"], agg["tp"], agg["fp"], agg["fn"])
        by_example_rows.append(
            {
                "approach": _TWO_STAGE_6,
                "project": group_label,
                "model_element": "Overall",
                "n": agg["n"],
                "s": agg["s"],
                "tp": agg["tp"],
                "fp": agg["fp"],
                "fn": agg["fn"],
                "precision": round(precision, 3) if precision is not None else None,
                "recall": round(recall, 3) if recall is not None else None,
                "f1": round(f1, 3) if f1 is not None else None,
            }
        )

    write_csv(
        out_dir / "rq1_generation_quality_by_example.csv",
        ["approach", "project", "model_element", "n", "s", "tp", "fp", "fn", "precision", "recall", "f1"],
        by_example_rows,
    )
    print(f"RQ1 CSVs written to: {out_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize RQ1 generation quality.")
    parser.add_argument("--root", type=Path, default=BASE_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--print", action="store_true", help="Print Markdown table to stdout.")
    args = parser.parse_args()

    if args.print:
        print("## RQ1: Claude Generation Quality From Human Assessment\n")
        print(rq1_markdown(args.root))
    else:
        write_rq1(args.root, args.out_dir)


if __name__ == "__main__":
    main()
