#!/usr/bin/env python3
"""Summarize the experiment data for the paper RQs.

This script is intentionally dependency-free so it can run in a clean Python
environment. It reads the xlsx workbooks directly as zipped XML files and emits
Markdown tables for the three paper-facing experiment groups:

* RQ1: human assessment of Claude-generated state machines.
* RQ2: human-vs-LLM grading quality on Claude-generated state machines.
* RQ3: grader behavior consistency across Claude/GPT/Gemini-generated state machines.
"""

from __future__ import annotations

import argparse
import csv
import re
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


BASE_DIR = Path(__file__).resolve().parent.parent
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
SCORES = (0.0, 0.5, 1.0)
TYPES = (
    "Composite State",
    "State",
    "Transition",
    "Action",
    "Region",
    "History State",
    "Guard",
    "Overall Score",
)
RQ3_GENERATORS = {"Claude4.5Sonnet", "GPT-5.5", "Gemini3.1ProPreview"}
RQ3_BASELINE_GENERATOR = "Claude4.5Sonnet"
RQ3_COMPARISON_GENERATORS = ("GPT-5.5", "Gemini3.1ProPreview")


@dataclass(frozen=True)
class MetricRow:
    approach: str
    project: str
    model_element: str
    precision: float | None
    recall: float | None
    f1: float | None


@dataclass(frozen=True)
class GradeRow:
    project: str
    model_element: str
    human: float
    llm: float
    is_additional: bool


def _shared_strings(zf: zipfile.ZipFile) -> list[str]:
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    values = []
    for si in root.findall("m:si", NS):
        values.append("".join(t.text or "" for t in si.findall(".//m:t", NS)))
    return values


def _col_index(cell_ref: str) -> int:
    letters = re.match(r"([A-Z]+)", cell_ref).group(1)
    idx = 0
    for char in letters:
        idx = idx * 26 + ord(char) - ord("A") + 1
    return idx - 1


def _workbook_sheets(zf: zipfile.ZipFile) -> dict[str, str]:
    root = ET.fromstring(zf.read("xl/workbook.xml"))
    sheets = {}
    for sheet in root.findall(".//m:sheet", NS):
        name = sheet.attrib["name"]
        sheet_id = sheet.attrib["sheetId"]
        sheets[name] = f"xl/worksheets/sheet{sheet_id}.xml"
    return sheets


def _sheet_rows(path: Path, sheet_match: str) -> list[list[str]]:
    with zipfile.ZipFile(path) as zf:
        strings = _shared_strings(zf)
        sheets = _workbook_sheets(zf)
        sheet_name = next(name for name in sheets if sheet_match.lower() in name.lower())
        root = ET.fromstring(zf.read(sheets[sheet_name]))

        rows = []
        for row in root.findall(".//m:sheetData/m:row", NS):
            values = []
            for cell in row.findall("m:c", NS):
                idx = _col_index(cell.attrib["r"])
                while len(values) <= idx:
                    values.append("")
                value_node = cell.find("m:v", NS)
                value = "" if value_node is None else value_node.text or ""
                if cell.attrib.get("t") == "s" and value:
                    value = strings[int(value)]
                values[idx] = value
            rows.append(values)
        return rows


def _as_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _project_from_path(path: Path) -> str:
    parts = path.parts
    return parts[parts.index("Grading") - 1]


def _approach_from_path(path: Path) -> str:
    parts = path.parts
    stage = parts[parts.index("Grading") + 1]
    examples = parts[parts.index("Grading") + 2]
    if stage == "1 stage":
        return "one-stage"
    if examples == "6-examples":
        return "two-stage (6 examples)"
    return "two-stage (3 examples)"


def _grader_from_filename(path: Path) -> str:
    match = re.search(r"CombinedHumanGradingVs(.+?)AutoGrading", path.name)
    return match.group(1) if match else "Unknown"


def _generator_from_tsv(path: Path) -> str:
    match = re.search(r"generated-by-(.+?)__graded-by-", path.name)
    return match.group(1) if match else "Unknown"


def _grader_from_tsv(path: Path) -> str:
    match = re.search(r"__graded-by-(.+?)\.tsv", path.name)
    return match.group(1) if match else "Unknown"


