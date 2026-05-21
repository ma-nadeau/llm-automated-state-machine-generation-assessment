#!/usr/bin/env python3
"""
RQ2: Human-vs-LLM grading quality on Claude-generated state machines.

Reads the Weighted Cohens Kappa sheet of every 2-stage/6-examples
CombinedHumanGradingVs*AutoGrading*.xlsx workbook and builds
per-file confusion matrix counts.

Output (written to _Figures/data/rq2/):
  rq2_confusion_matrices.csv  — raw confusion counts (human_score × llm_score)

Usage:
  python compute_rq2_grading_quality.py                         # writes CSVs to default out-dir
  python compute_rq2_grading_quality.py --out-dir /custom/path  # override output directory
  python compute_rq2_grading_quality.py --print                 # print Markdown tables to stdout only
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path

from _xlsx_utils import (
    BASE_DIR,
    SCORES,
    GradeRow,
    as_float,
    grader_from_filename,
    md_table,
    project_from_path,
    sheet_rows,
    stage_shot_from_path,
    write_csv,
)

DEFAULT_OUT_DIR = BASE_DIR / "_Figures" / "data" / "rq2"


# ── Grade loading ─────────────────────────────────────────────────────────────


def load_grade_rows(path: Path) -> list[GradeRow]:
    rows = []
    for row in sheet_rows(path, "Weighted Cohens Kappa")[1:]:
        if len(row) < 4 or not row[0] or not row[1]:
            break
        human = as_float(row[2])
        llm = as_float(row[3])
        if human is None or llm is None:
            continue
        rows.append(
            GradeRow(
                project=project_from_path(path),
                model_element=row[0]
                .strip()
                .replace("Composite state", "Composite State"),
                human=human,
                llm=llm,
                is_additional=row[1].strip().lower() == "additional elements",
            )
        )
    return rows


# ── Confusion matrix ──────────────────────────────────────────────────────────


def confusion(rows: list[GradeRow]) -> dict[float, Counter[float]]:
    matrix: dict[float, Counter[float]] = {score: Counter() for score in SCORES}
    for row in rows:
        if not row.is_additional:
            matrix[row.human][row.llm] += 1
            continue
        human_count = int(row.human)
        llm_count = int(row.llm)
        if human_count == 0 and llm_count == 0:
            matrix[0.0][0.0] += 1
        else:
            matrix[1.0][1.0] += min(human_count, llm_count)
            matrix[0.0][1.0] += max(llm_count - human_count, 0)
            matrix[1.0][0.0] += max(human_count - llm_count, 0)
    return matrix


# ── Summarize functions ───────────────────────────────────────────────────────


def _rq2_files(root: Path) -> list[Path]:
    return sorted(
        root.glob(
            "*/Grading/2 stage/6-examples/*CombinedHumanGradingVs*AutoGrading_Claude4.5SonnetGeneration.xlsx"
        )
    )


def summarize_rq2_confusions(root: Path) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str, str], list[GradeRow]] = defaultdict(list)
    for path in _rq2_files(root):
        grader = grader_from_filename(path)
        stage, shot = stage_shot_from_path(path)
        for row in load_grade_rows(path):
            grouped[(grader, stage, shot, "Overall Score")].append(row)
            grouped[(grader, stage, shot, row.model_element)].append(row)

    rows = []
    for (grader, stage, shot, model_element), values in sorted(grouped.items()):
        matrix = confusion(values)
        for human_score in SCORES:
            for llm_score in SCORES:
                rows.append(
                    {
                        "grader": grader,
                        "stage": stage,
                        "shot": shot,
                        "model_element": model_element,
                        "human_score": human_score,
                        "llm_score": llm_score,
                        "count": matrix[human_score][llm_score],
                    }
                )
    return rows


# ── Markdown ──────────────────────────────────────────────────────────────────


def rq2_confusions_markdown(root: Path) -> str:
    grouped: dict[str, list[GradeRow]] = defaultdict(list)
    for path in _rq2_files(root):
        grouped[grader_from_filename(path)].extend(load_grade_rows(path))
    blocks = []
    for grader in sorted(grouped):
        matrix = confusion(grouped[grader])
        table_rows = [
            [str(h), str(matrix[h][0.0]), str(matrix[h][0.5]), str(matrix[h][1.0])]
            for h in SCORES
        ]
        blocks.append(
            f"**{grader}**\n\n"
            + md_table(["Human \\ LLM", "0", "0.5", "1"], table_rows)
        )
    return "\n\n".join(blocks)


# ── Write ─────────────────────────────────────────────────────────────────────


def write_rq2(root: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        out_dir / "rq2_confusion_matrices.csv",
        [
            "grader",
            "stage",
            "shot",
            "model_element",
            "human_score",
            "llm_score",
            "count",
        ],
        summarize_rq2_confusions(root),
    )
    print(f"RQ2 CSVs written to: {out_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize RQ2 grading quality.")
    parser.add_argument("--root", type=Path, default=BASE_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument(
        "--print", action="store_true", help="Print Markdown tables to stdout."
    )
    args = parser.parse_args()

    if args.print:
        print("## RQ2: Overall Confusion Matrices\n")
        print(rq2_confusions_markdown(args.root))
    else:
        write_rq2(args.root, args.out_dir)


if __name__ == "__main__":
    main()
