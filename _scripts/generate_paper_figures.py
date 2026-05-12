#!/usr/bin/env python3
"""Generate publication-ready SVG figures from consolidated experiment CSVs.

The script is dependency-free on purpose. It reads the CSV files produced by
summarize_paper_experiments.py and writes vector SVG figures that can be used
directly in the paper or converted to PDF/PNG by the writing toolchain.
"""

from __future__ import annotations

import argparse
import csv
import html
import math
import shutil
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "_Figures" / "PaperExperimentData"
OUT_DIR = BASE_DIR / "_Figures" / "PaperFigures"

MODEL_ELEMENTS = [
    "Overall Score",
    "State",
    "Transition",
    "Action",
    "Guard",
    "Composite State",
    "History State",
    "Region",
]

MODEL_ELEMENT_LABELS = {
    "Overall Score": "Overall",
    "Composite State": "Composite",
    "History State": "History",
}

GRADERS = ["Claude4.5Sonnet", "GPT-5.5", "Gemini3.1ProPreview"]
GRADER_LABELS = {
    "Claude4.5Sonnet": "Claude 4.5 Sonnet",
    "GPT-5.5": "GPT-5.5",
    "Gemini3.1ProPreview": "Gemini 3.1 Pro Preview",
}

PALETTE = {
    "ink": "#17212b",
    "muted": "#667085",
    "grid": "#e5e7eb",
    "paper": "#fbfcfe",
    "panel": "#ffffff",
    "axis": "#d0d5dd",
    "one": "#4f46e5",
    "two": "#059669",
    "claude": "#6d5dfc",
    "gpt": "#0f9f8f",
    "gemini": "#e46b38",
    "zero": "#d4515c",
    "half": "#d6a12a",
    "one_score": "#2f9e66",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def f(value: str | float | int | None) -> float:
    if value in (None, ""):
        return float("nan")
    return float(value)


def pct(value: float) -> str:
    return f"{value * 100:.0f}%"


def label_element(value: str) -> str:
    return MODEL_ELEMENT_LABELS.get(value, value)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


class Svg:
    def __init__(self, width: int, height: int, title: str):
        self.width = width
        self.height = height
        self.parts: list[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">',
            "<defs>",
            '<filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">',
            '<feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#101828" flood-opacity="0.12"/>',
            "</filter>",
            '<linearGradient id="headerFade" x1="0" y1="0" x2="1" y2="0">',
            '<stop offset="0%" stop-color="#f7f8ff"/>',
            '<stop offset="100%" stop-color="#f2fbf8"/>',
            "</linearGradient>",
            "</defs>",
            f'<rect width="{width}" height="{height}" fill="{PALETTE["paper"]}"/>',
            '<style>text{font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;} .title{font-size:28px;font-weight:800;fill:#17212b;} .subtitle{font-size:15px;fill:#667085;} .label{font-size:15px;fill:#344054;} .small{font-size:13px;fill:#667085;} .tiny{font-size:11px;fill:#667085;} .num{font-size:13px;font-weight:700;fill:#17212b;} .axis{stroke:#d0d5dd;stroke-width:1;} .grid{stroke:#e5e7eb;stroke-width:1;} .panelTitle{font-size:17px;font-weight:750;fill:#17212b;} .legend{font-size:14px;fill:#344054;}</style>',
        ]

    def rect(self, x, y, w, h, fill, stroke="none", rx=0, opacity=1, extra=""):
        self.parts.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx:.2f}" fill="{fill}" stroke="{stroke}" opacity="{opacity}" {extra}/>'
        )

    def line(self, x1, y1, x2, y2, stroke, width=1, opacity=1, dash=None):
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}"{dash_attr}/>'
        )

    def text(self, x, y, text, cls="label", anchor="start", weight=None, fill=None, size=None):
        attrs = [f'x="{x:.2f}"', f'y="{y:.2f}"', f'class="{cls}"', f'text-anchor="{anchor}"']
        if weight:
            attrs.append(f'font-weight="{weight}"')
        if fill:
            attrs.append(f'fill="{fill}"')
        if size:
            attrs.append(f'font-size="{size}"')
        self.parts.append(f'<text {" ".join(attrs)}>{esc(text)}</text>')

    def circle(self, cx, cy, r, fill, stroke="white", width=2, opacity=1):
        self.parts.append(
            f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}"/>'
        )

    def path(self, d, fill="none", stroke="#000", width=1, opacity=1):
        self.parts.append(
            f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}" stroke-linecap="round" stroke-linejoin="round"/>'
        )

    def save(self, path: Path):
        self.parts.append("</svg>")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(self.parts), encoding="utf-8")


