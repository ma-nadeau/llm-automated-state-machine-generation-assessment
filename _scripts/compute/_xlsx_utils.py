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