def _canonical_model_name(name: str) -> str:
    names = {
        "claude-4.5-sonnet": "Claude4.5Sonnet",
        "Claude 4.5 Sonnet": "Claude4.5Sonnet",
        "GPT-5.5": "GPT-5.5",
        "gemini-3.1-pro-preview": "Gemini3.1ProPreview",
    }
    return names.get(name, name)


def _avg(values: list[float | None]) -> float | None:
    present = [v for v in values if v is not None]
    return sum(present) / len(present) if present else None


def _fmt(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.3f}"


def _table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |"]
    out.append("| " + " | ".join("---" for _ in headers) + " |")
    out.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(out)


def _write_csv(path: Path, headers: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in headers})


def load_human_metric_rows(root: Path) -> list[MetricRow]:
    files = sorted(
        root.glob("*/Grading/*/*/*HumanGrading_Claude4.5SonnetGeneration.xlsx")
    )
    rows: list[MetricRow] = []
    for path in files:
        metrics = _sheet_rows(path, "Metrics")
        in_human_block = False
        for row in metrics:
            label = row[0].strip() if row else ""
            if label.endswith("Human") or "Grader #1" in label:
                in_human_block = True
                continue
            if in_human_block and label.startswith("Claude Grader") and "Human" not in label:
                break
            if in_human_block and label in TYPES:
                rows.append(
                    MetricRow(
                        approach=_approach_from_path(path),
                        project=_project_from_path(path),
                        model_element=label.replace("Composite state", "Composite State"),
                        precision=_as_float(row[5]) if len(row) > 5 else None,
                        recall=_as_float(row[6]) if len(row) > 6 else None,
                        f1=_as_float(row[7]) if len(row) > 7 else None,
                    )
                )
    return rows


def load_grade_rows(path: Path) -> list[GradeRow]:
    rows = []
    for row in _sheet_rows(path, "Weighted Cohens Kappa")[1:]:
        if len(row) < 4 or not row[0] or not row[1]:
            break
        human = _as_float(row[2])
        llm = _as_float(row[3])
        if human is None or llm is None:
            continue
        rows.append(
            GradeRow(
                project=_project_from_path(path),
                model_element=row[0].strip().replace("Composite state", "Composite State"),
                human=human,
                llm=llm,
                is_additional=row[1].strip().lower() == "additional elements",
            )
        )
    return rows


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


def prf_from_confusion(matrix: dict[float, Counter[float]]) -> tuple[float, float, float, float]:
    per_label = []
    total = sum(matrix[h][p] for h in SCORES for p in SCORES)
    agree = sum(matrix[s][s] for s in SCORES)
    for score in SCORES:
        tp = matrix[score][score]
        predicted = sum(matrix[h][score] for h in SCORES)
        actual = sum(matrix[score][p] for p in SCORES)
        precision = tp / predicted if predicted else None
        recall = tp / actual if actual else None
        if precision is None or recall is None or precision + recall == 0:
            f1 = None
        else:
            f1 = 2 * precision * recall / (precision + recall)
        per_label.append((precision, recall, f1))
    return (
        agree / total if total else 0.0,
        _avg([x[0] for x in per_label]) or 0.0,
        _avg([x[1] for x in per_label]) or 0.0,
        _avg([x[2] for x in per_label]) or 0.0,
    )


def score_distribution(tsv_files: list[Path]) -> dict[tuple[str, str, str], Counter[float]]:
    dist: dict[tuple[str, str, str], Counter[float]] = defaultdict(Counter)
    for path in tsv_files:
        generator = _canonical_model_name(_generator_from_tsv(path))
        grader = _canonical_model_name(_grader_from_tsv(path))
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row in reader:
                model_element = (row.get("Type") or row.get("type") or "").strip()
                grade = _as_float((row.get("Grading") or row.get("grading") or "").strip())
                if model_element and grade in SCORES:
                    dist[(generator, grader, model_element)][grade] += 1
                    dist[(generator, grader, "Overall Score")][grade] += 1
    return dist


