#!/usr/bin/env python3
"""
Generate publication-ready global confusion matrix figures.

Aggregates all 2-stage / 6-examples CombinedHumanGrading xlsx files per
AutoGrading LLM and saves a single title-free Global figure per LLM to
_Figures/confusion_matrices/.

Output files (one per AutoGrading LLM):
  fig_rq2_confusion_global_<llm>.png

Usage:
  python generate_paper_rq2_confusion_matrices.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUT_DIR = (
    BASE_DIR / "_Figures" / "confusion_matrices" / "rq2_paper_figures" / "paper_figures"
)

sys.path.insert(0, str(Path(__file__).parent))
from generate_agreement_figures import (
    build_confusion_matrix,
    extract_autograding_llm,
    extract_human_vs_llm_key,
    find_xlsx_files,
    load_grading_data,
    plot_confusion_heatmap,
)


def _llm_file_slug(autograding_llm: str) -> str:
    """Convert e.g. 'Claude4.5SonnetAutoGrading' → 'claude4-5sonnet'."""
    name = autograding_llm.replace("AutoGrading", "").replace(".", "-")
    return name.lower()


def save_global_figure(
    df: pd.DataFrame,
    out_path: Path,
    llm_name: str = "",
    x_label: str = "LLM Score",
    y_label: str = "Human Score",
) -> None:
    """Save the Global (all element types) confusion matrix as PNG."""
    matrix = build_confusion_matrix(df, type_filter=None)
    fig, ax = plt.subplots(figsize=(5, 4.5))
    plot_confusion_heatmap(
        ax,
        matrix,
        llm_name,
        show_ylabel=True,
        show_xlabel=True,
        x_label=x_label,
        y_label=y_label,
        font_size=15,
    )
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=1000, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved → {out_path.relative_to(BASE_DIR)}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    files = find_xlsx_files(
        BASE_DIR,
        stage_filter="2",
        file_pattern="*CombinedHumanGrading*.xlsx",
    )
    files = [f for f in files if "6-examples" in str(f)]
    print(f"Found {len(files)} 2-stage / 6-examples file(s).\n")
    if not files:
        print("No files matched. Exiting.")
        return

    groups: dict[str, list[Path]] = {}
    for f in files:
        key = extract_human_vs_llm_key(f.stem)
        if key is None:
            print(f"  [WARN] Could not extract LLM key from {f.name}, skipping.")
            continue
        groups.setdefault(key, []).append(f)

    print(
        f"Found {len(groups)} AutoGrading LLM group(s): "
        + ", ".join(sorted(groups))
        + "\n"
    )

    for key in sorted(groups):
        group_files = sorted(groups[key])
        autograding_llm = extract_autograding_llm(key)
        slug = _llm_file_slug(autograding_llm)

        print(f"Group: {autograding_llm}  ({len(group_files)} file(s))")
        frames: list[pd.DataFrame] = []
        for xlsx_path in group_files:
            df = load_grading_data(xlsx_path)
            if df is not None and len(df) > 0:
                frames.append(df)
                print(f"  Loaded {len(df):3d} rows  ← {xlsx_path.name[:75]}")

        if not frames:
            print("  [WARN] No valid data. Skipping.")
            print()
            continue

        df_all = pd.concat(frames, ignore_index=True)
        print(f"  Aggregated: {len(df_all)} rows across {len(frames)} file(s)")
        save_global_figure(df_all, OUT_DIR / f"fig_rq2_confusion_global_{slug}.png")
        print()

    print("Done.")


if __name__ == "__main__":
    main()
