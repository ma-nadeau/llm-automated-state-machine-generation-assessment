#!/usr/bin/env python3
"""
RQ2: Human inter-rater agreement for manual grading of Claude-generated state machines.

Reads all _HumanGrading_ xlsx workbooks and computes the linear weighted Cohen's
kappa between the two human raters for each assessment (project × approach).

Reports:
  - Per approach (2-stage 6-shot, 2-stage 3-shot, 1-stage 3-shot):
      kappa per project, average kappa, % of assessments with kappa > 0.80
  - Aggregate across all approaches:
      average kappa, % of assessments with kappa > 0.80

Output written to _Figures/data/rq2/rq2_human_grading_agreement.csv

Usage:
  python compute_rq2_human_grading_agreement.py
"""

from __future__ import annotations

from pathlib import Path

from sklearn.metrics import cohen_kappa_score

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _xlsx_utils import (
    BASE_DIR,
    as_float,
    iter_xlsx,
    project_from_path,
    sheet_rows,
    stage_shot_from_path,
    write_csv,
)

DEFAULT_OUT_DIR = BASE_DIR / "_Figures" / "data" / "rq2"

VALID_SCORES = {0.0, 0.5, 1.0}
SCORE_TO_INT = {0.0: 0, 0.5: 1, 1.0: 2}
INT_LABELS = [0, 1, 2]

APPROACH_ORDER = ["2-stage 6-shot", "2-stage 3-shot", "1-stage 3-shot"]


# ── helpers ───────────────────────────────────────────────────────────────────


def approach_label(stage: str, shot: str) -> str:
    if stage == "1":
        return "1-stage 3-shot"
    return "2-stage 6-shot" if shot == "6-examples" else "2-stage 3-shot"


def load_human_pairs(path: Path) -> list[tuple[int, int]]:
    """Extract (rater1_int, rater2_int) score pairs from the Weighted Cohens Kappa sheet.

    'Additional elements' rows store element counts rather than 0/0.5/1 scores.
    They are converted to binary (present/absent) pairs using the same logic as
    the confusion() function in compute_rq2_grading_quality.py:
      - both counts 0          → one (0, 0) pair
      - counts c1, c2 > 0     → min(c1,c2) agreed (1,1) pairs
                                 + excess (0,1) or (1,0) disagreement pairs
    """
    pairs = []
    for row in sheet_rows(path, "Weighted Cohens Kappa")[1:]:
        if len(row) < 4 or not row[0] or not row[1]:
            break
        r1 = as_float(row[2])
        r2 = as_float(row[3])
        if r1 is None or r2 is None:
            continue

        if row[1].strip().lower() == "additional elements":
            c1, c2 = int(r1), int(r2)
            if c1 == 0 and c2 == 0:
                pairs.append((SCORE_TO_INT[0.0], SCORE_TO_INT[0.0]))
            else:
                pairs.extend([(SCORE_TO_INT[1.0], SCORE_TO_INT[1.0])] * min(c1, c2))
                pairs.extend([(SCORE_TO_INT[0.0], SCORE_TO_INT[1.0])] * max(c2 - c1, 0))
                pairs.extend([(SCORE_TO_INT[1.0], SCORE_TO_INT[0.0])] * max(c1 - c2, 0))
        else:
            if r1 not in VALID_SCORES or r2 not in VALID_SCORES:
                continue
            pairs.append((SCORE_TO_INT[r1], SCORE_TO_INT[r2]))
    return pairs


def compute_kappa(pairs: list[tuple[int, int]]) -> tuple[float | None, int]:
    """Compute linear weighted Cohen's kappa from (rater1, rater2) integer pairs."""
    n = len(pairs)
    if n < 2:
        return None, n
    y1 = [p[0] for p in pairs]
    y2 = [p[1] for p in pairs]
    if len(set(y1 + y2)) < 2:
        return None, n
    try:
        kappa = cohen_kappa_score(y1, y2, weights="linear", labels=INT_LABELS)
    except Exception:
        return None, n
    return kappa, n


def human_grading_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in [
        "*/Grading/1 stage/3-examples/*_HumanGrading_*.xlsx",
        "*/Grading/2 stage/3-examples/*_HumanGrading_*.xlsx",
        "*/Grading/2 stage/6-examples/*_HumanGrading_*.xlsx",
    ]:
        files.extend(root.glob(pattern))
    return sorted(files)