def rq1(root: Path) -> str:
    table_rows = []
    for row in summarize_rq1(root):
        table_rows.append(
            [
                str(row["approach"]),
                str(row["model_element"]),
                str(row["examples"]),
                _fmt(row["precision"]),
                _fmt(row["recall"]),
                _fmt(row["f1"]),
            ]
        )
    return _table(["Approach", "Model element", "Examples", "Precision", "Recall", "F1"], table_rows)


def summarize_rq1(root: Path) -> list[dict[str, object]]:
    metric_rows = load_human_metric_rows(root)
    grouped: dict[tuple[str, str], list[MetricRow]] = defaultdict(list)
    for row in metric_rows:
        grouped[(row.approach, row.model_element)].append(row)

    rows = []
    for approach in ("one-stage", "two-stage (6 examples)"):
        for model_element in TYPES:
            values = grouped.get((approach, model_element), [])
            if not values:
                continue
            rows.append(
                {
                    "approach": approach,
                    "model_element": model_element,
                    "examples": len({v.project for v in values}),
                    "precision": _avg([v.precision for v in values]),
                    "recall": _avg([v.recall for v in values]),
                    "f1": _avg([v.f1 for v in values]),
                }
            )
    return rows


def rq2(root: Path) -> str:
    table_rows = []
    for row in summarize_rq2(root):
        table_rows.append(
            [
                str(row["grader"]),
                str(row["model_element"]),
                str(row["items"]),
                _fmt(row["exact_agreement"]),
                _fmt(row["macro_precision"]),
                _fmt(row["macro_recall"]),
                _fmt(row["macro_f1"]),
            ]
        )
    return _table(
        ["Grader", "Model element", "Items", "Exact agreement", "Macro P", "Macro R", "Macro F1"],
        table_rows,
    )


def _rq2_grouped(root: Path) -> dict[tuple[str, str], list[GradeRow]]:
    files = sorted(
        root.glob(
            "*/Grading/2 stage/6-examples/*CombinedHumanGradingVs*AutoGrading_Claude4.5SonnetGeneration.xlsx"
        )
    )
    grouped: dict[tuple[str, str], list[GradeRow]] = defaultdict(list)
    for path in files:
        grader = _grader_from_filename(path)
        for row in load_grade_rows(path):
            grouped[(grader, "Overall Score")].append(row)
            grouped[(grader, row.model_element)].append(row)
    return grouped


def summarize_rq2(root: Path) -> list[dict[str, object]]:
    grouped = _rq2_grouped(root)
    rows = []
    for grader in sorted({key[0] for key in grouped}):
        for model_element in TYPES:
            values = grouped.get((grader, model_element), [])
            if not values:
                continue
            exact, precision, recall, f1 = prf_from_confusion(confusion(values))
            rows.append(
                {
                    "grader": grader,
                    "model_element": model_element,
                    "items": len(values),
                    "exact_agreement": exact,
                    "macro_precision": precision,
                    "macro_recall": recall,
                    "macro_f1": f1,
                }
            )
    return rows


def summarize_rq2_confusions(root: Path) -> list[dict[str, object]]:
    grouped = _rq2_grouped(root)
    rows = []
    for (grader, model_element), values in sorted(grouped.items()):
        matrix = confusion(values)
        for human_score in SCORES:
            for llm_score in SCORES:
                rows.append(
                    {
                        "grader": grader,
                        "model_element": model_element,
                        "human_score": human_score,
                        "llm_score": llm_score,
                        "count": matrix[human_score][llm_score],
                    }
                )
    return rows


def rq2_confusions(root: Path) -> str:
    files = sorted(
        root.glob(
            "*/Grading/2 stage/6-examples/*CombinedHumanGradingVs*AutoGrading_Claude4.5SonnetGeneration.xlsx"
        )
    )
    grouped: dict[str, list[GradeRow]] = defaultdict(list)
    for path in files:
        grouped[_grader_from_filename(path)].extend(load_grade_rows(path))

    blocks = []
    for grader in sorted(grouped):
        matrix = confusion(grouped[grader])
        table_rows = [
            [str(h), str(matrix[h][0.0]), str(matrix[h][0.5]), str(matrix[h][1.0])]
            for h in SCORES
        ]
        blocks.append(f"**{grader}**\n\n" + _table(["Human \\ LLM", "0", "0.5", "1"], table_rows))
    return "\n\n".join(blocks)


