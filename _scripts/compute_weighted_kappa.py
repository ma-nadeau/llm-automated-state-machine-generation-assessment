#!/usr/bin/env python3
"""
Computes linear weighted Cohen's kappa between human and LLM grading.

Input:  _Figures/PaperExperimentData/rq2_confusion_matrices.csv
Output: _Figures/PaperExperimentData/rq2_weighted_kappa_results.csv  (+ printed table)

Usage:
  python compute_weighted_kappa.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.metrics import cohen_kappa_score

# Resolve paths relative to this script so the script works from any cwd.
# BASE_DIR = Evaluations/, DATA_DIR = Evaluations/_Figures/PaperExperimentData/
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "_Figures" / "PaperExperimentData"
CSV_IN   = DATA_DIR / "rq2_confusion_matrices.csv"   # aggregated confusion-matrix rows
CSV_OUT  = DATA_DIR / "rq2_weighted_kappa_results.csv"

# The grading rubric allows three score values: 0, 0.5, and 1.
VALID_SCORES = {0.0, 0.5, 1.0}

# sklearn's linear-weight formula is  w(i,j) = |i−j| / (max_label − min_label).
# If we pass the raw float labels {0.0, 0.5, 1.0} sklearn may treat the scale as
# continuous and produce incorrect weights.  Mapping to consecutive integers
# {0, 1, 2} makes sklearn recognise them as ordinal classes while preserving the
# relative distances: w(0↔1) = w(1↔2) = 0.5 and w(0↔2) = 1 — identical to the
# spreadsheet's  |score_A − score_B| / 1  weight matrix.
SCORE_TO_INT = {0.0: 0, 0.5: 1, 1.0: 2}
INT_LABELS   = [0, 1, 2]   # passed explicitly so the 3×3 weight matrix is always used


# ── helpers ───────────────────────────────────────────────────────────────────

def expand_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Expand aggregated (human, llm, count) rows into individual pair rows.

    The CSV stores the confusion matrix in long form: each row holds a
    (human_score, llm_score, count) triplet — i.e. one cell of the confusion
    matrix.  sklearn expects one row per rated item, so we repeat each pair
    `count` times and convert the scores to their integer equivalents.
    """
    rows = []
    for _, r in df.iterrows():
        # Repeat this (human, llm) integer pair `count` times to reconstruct
        # the full list of individual ratings.
        rows.extend(
            [(SCORE_TO_INT[r["human_score"]], SCORE_TO_INT[r["llm_score"]])]
            * int(r["count"])
        )
    if not rows:
        return pd.DataFrame(columns=["human_int", "llm_int"])
    return pd.DataFrame(rows, columns=["human_int", "llm_int"])


def compute_kappa(pairs: pd.DataFrame) -> tuple[float | None, int]:
    """Compute linear weighted Cohen's kappa from a pairs DataFrame.

    Returns (kappa, n).  Returns (None, n) when kappa cannot be computed
    (fewer than 2 items, or all items share the same score — in that case the
    expected disagreement D_exp is 0 and κ = 1 − D_obs/D_exp is undefined).

    Formula (equivalent to the spreadsheet):
        κ = 1 − D_obs / D_exp
    where
        D_obs = Σ  (observed_count(i,j) / n) × w(i,j)   [observed weighted disagreement]
        D_exp = Σ  (row_i_total/n × col_j_total/n) × w(i,j)  [chance weighted disagreement]
        w(i,j) = |i−j| / (max_label − min_label)              [linear disagreement weight]
    """
    n = len(pairs)
    # Need at least 2 items to estimate agreement.
    if n < 2:
        return None, n

    y_human = pairs["human_int"].tolist()
    y_llm   = pairs["llm_int"].tolist()

    # If every rating in the combined set is identical, D_exp = 0 and kappa is
    # undefined (division by zero inside sklearn).  Return None instead.
    if len(set(y_human + y_llm)) < 2:
        return None, n

    try:
        # weights="linear" → w(i,j) = |i−j| / (n_classes − 1)
        # labels=INT_LABELS forces the full 3×3 weight matrix even when one
        # score level is absent from this particular subset.
        kappa = cohen_kappa_score(y_human, y_llm, weights="linear", labels=INT_LABELS)
    except Exception:
        return None, n

    return kappa, n


# ── load & validate ───────────────────────────────────────────────────────────

# Read the long-form confusion matrix: one row per (grader, model_element,
# human_score, llm_score) combination, with a `count` column.
df = pd.read_csv(CSV_IN)

# Abort early if the expected columns are missing rather than producing
# cryptic KeyErrors later.
required_cols = {"grader", "model_element", "human_score", "llm_score", "count"}
missing = required_cols - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {missing}")