def header(svg: Svg, title: str, subtitle: str):
    svg.text(58, 48, title, cls="title")
    svg.text(58, 75, subtitle, cls="subtitle")


def legend(svg: Svg, items: list[tuple[str, str]], x: float, y: float):
    cx = x
    for label, color in items:
        svg.rect(cx, y - 11, 20, 12, color, rx=6)
        svg.text(cx + 28, y, label, cls="legend")
        cx += 28 + max(95, len(label) * 7.4)


def nice_ticks(min_v=0.0, max_v=1.0, count=5):
    return [min_v + (max_v - min_v) * i / (count - 1) for i in range(count)]


def fig_rq1(data_dir: Path, out_dir: Path):
    rows = read_csv(data_dir / "rq1_generation_quality_summary.csv")
    by_key = {(r["approach"], r["model_element"]): r for r in rows}

    svg = Svg(1680, 980, "RQ1 generation quality")
    header(
        svg,
        "RQ1 - Claude generation quality from human assessment",
        "Precision, recall, and F1 averaged across state-machine examples; one-stage baseline vs two-stage prompting.",
    )
    legend(svg, [("One-stage", PALETTE["one"]), ("Two-stage", PALETTE["two"])], 58, 112)

    metrics = [("precision", "Precision"), ("recall", "Recall"), ("f1", "F1")]
    left = 82
    top = 150
    panel_w = 470
    panel_h = 650
    gap = 34
    plot_pad_l = 116
    plot_pad_r = 26
    plot_pad_t = 30
    plot_pad_b = 70

    for m_idx, (metric, title) in enumerate(metrics):
        x0 = left + m_idx * (panel_w + gap)
        y0 = top
        svg.rect(x0, y0, panel_w, panel_h, PALETTE["panel"], stroke="#e7eaf2", rx=10)
        svg.text(x0 + 28, y0 + 44, title, cls="panelTitle")

        px0 = x0 + plot_pad_l
        px1 = x0 + panel_w - plot_pad_r
        py0 = y0 + plot_pad_t + 38
        py1 = y0 + panel_h - plot_pad_b
        for tick in nice_ticks(0, 1, 6):
            x = px0 + tick * (px1 - px0)
            svg.line(x, py0, x, py1, PALETTE["grid"])
            svg.text(x, py1 + 28, pct(tick), cls="tiny", anchor="middle")

        row_h = (py1 - py0) / len(MODEL_ELEMENTS)
        for idx, element in enumerate(MODEL_ELEMENTS):
            y = py0 + idx * row_h + row_h * 0.52
            if m_idx == 0:
                svg.text(x0 + 28, y + 5, label_element(element), cls="label")
            one = f(by_key.get(("one-stage", element), {}).get(metric, "nan"))
            two = f(by_key.get(("two-stage (6 examples)", element), {}).get(metric, "nan"))
            x_one = px0 + max(0, min(1, one)) * (px1 - px0)
            x_two = px0 + max(0, min(1, two)) * (px1 - px0)
            svg.line(x_one, y, x_two, y, "#aab2c5", width=3, opacity=0.8)
            svg.circle(x_one, y, 8, PALETTE["one"])
            svg.circle(x_two, y, 8, PALETTE["two"])
            if metric == "f1":
                delta = two - one
                svg.text(px1 + 2, y + 5, f"{delta:+.2f}", cls="tiny", fill=PALETTE["two"] if delta >= 0 else PALETTE["zero"])

        svg.text((px0 + px1) / 2, y0 + panel_h - 18, "Score", cls="small", anchor="middle")

    svg.text(1464, 812, "F1 delta", cls="tiny", anchor="middle")
    svg.text(840, 900, "Data: rq1_generation_quality_summary.csv", cls="small", anchor="middle")
    svg.save(out_dir / "fig_rq1_generation_quality.svg")


