#!/usr/bin/env python3
"""
Aggregate CombinedHumanGrading vs LLM AutoGrading metrics for the 2-stage 6-examples setup.

Reads raw scores directly from the grading sheets (not the cached Metrics sheet):
  Sheet 2 (Human Grading) – col C scores, human grader.
  Sheet 3 (LLM Grading)   – col C scores, LLM auto-grader.

Dynamically detects the split between expected elements and additional (FP) elements
in each sheet by finding the first row where col B or col D contains "additional element".

Weighted scoring per element type:
  S  = sum of col-C scores for expected elements  (weighted TP)
  TP = count of expected elements with score > 0  (binary TP count)
  FP = sum of col-C integer counts from additional-element rows (0, 1, 2, …)
  FN = count of expected elements with score == 0
  P  = S / (TP + FP),  R = S / (TP + FN),  F1 = 2PR/(P+R)

The Human section is read only once per example (it is identical across the 3 LLM files).

Output: _Figures/data/rq2/rq2_2stage_6examples_Metrics_CombinedHumanVsLLM.csv
Columns: Grader, ElementType, TotalN, TotalS, TotalTP, TotalFP, TotalFN,
         TotalElements, Precision, Recall, F1
"""

import csv
import glob
import os
import re
from collections import defaultdict

from _xlsx_utils import parse_raw_grading_sheet
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
OUTPUT_DIR = os.path.join(BASE_DIR, "_Figures", "data", "rq2")
OUTPUT_FILE = "rq2_2stage_6examples_Metrics_CombinedHumanVsLLM.csv"

TARGET_TYPES = [
    "Action",
    "Composite State",
    "Guard",
    "History State",
    "Region",
    "State",
    "Transition",
]

HUMAN_GRADER_LABEL = "Human"

HUMAN_SHEET_INDEX = 1   # 2nd sheet = Human Grading
LLM_SHEET_INDEX   = 2   # 3rd sheet = LLM Grading


def compute_metrics(s, tp, fp, fn):
    precision = s / (tp + fp) if (tp + fp) > 0 else None
    recall    = s / (tp + fn) if (tp + fn) > 0 else None
    if precision is not None and recall is not None and (precision + recall) > 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = None
    return precision, recall, f1


def fmt(val, decimals=6):
    return round(val, decimals) if val is not None else "N/A"


def accumulate(agg, type_data):
    """Add parsed sheet data (dict: type -> {S,TP,FN,FP,N}) into agg."""
    for norm_type, d in type_data.items():
        agg[norm_type]["N"]  += d["N"]
        agg[norm_type]["S"]  += d["S"]
        agg[norm_type]["TP"] += d["TP"]
        agg[norm_type]["FP"] += d["FP"]
        agg[norm_type]["FN"] += d["FN"]