def fmt_kappa(v: float | None) -> str:
    return f"{v:.4f}" if v is not None else "N/A"


# ── main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    root = BASE_DIR
    out_dir = DEFAULT_OUT_DIR

    results: list[dict[str, object]] = []
    for path in iter_xlsx(human_grading_files(root)):
        project = project_from_path(path)
        stage, shot = stage_shot_from_path(path)
        approach = approach_label(stage, shot)
        pairs = load_human_pairs(path)
        kappa, n = compute_kappa(pairs)
        results.append({"approach": approach, "project": project, "kappa": kappa, "n": n})

    # ── per-approach tables ───────────────────────────────────────────────────

    for approach in APPROACH_ORDER:
        subset = [r for r in results if r["approach"] == approach]
        if not subset:
            continue

        print(f"\n{'=' * 60}")
        print(f"  {approach}")
        print(f"{'=' * 60}")

        proj_w = max(len("Project"), max(len(str(r["project"])) for r in subset))
        header = f"{'Project':<{proj_w}}  {'Kappa':>10}  {'n':>5}"
        print(header)
        print("-" * len(header))

        valid: list[float] = []
        for r in sorted(subset, key=lambda x: x["project"]):
            k_str = fmt_kappa(r["kappa"])
            print(f"{r['project']:<{proj_w}}  {k_str:>10}  {r['n']:>5}")
            if r["kappa"] is not None:
                valid.append(float(r["kappa"]))

        if valid:
            avg = sum(valid) / len(valid)
            pct = 100.0 * sum(1 for k in valid if k > 0.80) / len(valid)
            print(f"\n  Assessments   : {len(valid)}")
            print(f"  Average kappa : {avg:.4f}")
            print(f"  % kappa > 0.80: {pct:.1f}%")

    # ── aggregate summary ─────────────────────────────────────────────────────

    all_kappas = [float(r["kappa"]) for r in results if r["kappa"] is not None]

    print(f"\n{'=' * 60}")
    print("  Aggregate (all approaches combined)")
    print(f"{'=' * 60}")

    if all_kappas:
        total_avg = sum(all_kappas) / len(all_kappas)
        total_pct = 100.0 * sum(1 for k in all_kappas if k > 0.80) / len(all_kappas)
        print(f"  Total assessments : {len(all_kappas)}")
        print(f"  Average kappa     : {total_avg:.4f}")
        print(f"  % kappa > 0.80    : {total_pct:.1f}%")
    else:
        print("  No valid kappa values found.")

    # ── export CSV ────────────────────────────────────────────────────────────

    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "rq2_human_grading_agreement.csv"

    export: list[dict[str, object]] = [
        {
            "approach": r["approach"],
            "project": r["project"],
            "kappa": round(float(r["kappa"]), 6) if r["kappa"] is not None else "",
            "n": r["n"],
            "pct_above_0.80": "",
        }
        for r in results
    ]

    # Per-approach aggregate rows
    for approach in APPROACH_ORDER:
        subset_kappas = [
            float(r["kappa"]) for r in results
            if r["approach"] == approach and r["kappa"] is not None
        ]
        if not subset_kappas:
            continue
        export.append({
            "approach": approach,
            "project": "Aggregate",
            "kappa": round(sum(subset_kappas) / len(subset_kappas), 6),
            "n": sum(r["n"] for r in results if r["approach"] == approach),
            "pct_above_0.80": round(
                100.0 * sum(1 for k in subset_kappas if k > 0.80) / len(subset_kappas), 1
            ),
        })

    # Overall aggregate row
    if all_kappas:
        export.append({
            "approach": "Overall",
            "project": "Aggregate",
            "kappa": round(sum(all_kappas) / len(all_kappas), 6),
            "n": sum(r["n"] for r in results if r["kappa"] is not None),
            "pct_above_0.80": round(
                100.0 * sum(1 for k in all_kappas if k > 0.80) / len(all_kappas), 1
            ),
        })

    write_csv(csv_path, ["approach", "project", "kappa", "n", "pct_above_0.80"], export)
    print(f"\nResults written to: {csv_path.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()