def fig_rq1_f1_focus(data_dir: Path, out_dir: Path):
    rows = read_csv(data_dir / "rq1_generation_quality_summary.csv")
    by_key = {(r["approach"], r["model_element"]): r for r in rows}
    elements = sorted(
        MODEL_ELEMENTS,
        key=lambda e: f(by_key[("two-stage (6 examples)", e)]["f1"]),
        reverse=True,
    )

    svg = Svg(1400, 760, "RQ1 F1 improvement")
    header(
        svg,
        "RQ1 - Generation quality: F1 by model element",
        "Human assessment of Claude-generated state machines; two-stage prompting improves F1 for most model elements.",
    )
    legend(svg, [("One-stage", PALETTE["one"]), ("Two-stage", PALETTE["two"])], 58, 112)

    left = 220
    right = 1240
    top = 165
    row_h = 62
    for tick in nice_ticks(0.4, 1.0, 7):
        x = left + (tick - 0.4) / 0.6 * (right - left)
        svg.line(x, top - 20, x, top + row_h * len(elements) - 14, PALETTE["grid"])
        svg.text(x, top + row_h * len(elements) + 22, pct(tick), cls="tiny", anchor="middle")
    svg.line(left, top - 20, left, top + row_h * len(elements) - 14, PALETTE["axis"])

    for idx, element in enumerate(elements):
        y = top + idx * row_h
        one = f(by_key[("one-stage", element)]["f1"])
        two = f(by_key[("two-stage (6 examples)", element)]["f1"])
        x_one = left + (one - 0.4) / 0.6 * (right - left)
        x_two = left + (two - 0.4) / 0.6 * (right - left)
        svg.text(58, y + 6, label_element(element), cls="label")
        svg.line(x_one, y, x_two, y, "#b8c0d3", width=4)
        svg.circle(x_one, y, 9, PALETTE["one"])
        svg.circle(x_two, y, 9, PALETTE["two"])
        delta = two - one
        svg.text(right + 28, y + 5, f"{pct(two)}", cls="num")
        svg.text(right + 92, y + 5, f"({delta:+.2f})", cls="tiny", fill=PALETTE["two"] if delta >= 0 else PALETTE["zero"])

    svg.text(right + 28, top - 34, "Two-stage F1", cls="tiny")
    svg.text(right + 92, top - 34, "Delta", cls="tiny")
    svg.text((left + right) / 2, 705, "F1 score", cls="small", anchor="middle")
    svg.text(700, 735, "Data: rq1_generation_quality_summary.csv", cls="small", anchor="middle")
    svg.save(out_dir / "fig_rq1_f1_by_model_element.svg")


def fig_rq2_overall(data_dir: Path, out_dir: Path):
    rows = [
        r
        for r in read_csv(data_dir / "rq2_grading_quality_summary.csv")
        if r["model_element"] == "Overall Score"
    ]
    rows.sort(key=lambda r: f(r["macro_f1"]), reverse=True)
    metrics = [
        ("macro_f1", "Macro F1"),
        ("exact_agreement", "Exact agreement"),
        ("macro_precision", "Macro precision"),
        ("macro_recall", "Macro recall"),
    ]

    svg = Svg(1500, 860, "RQ2 grader quality")
    header(
        svg,
        "RQ2 - Automated grading quality against human assessment",
        "Overall grading performance on Claude-generated state machines; higher is better.",
    )

    left = 120
    top = 145
    chart_w = 1180
    row_h = 132
    bar_h = 20
    x_label_w = 215
    x0 = left + x_label_w
    x1 = left + chart_w

    for tick in nice_ticks(0, 1, 6):
        x = x0 + tick * (x1 - x0)
        svg.line(x, top - 18, x, top + row_h * len(rows) + 30, PALETTE["grid"])
        svg.text(x, top + row_h * len(rows) + 64, pct(tick), cls="tiny", anchor="middle")
    svg.line(x0, top - 18, x0, top + row_h * len(rows) + 30, PALETTE["axis"])

    colors = [PALETTE["gemini"], PALETTE["gpt"], PALETTE["claude"]]
    for idx, row in enumerate(rows):
        y = top + idx * row_h
        grader = row["grader"]
        color = colors[idx % len(colors)]
        svg.rect(left - 28, y - 38, chart_w + 88, row_h - 12, "#ffffff", stroke="#edf0f6", rx=10)
        svg.text(left, y + 6, GRADER_LABELS.get(grader, grader), cls="panelTitle")
        svg.text(left, y + 32, f'n = {row["items"]} graded model elements', cls="small")
        for m_idx, (metric, metric_label) in enumerate(metrics):
            yy = y + 56 + m_idx * 20
            value = f(row[metric])
            w = value * (x1 - x0)
            fill = color if metric == "macro_f1" else "#a3adc2"
            svg.rect(x0, yy - bar_h + 5, w, bar_h - 5, fill, rx=7, opacity=0.95 if metric == "macro_f1" else 0.65)
            svg.text(x0 - 14, yy, metric_label, cls="tiny", anchor="end")
            svg.text(x0 + w + 10, yy, pct(value), cls="num")

    svg.text((x0 + x1) / 2, 720, "Score", cls="small", anchor="middle")
    svg.text(750, 760, "Data: rq2_grading_quality_summary.csv", cls="small", anchor="middle")
    svg.save(out_dir / "fig_rq2_grader_quality_overall.svg")