def rq3(root: Path) -> str:
    distribution_rows = []
    for row in summarize_rq3(root):
        distribution_rows.append(
            [
                str(row["generator"]),
                str(row["grader"]),
                str(row["model_element"]),
                str(row["items"]),
                _fmt(row["score_0_pct"]),
                _fmt(row["score_0_5_pct"]),
                _fmt(row["score_1_pct"]),
            ]
        )

    stability_rows = []
    for row in summarize_rq3_per_grader_stability(root):
        if row["model_element"] != "Overall Score":
            continue
        stability_rows.append(
            [
                str(row["grader"]),
                str(row["comparison_generator"]),
                _fmt(row["baseline_score_1_pct"]),
                _fmt(row["comparison_score_1_pct"]),
                _fmt(row["delta_score_1_pct"]),
                _fmt(row["baseline_score_0_5_pct"]),
                _fmt(row["comparison_score_0_5_pct"]),
                _fmt(row["delta_score_0_5_pct"]),
            ]
        )

    ranking_rows = []
    for row in summarize_rq3_cross_grader_rankings(root):
        if row["model_element"] != "Overall Score":
            continue
        ranking_rows.append(
            [
                str(row["generator"]),
                str(row["grader"]),
                _fmt(row["score_1_pct"]),
                str(row["rank_by_score_1"]),
            ]
        )

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
            _table(
                [
                    "Generator",
                    "Grader",
                    "Model element",
                    "Items",
                    "Score 0",
                    "Score 0.5",
                    "Score 1",
                ],
                distribution_rows,
            ),
            "**Per-grader stability (Overall Score)**",
            _table(
                [
                    "Grader",
                    "Comparison generator",
                    "Baseline %1",
                    "Comparison %1",
                    "Delta %1",
                    "Baseline %0.5",
                    "Comparison %0.5",
                    "Delta %0.5",
                ],
                stability_rows,
            ),
            "**Cross-grader rankings by %1 (Overall Score)**",
            _table(["Generator", "Grader", "Score 1", "Rank"], ranking_rows),
        ]
    )


def _rq3_files(root: Path) -> list[Path]:
    files = sorted(
        root.glob(
            "*/Grading/2 stage/6-examples/Generated Files/grading_results__generated-by-*__graded-by-*.tsv"
        )
    )
    return [
        p
        for p in files
        if _canonical_model_name(_generator_from_tsv(p)) in RQ3_GENERATORS
    ]


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
        (str(row["generator"]), str(row["grader"]), str(row["model_element"])): row
        for row in summarize_rq3(root)
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
                        "delta_score_0_5_pct": comparison["score_0_5_pct"]
                        - baseline["score_0_5_pct"],
                        "delta_score_1_pct": comparison["score_1_pct"] - baseline["score_1_pct"],
                    }
                )
    return rows


def summarize_rq3_cross_grader_rankings(root: Path) -> list[dict[str, object]]:
    lookup = _rq3_lookup(root)
    rows = []
    for generator in sorted({generator for generator, _, _ in lookup}):
        for model_element in TYPES:
            candidates = [
                row
                for (row_generator, _, row_model_element), row in lookup.items()
                if row_generator == generator and row_model_element == model_element
            ]
            candidates.sort(key=lambda row: (-row["score_1_pct"], str(row["grader"])))
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


def data_availability(root: Path) -> list[dict[str, object]]:
    counts: Counter[tuple[str, str, str]] = Counter()
    for path in root.glob(
        "*/Grading/2 stage/6-examples/*CombinedHumanGradingVs*AutoGrading_Claude4.5SonnetGeneration.xlsx"
    ):
        counts[("Claude4.5Sonnet", _canonical_model_name(_grader_from_filename(path)), "human-vs-llm xlsx")] += 1
    for path in root.glob("*/Grading/2 stage/6-examples/Generated Files/grading_results__generated-by-*__graded-by-*.tsv"):
        counts[(_canonical_model_name(_generator_from_tsv(path)), _canonical_model_name(_grader_from_tsv(path)), "llm-grading tsv")] += 1
    return [
        {
            "generator": generator,
            "grader": grader,
            "data_kind": data_kind,
            "file_count": count,
        }
        for (generator, grader, data_kind), count in sorted(counts.items())
    ]