def main():
    pattern = os.path.join(
        BASE_DIR,
        "*/Grading/2 stage/6-examples/"
        "*_CombinedHumanGradingVs*AutoGrading_Claude4.5SonnetGeneration.xlsx",
    )
    files = sorted(
        f for f in glob.glob(pattern) if not os.path.basename(f).startswith("~")
    )

    if not files:
        print("ERROR: No matching files found.")
        return

    print(f"Found {len(files)} files.\n")

    # grader -> element_type -> cumulative {N, S, TP, FP, FN}
    aggregated = defaultdict(
        lambda: defaultdict(lambda: {"N": 0.0, "S": 0.0, "TP": 0.0, "FP": 0.0, "FN": 0.0})
    )

    human_examples_seen: set[str] = set()

    for filepath in files:
        bn = os.path.basename(filepath)
        m = re.search(r"CombinedHumanGradingVs(.+?)AutoGrading", bn)
        if not m:
            print(f"  WARNING: Cannot parse LLM name from: {bn}")
            continue
        llm = m.group(1)
        example = os.path.basename(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(filepath))))
        )

        path = Path(filepath)

        # ── Human grading: sheet 2 (index 1) ──
        human_flag = ""
        if example not in human_examples_seen:
            human_data = parse_raw_grading_sheet(path, HUMAN_SHEET_INDEX)
            accumulate(aggregated[HUMAN_GRADER_LABEL], human_data)
            human_examples_seen.add(example)
            human_flag = f"  [+human, {len(human_data)} types]"

        # ── LLM grading: sheet 3 (index 2) ──
        llm_data = parse_raw_grading_sheet(path, LLM_SHEET_INDEX)
        accumulate(aggregated[llm], llm_data)

        print(f"  {example:35} | {llm:25} | {len(llm_data)} LLM types{human_flag}")

    # ── Build output rows ─────────────────────────────────────────────────────
    GRADER_ORDER = [
        HUMAN_GRADER_LABEL,
        "Claude4.5Sonnet",
        "GPT-5.5",
        "Gemini3.1ProPreview",
    ]
    output_rows = []

    for grader in GRADER_ORDER:
        if grader not in aggregated:
            print(f"  WARNING: No data for grader '{grader}'")
            continue

        total_n = total_s = total_tp = total_fp = total_fn = 0.0

        for etype in TARGET_TYPES:
            d = aggregated[grader][etype]
            n, s, tp, fp, fn = d["N"], d["S"], d["TP"], d["FP"], d["FN"]
            precision, recall, f1 = compute_metrics(s, tp, fp, fn)
            output_rows.append(
                {
                    "Grader": grader,
                    "ElementType": etype,
                    "TotalN": round(n, 4),
                    "TotalS": round(s, 4),
                    "TotalTP": round(tp, 4),
                    "TotalFP": round(fp, 4),
                    "TotalFN": round(fn, 4),
                    "TotalElements": round(n + fp, 4),
                    "Precision": fmt(precision),
                    "Recall": fmt(recall),
                    "F1": fmt(f1),
                }
            )
            total_n  += n
            total_s  += s
            total_tp += tp
            total_fp += fp
            total_fn += fn

        precision, recall, f1 = compute_metrics(total_s, total_tp, total_fp, total_fn)
        output_rows.append(
            {
                "Grader": grader,
                "ElementType": "Overall",
                "TotalN": round(total_n, 4),
                "TotalS": round(total_s, 4),
                "TotalTP": round(total_tp, 4),
                "TotalFP": round(total_fp, 4),
                "TotalFN": round(total_fn, 4),
                "TotalElements": round(total_n + total_fp, 4),
                "Precision": fmt(precision),
                "Recall": fmt(recall),
                "F1": fmt(f1),
            }
        )

    # ── Write CSV ─────────────────────────────────────────────────────────────
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    fields = [
        "Grader", "ElementType",
        "TotalN", "TotalS", "TotalTP", "TotalFP", "TotalFN",
        "TotalElements", "Precision", "Recall", "F1",
    ]
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)

    # ── Console summary ───────────────────────────────────────────────────────
    print("\n" + "=" * 110)
    print(
        f"{'Grader':25} {'ElementType':20} {'N':>7} {'S':>7} {'TP':>7} {'FP':>7} {'FN':>7}  {'Prec':>8} {'Rec':>8} {'F1':>8}"
    )
    print("=" * 110)
    prev_grader = None
    for r in output_rows:
        if r["Grader"] != prev_grader:
            if prev_grader is not None:
                print()
            prev_grader = r["Grader"]
        marker = "  <-- Overall" if r["ElementType"] == "Overall" else ""
        print(
            f"{r['Grader']:25} {r['ElementType']:20} "
            f"{r['TotalN']:>7} {r['TotalS']:>7} {r['TotalTP']:>7} {r['TotalFP']:>7} {r['TotalFN']:>7}  "
            f"{str(r['Precision']):>8} {str(r['Recall']):>8} {str(r['F1']):>8}{marker}"
        )

    print(f"\nOutput written to: {out_path}")


if __name__ == "__main__":
    main()