def heat_color(value: float) -> str:
    value = max(0, min(1, value))
    stops = [
        (0.00, (248, 250, 252)),
        (0.35, (204, 236, 229)),
        (0.70, (91, 190, 166)),
        (1.00, (14, 126, 112)),
    ]
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if a <= value <= b:
            t = (value - a) / (b - a) if b > a else 0
            rgb = tuple(round(ca[i] + t * (cb[i] - ca[i])) for i in range(3))
            return "#{:02x}{:02x}{:02x}".format(*rgb)
    return "#0e7e70"


def fig_rq2_heatmap(data_dir: Path, out_dir: Path):
    rows = read_csv(data_dir / "rq2_grading_quality_summary.csv")
    vals = {(r["grader"], r["model_element"]): f(r["macro_f1"]) for r in rows}

    svg = Svg(1500, 900, "RQ2 model element heatmap")
    header(
        svg,
        "RQ2 - Grading reliability by model element",
        "Macro F1 for each LLM grader, broken down by the type of model element.",
    )

    x0 = 310
    y0 = 165
    cell_w = 128
    cell_h = 112
    for c, element in enumerate(MODEL_ELEMENTS):
        x = x0 + c * cell_w
        svg.text(x + cell_w / 2, y0 - 28, label_element(element), cls="small", anchor="middle")
    for r, grader in enumerate(GRADERS):
        y = y0 + r * cell_h
        svg.text(80, y + cell_h / 2 + 6, GRADER_LABELS[grader], cls="panelTitle")
        for c, element in enumerate(MODEL_ELEMENTS):
            x = x0 + c * cell_w
            value = vals[(grader, element)]
            svg.rect(x + 4, y + 4, cell_w - 8, cell_h - 8, heat_color(value), stroke="#ffffff", rx=10)
            fill = "#ffffff" if value > 0.68 else PALETTE["ink"]
            svg.text(x + cell_w / 2, y + cell_h / 2 + 7, pct(value), cls="num", anchor="middle", fill=fill, size=22)

    legend_x = 420
    legend_y = 575
    legend_w = 520
    svg.text(legend_x, legend_y - 18, "Macro F1", cls="small")
    for i in range(100):
        value = i / 99
        svg.rect(legend_x + i * legend_w / 100, legend_y, legend_w / 100 + 1, 18, heat_color(value))
    for tick in nice_ticks(0, 1, 6):
        x = legend_x + tick * legend_w
        svg.line(x, legend_y + 18, x, legend_y + 28, PALETTE["axis"])
        svg.text(x, legend_y + 48, pct(tick), cls="tiny", anchor="middle")

    svg.text(750, 760, "Data: rq2_grading_quality_summary.csv", cls="small", anchor="middle")
    svg.save(out_dir / "fig_rq2_grader_quality_by_model_element.svg")