def write_outputs(root: Path, out_dir: Path) -> None:
    rq1_rows = summarize_rq1(root)
    _write_csv(
        out_dir / "rq1_generation_quality_summary.csv",
        ["approach", "model_element", "examples", "precision", "recall", "f1"],
        rq1_rows,
    )
    metric_rows = load_human_metric_rows(root)
    _write_csv(
        out_dir / "rq1_generation_quality_by_example.csv",
        ["approach", "project", "model_element", "precision", "recall", "f1"],
        [
            {
                "approach": row.approach,
                "project": row.project,
                "model_element": row.model_element,
                "precision": row.precision,
                "recall": row.recall,
                "f1": row.f1,
            }
            for row in metric_rows
        ],
    )

    _write_csv(
        out_dir / "rq2_grading_quality_summary.csv",
        [
            "grader",
            "model_element",
            "items",
            "exact_agreement",
            "macro_precision",
            "macro_recall",
            "macro_f1",
        ],
        summarize_rq2(root),
    )
    _write_csv(
        out_dir / "rq2_confusion_matrices.csv",
        ["grader", "model_element", "human_score", "llm_score", "count"],
        summarize_rq2_confusions(root),
    )
    _write_csv(
        out_dir / "rq3_grading_score_distribution.csv",
        [
            "generator",
            "grader",
            "model_element",
            "items",
            "score_0_count",
            "score_0_5_count",
            "score_1_count",
            "score_0_pct",
            "score_0_5_pct",
            "score_1_pct",
        ],
        summarize_rq3(root),
    )
    _write_csv(
        out_dir / "rq3_per_grader_stability.csv",
        [
            "grader",
            "model_element",
            "baseline_generator",
            "comparison_generator",
            "baseline_score_0_pct",
            "baseline_score_0_5_pct",
            "baseline_score_1_pct",
            "comparison_score_0_pct",
            "comparison_score_0_5_pct",
            "comparison_score_1_pct",
            "delta_score_0_pct",
            "delta_score_0_5_pct",
            "delta_score_1_pct",
        ],
        summarize_rq3_per_grader_stability(root),
    )
    _write_csv(
        out_dir / "rq3_cross_grader_rankings.csv",
        ["generator", "model_element", "grader", "score_1_pct", "rank_by_score_1"],
        summarize_rq3_cross_grader_rankings(root),
    )
    _write_csv(
        out_dir / "data_availability.csv",
        ["generator", "grader", "data_kind", "file_count"],
        data_availability(root),
    )

    summary = "\n".join(
        [
            "# Paper Experiment Summary",
            "",
            "## RQ1: Claude Generation Quality From Human Assessment",
            "",
            rq1(root),
            "",
            "## RQ2: LLM Grading Quality Against Human Assessment",
            "",
            rq2(root),
            "",
            "## RQ2: Overall Confusion Matrices",
            "",
            rq2_confusions(root),
            "",
            "## RQ3: Grader Behavior Consistency Across Generated Inputs",
            "",
            rq3(root),
            "",
        ]
    )
    (out_dir / "paper_experiment_summary.md").write_text(summary, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=BASE_DIR)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Write figure-ready CSVs and a Markdown summary to this directory.",
    )
    args = parser.parse_args()

    if args.out_dir is not None:
        write_outputs(args.root, args.out_dir)
        print(f"Wrote consolidated experiment data to {args.out_dir}")
        return

    print("# Paper Experiment Summary\n")
    print("## RQ1: Claude Generation Quality From Human Assessment\n")
    print(rq1(args.root))
    print("\n## RQ2: LLM Grading Quality Against Human Assessment\n")
    print(rq2(args.root))
    print("\n## RQ2: Overall Confusion Matrices\n")
    print(rq2_confusions(args.root))
    print("\n## RQ3: Grader Behavior Consistency Across Generated Inputs\n")
    print(rq3(args.root))


if __name__ == "__main__":
    main()
