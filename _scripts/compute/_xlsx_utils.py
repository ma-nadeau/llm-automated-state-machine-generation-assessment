"""
Shared constants, dataclasses, and low-level xlsx/TSV utilities used by all
compute_rq*.py scripts.  Not intended to be run directly.

Reads xlsx workbooks as zipped XML files (no openpyxl / pandas dependency).
"""

from __future__ import annotations

import csv
import re
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Iterator
from xml.etree import ElementTree as ET

if TYPE_CHECKING:
    from collections.abc import Iterable

# _scripts/compute/ -> _scripts/ -> Evaluations/
BASE_DIR = Path(__file__).resolve().parent.parent.parent

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

SCORES = (0.0, 0.5, 1.0)

TYPE_ALIASES: dict[str, str] = {
    "action": "Action",
    "composite state": "Composite State",
    "composite states": "Composite State",
    "guard": "Guard",
    "history state": "History State",
    "history states": "History State",
    "region": "Region",
    "state": "State",
    "states": "State",
    "transition": "Transition",
    "transitions": "Transition",
}

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


# ── Dataclasses ───────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class MetricRow:
    approach: str
    project: str
    model_element: str
    n: float | None
    tp: float | None
    fp: float | None
    fn: float | None
    s: float | None = None  # weighted TP (sum of scores); None = not computed


@dataclass(frozen=True)
class GradeRow:
    project: str
    model_element: str
    human: float
    llm: float
    is_additional: bool


# ── xlsx XML readers ──────────────────────────────────────────────────────────

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


def iter_xlsx(paths: "Iterable[Path]") -> "Iterator[Path]":
    """Yield paths that are real xlsx files, skipping Excel lock files (~$…)."""
    for p in paths:
        if not p.name.startswith("~$"):
            yield p


def sheet_rows(path: Path, sheet_match: str) -> list[list[str]]:
    """Return all rows from the first sheet whose name contains sheet_match."""
    with zipfile.ZipFile(path) as zf:
        strings = _shared_strings(zf)
        sheets = _workbook_sheets(zf)
        sheet_name = next(
            name for name in sheets if sheet_match.lower() in name.lower()
        )
        root = ET.fromstring(zf.read(sheets[sheet_name]))
        rows = []
        for row in root.findall(".//m:sheetData/m:row", NS):
            values: list[str] = []
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


def sheet_rows_by_index(path: Path, index: int) -> list[list[str]]:
    """Return all rows from the sheet at the given 0-based index."""
    with zipfile.ZipFile(path) as zf:
        strings = _shared_strings(zf)
        sheets = _workbook_sheets(zf)
        sheet_name = list(sheets.keys())[index]
        root = ET.fromstring(zf.read(sheets[sheet_name]))
        rows: list[list[str]] = []
        for row in root.findall(".//m:sheetData/m:row", NS):
            values: list[str] = []
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


def _is_additional_row(elem_val: str) -> bool:
    return "additional element" in elem_val.strip().lower()


def parse_raw_grading_sheet(
    path: Path, sheet_index: int
) -> dict[str, dict[str, float]]:
    """
    Parse a raw Human or LLM grading sheet (col A=type, B=element, C=score, D=note).

    Dynamically splits rows into expected vs. additional (FP) by detecting the first
    row where col B contains "additional element".

    Returns dict: norm_type -> {"S", "TP", "FN", "FP", "N"}
      S  = sum of scores for expected elements (weighted TP)
      TP = count of expected elements with score > 0 (binary)
      FN = count of expected elements with score == 0
      FP = sum of col-C integer counts from additional rows (0, 1, 2, …)
      N  = TP + FN = total expected elements
    """
    rows = sheet_rows_by_index(path, sheet_index)

    # Row 0 is the header; find split starting from row 1.
    split_idx: int | None = None
    for i, row in enumerate(rows):
        if i == 0:
            continue
        elem = row[1] if len(row) > 1 else ""
        if _is_additional_row(elem):
            split_idx = i
            break

    expected = rows[1:split_idx] if split_idx is not None else rows[1:]
    additional = rows[split_idx:] if split_idx is not None else []

    result: dict[str, dict[str, float]] = {}

    for row in expected:
        t_val = row[0] if row else ""
        s_val = row[2] if len(row) > 2 else ""
        norm = TYPE_ALIASES.get(t_val.strip().lower() if t_val else "")
        if norm is None:
            continue
        score = as_float(s_val) or 0.0
        if norm not in result:
            result[norm] = {"S": 0.0, "TP": 0.0, "FN": 0.0, "FP": 0.0, "N": 0.0}
        result[norm]["S"] += score
        result[norm]["N"] += 1.0
        if score > 0:
            result[norm]["TP"] += 1.0
        else:
            result[norm]["FN"] += 1.0

    for row in additional:
        t_val = row[0] if row else ""
        s_val = row[2] if len(row) > 2 else ""
        norm = TYPE_ALIASES.get(t_val.strip().lower() if t_val else "")
        if norm is None:
            continue
        if norm not in result:
            result[norm] = {"S": 0.0, "TP": 0.0, "FN": 0.0, "FP": 0.0, "N": 0.0}
        result[norm]["FP"] += as_float(s_val) or 0.0

    return result


# ── Path helpers ──────────────────────────────────────────────────────────────

def project_from_path(path: Path) -> str:
    parts = path.parts
    return parts[parts.index("Grading") - 1]


def approach_from_path(path: Path) -> str:
    parts = path.parts
    stage = parts[parts.index("Grading") + 1]
    examples = parts[parts.index("Grading") + 2]
    if stage == "1 stage":
        return "one-stage"
    if examples == "6-examples":
        return "two-stage (6 examples)"
    return "two-stage (3 examples)"


def grader_from_filename(path: Path) -> str:
    match = re.search(r"CombinedHumanGradingVs(.+?)AutoGrading", path.name)
    return match.group(1) if match else "Unknown"


def stage_shot_from_path(path: Path) -> tuple[str, str]:
    """Return (stage, shot) from path: …/Grading/2 stage/6-examples/… → ("2", "6-examples")."""
    parts = path.parts
    idx = parts.index("Grading")
    stage = parts[idx + 1].split()[0]
    shot = parts[idx + 2]
    return stage, shot


def generator_from_tsv(path: Path) -> str:
    match = re.search(r"generated-by-(.+?)__graded-by-", path.name)
    return match.group(1) if match else "Unknown"


def grader_from_tsv(path: Path) -> str:
    match = re.search(r"__graded-by-(.+?)\.tsv", path.name)
    return match.group(1) if match else "Unknown"


def canonical_model_name(name: str) -> str:
    names = {
        "claude-4.5-sonnet": "Claude4.5Sonnet",
        "Claude 4.5 Sonnet": "Claude4.5Sonnet",
        "GPT-5.5": "GPT-5.5",
        "gemini-3.1-pro-preview": "Gemini3.1ProPreview",
    }
    return names.get(name, name)


# ── Numeric helpers ───────────────────────────────────────────────────────────

def as_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def avg(values: list[float | None]) -> float | None:
    present = [v for v in values if v is not None]
    return sum(present) / len(present) if present else None


# ── Markdown / formatting helpers ─────────────────────────────────────────────

def fmt(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.3f}"


def _md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(_md_cell(h) for h in headers) + " |"]
    out.append("| " + " | ".join("---" for _ in headers) + " |")
    out.extend("| " + " | ".join(_md_cell(c) for c in row) + " |" for row in rows)
    return "\n".join(out)


# ── CSV writer ────────────────────────────────────────────────────────────────

def write_csv(path: Path, headers: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({h: row.get(h, "") for h in headers})