# Drop rows where any key field is NaN — they cannot contribute to kappa.
df = df.dropna(subset=["grader", "model_element", "human_score", "llm_score", "count"])

# Validate that every score is one of the three allowed rubric values.
# Out-of-range scores would silently corrupt the weight matrix, so warn and drop.
invalid_human = df[~df["human_score"].isin(VALID_SCORES)]
invalid_llm   = df[~df["llm_score"].isin(VALID_SCORES)]
if not invalid_human.empty:
    print(f"WARNING: {len(invalid_human)} rows with invalid human_score dropped.")
    df = df[df["human_score"].isin(VALID_SCORES)]
if not invalid_llm.empty:
    print(f"WARNING: {len(invalid_llm)} rows with invalid llm_score dropped.")
    df = df[df["llm_score"].isin(VALID_SCORES)]

# Ensure count is an integer and remove zero-count rows (no items to expand).
df["count"] = df["count"].astype(int)
df = df[df["count"] > 0]

# Collect unique graders (LLMs) and model-element categories.
# "Overall Score" is excluded from per-category analysis: it is a composite
# of the other categories and including it would double-count those items when
# pooling all categories for the overall kappa.
llms       = sorted(df["grader"].unique())
categories = sorted(c for c in df["model_element"].unique() if c != "Overall Score")

print(f"LLMs detected      : {llms}")
print(f"Categories detected: {categories}")
print()

# ── compute kappas ────────────────────────────────────────────────────────────

results = []

for llm in llms:
    # Isolate all rows for this grader.
    llm_df = df[df["grader"] == llm]

    # Per-category kappa: build the confusion matrix for one model element at a
    # time, expand it into individual (human, llm) pairs, then compute kappa.
    for cat in categories:
        cat_df = llm_df[llm_df["model_element"] == cat]
        pairs  = expand_rows(cat_df)          # reconstruct individual ratings
        kappa, n = compute_kappa(pairs)       # κ = 1 − D_obs / D_exp
        results.append({"LLM": llm, "Category": cat, "Kappa": kappa, "n": n})

    # Overall kappa: pool every per-category pair for this LLM into one set.
    # This is equivalent to computing kappa on the full confusion matrix
    # (sum of all per-category matrices), which is the correct aggregate.
    overall_df = llm_df[llm_df["model_element"].isin(categories)]
    pairs      = expand_rows(overall_df)
    kappa, n   = compute_kappa(pairs)
    results.append({"LLM": llm, "Category": "Overall", "Kappa": kappa, "n": n})

results_df = pd.DataFrame(results)

# ── display ───────────────────────────────────────────────────────────────────

def fmt_kappa(v: float | None) -> str:
    # Show 4 decimal places for valid kappa values; "N/A" when undefined.
    return f"{v:.4f}" if v is not None else "N/A"

# Compute column widths dynamically so the table stays aligned regardless of
# how long the LLM names or category names are.
col_w = {
    "LLM":      max(len("LLM"),      results_df["LLM"].str.len().max()),
    "Category": max(len("Category"), results_df["Category"].str.len().max()),
    "Kappa":    max(len("Linear Weighted Cohen's Kappa"), 10),
    "n":        max(len("n"), 6),
}

header = (
    f"{'LLM':<{col_w['LLM']}}  "
    f"{'Category':<{col_w['Category']}}  "
    f"{'Linear Weighted Cohen\'s Kappa':>{col_w['Kappa']}}  "
    f"{'n':>{col_w['n']}}"
)
print(header)
print("-" * len(header))

# Print one row per (LLM, Category) pair; insert a blank line between LLMs
# to visually separate each grader's block.
prev_llm = None
for _, row in results_df.iterrows():
    if prev_llm and row["LLM"] != prev_llm:
        print()
    print(
        f"{row['LLM']:<{col_w['LLM']}}  "
        f"{row['Category']:<{col_w['Category']}}  "
        f"{fmt_kappa(row['Kappa']):>{col_w['Kappa']}}  "
        f"{row['n']:>{col_w['n']}}"
    )
    prev_llm = row["LLM"]

# ── export ────────────────────────────────────────────────────────────────────

# Round kappa to 6 decimal places before writing to avoid floating-point
# noise in the CSV (e.g. 0.8000000000000002 → 0.8).
export_df = results_df.copy()
export_df["Kappa"] = export_df["Kappa"].apply(
    lambda v: round(v, 6) if v is not None else None
)
export_df.to_csv(CSV_OUT, index=False)
print(f"\nResults exported to: {CSV_OUT.relative_to(BASE_DIR)}")