def fig_rq2_confusion(data_dir: Path, out_dir: Path):
    rows = [
        r
        for r in read_csv(data_dir / "rq2_confusion_matrices.csv")
        if r["model_element"] == "Overall Score"
    ]
    matrices: dict[str, dict[tuple[float, float], int]] = {g: {} for g in GRADERS}
    for row in rows:
        matrices[row["grader"]][(f(row["human_score"]), f(row["llm_score"]))] = int(row["count"])

    svg = Svg(1600, 760, "RQ2 confusion matrices")
    header(
        svg,
        "RQ2 - Overall human vs LLM grading decisions",
        "Row-normalized confusion matrices for the 0 / 0.5 / 1 assessment options.",
    )
    scores = [0.0, 0.5, 1.0]
    panel_w = 430
    cell = 96
    top = 165
    left = 120
    gap = 58
    for p_idx, grader in enumerate(GRADERS):
        x0 = left + p_idx * (panel_w + gap)
        y0 = top
        svg.rect(x0, y0 - 46, panel_w, 410, "#ffffff", stroke="#e7eaf2", rx=10)
        svg.text(x0 + panel_w / 2, y0 - 26, GRADER_LABELS[grader], cls="panelTitle", anchor="middle")
        matrix = matrices[grader]
        row_totals = {h: sum(matrix.get((h, l), 0) for l in scores) for h in scores}
        for i, h in enumerate(scores):
            svg.text(x0 + 32, y0 + i * cell + 58, str(h).rstrip("0").rstrip("."), cls="small", anchor="middle")
        for j, l in enumerate(scores):
            svg.text(x0 + 112 + j * cell + cell / 2, y0 - 12, str(l).rstrip("0").rstrip("."), cls="small", anchor="middle")
        for i, h in enumerate(scores):
            for j, l in enumerate(scores):
                count = matrix.get((h, l), 0)
                share = count / row_totals[h] if row_totals[h] else 0
                x = x0 + 112 + j * cell
                y = y0 + i * cell
                svg.rect(x, y, cell - 6, cell - 6, heat_color(share), stroke="#ffffff", rx=10)
                text_fill = "#ffffff" if share > 0.58 else PALETTE["ink"]
                svg.text(x + cell / 2 - 3, y + 39, pct(share), cls="num", anchor="middle", fill=text_fill, size=21)
                svg.text(x + cell / 2 - 3, y + 65, f"n={count}", cls="tiny", anchor="middle", fill=text_fill)
                if i == j:
                    svg.rect(x + 5, y + 5, cell - 16, cell - 16, "none", stroke="#17212b", rx=12, opacity=0.75)
        svg.text(x0 + 30, y0 + 334, "Human", cls="small")
        svg.text(x0 + 256, y0 + 334, "LLM score", cls="small", anchor="middle")

    svg.text(800, 620, "Data: rq2_confusion_matrices.csv", cls="small", anchor="middle")
    svg.save(out_dir / "fig_rq2_overall_confusion_matrices.svg")


def fig_rq3(data_dir: Path, out_dir: Path):
    rows = read_csv(data_dir / "rq3_grading_score_distribution.csv")
    keep = [r for r in rows if r["model_element"] in MODEL_ELEMENTS]
    data = {(r["generator"], r["model_element"]): r for r in keep}
    generators = ["GPT-5.5", "Gemini3.1ProPreview"]

    svg = Svg(1600, 920, "RQ3 grading trends")
    header(
        svg,
        "RQ3 - Grading trends on additional generated state machines",
        "Claude grader score distributions for GPT-5.5 and Gemini-generated state machines; not human-validated generation quality.",
    )
    legend(
        svg,
        [("Score 0", PALETTE["zero"]), ("Score 0.5", PALETTE["half"]), ("Score 1", PALETTE["one_score"])],
        58,
        112,
    )

    left = 170
    top = 155
    chart_w = 1260
    group_h = 68
    bar_h = 22
    label_w = 150
    x0 = left + label_w
    x1 = left + chart_w

    for tick in nice_ticks(0, 1, 6):
        x = x0 + tick * (x1 - x0)
        svg.line(x, top - 26, x, top + group_h * len(MODEL_ELEMENTS) + 16, PALETTE["grid"])
        svg.text(x, top + group_h * len(MODEL_ELEMENTS) + 38, pct(tick), cls="tiny", anchor="middle")

    for idx, element in enumerate(MODEL_ELEMENTS):
        y = top + idx * group_h
        svg.text(left, y + 31, label_element(element), cls="label", anchor="start")
        for g_idx, generator in enumerate(generators):
            row = data[(generator, element)]
            yy = y + 10 + g_idx * 28
            svg.text(x0 - 10, yy + 15, "GPT" if generator == "GPT-5.5" else "Gemini", cls="tiny", anchor="end")
            cursor = x0
            segments = [
                (f(row["score_0_pct"]), PALETTE["zero"], row["score_0_count"]),
                (f(row["score_0_5_pct"]), PALETTE["half"], row["score_0_5_count"]),
                (f(row["score_1_pct"]), PALETTE["one_score"], row["score_1_count"]),
            ]
            for share, color, count in segments:
                w = share * (x1 - x0)
                if w > 0:
                    svg.rect(cursor, yy, w, bar_h, color, rx=6 if cursor == x0 or math.isclose(cursor + w, x1) else 0)
                    if w > 52:
                        text_fill = "#ffffff" if color != PALETTE["half"] else PALETTE["ink"]
                        svg.text(cursor + w / 2, yy + 15, pct(share), cls="tiny", anchor="middle", fill=text_fill)
                cursor += w
            svg.text(x1 + 12, yy + 15, f'n={row["items"]}', cls="tiny")

    svg.text((x0 + x1) / 2, top + group_h * len(MODEL_ELEMENTS) + 74, "Share of model elements assigned each score", cls="small", anchor="middle")
    svg.text(800, 875, "Data: rq3_grading_score_distribution.csv", cls="small", anchor="middle")
    svg.save(out_dir / "fig_rq3_grading_trends_score_distribution.svg")


def write_contact_sheet(out_dir: Path):
    svgs = sorted(out_dir.glob("fig_*.svg"))
    cards = []
    for svg in svgs:
        cards.append(
            f'<section><h2>{esc(svg.stem)}</h2><img src="{esc(svg.name)}" alt="{esc(svg.stem)}"></section>'
        )
    html_doc = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Paper Figures</title>
<style>
body{margin:0;background:#eef2f7;color:#17212b;font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;}
main{max-width:1280px;margin:40px auto;padding:0 24px;}
h1{font-size:36px;margin:0 0 8px;}
p{color:#667085;margin:0 0 28px;}
section{background:white;border:1px solid #dfe5ee;border-radius:18px;padding:18px;margin:22px 0;box-shadow:0 12px 34px rgba(16,24,40,.08);}
h2{font-size:16px;margin:0 0 14px;color:#344054;}
img{width:100%;height:auto;border-radius:12px;background:#fbfcfe;}
</style>
</head>
<body><main>
<h1>Paper Figures</h1>
<p>Contact sheet generated from _Figures/PaperExperimentData.</p>
""" + "\n".join(cards) + """
</main></body></html>
"""
    (out_dir / "index.html").write_text(html_doc, encoding="utf-8")


def write_png_previews(out_dir: Path, width: int = 2400) -> None:
    converter = shutil.which("rsvg-convert")
    if converter is None:
        print("Skipping PNG previews: rsvg-convert is not installed.")
        return
    for svg_path in sorted(out_dir.glob("fig_*.svg")):
        png_path = svg_path.with_suffix(".png")
        subprocess.run(
            [converter, "-w", str(width), str(svg_path), "-o", str(png_path)],
            check=True,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    parser.add_argument(
        "--png",
        action="store_true",
        help="Also write PNG previews if rsvg-convert is available.",
    )
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    fig_rq1_f1_focus(args.data_dir, args.out_dir)
    fig_rq1(args.data_dir, args.out_dir)
    fig_rq2_overall(args.data_dir, args.out_dir)
    fig_rq2_heatmap(args.data_dir, args.out_dir)
    fig_rq2_confusion(args.data_dir, args.out_dir)
    fig_rq3(args.data_dir, args.out_dir)
    write_contact_sheet(args.out_dir)
    if args.png:
        write_png_previews(args.out_dir)
    print(f"Wrote paper figures to {args.out_dir}")


if __name__ == "__main__":
    main()
