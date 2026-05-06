# Evaluations - Directory Structure

This directory contains evaluation results for state machine diagram generation across multiple projects using different prompting strategies (1 stage vs 2 stage), along with human and automatic grading via an LLM.

Initial generation and grading results used **Claude 4.5 Sonnet** as both the generator and the auto-grader baseline. Two types of model comparison experiments are then defined:

| Experiment Type | What varies | What is fixed |
|-----------------|-------------|---------------|
| **Generation Comparison** | Generation model (e.g. GPT-5.5, Gemini 3.1 Pro Preview) | Auto-grader (Claude 4.5 Sonnet) |
| **Grading Comparison** | Auto-grader model (e.g. GPT-5.5, Gemini 3.1 Pro Preview) | Generation model (Claude 4.5 Sonnet) |

The repositories used to generate these results are:

- https://github.com/reheant/mermaid-parser-py — Mermaid parsing logic  
- https://github.com/reheant/StateMachineLLM — Generation, prompting, and visualization logic  

## Top-Level Structure

```
Evaluations/
├── _scripts/
│   └── generate_agreement_figures.py      # Script: confusion matrix figures (--mode flag)
├── _Figures/
│   └── Confusion Matrices/
│       └── ConfusionMatrices_CombinedHumanVs<AutoGradingLLM>_<GenerationLLM>/   # Aggregated + per-file human-vs-llm matrices
├── Grading Summary.xlsx
├── README.md
└── [Example Name]/
    ├── [Example Name] - Description.pdf
    ├── [Example Name] - Sample Solution.pdf
    ├── [Example Name] Evaluation - Template.xlsx
    ├── [example_name]_ground_truth_mermaid.txt
    ├── [example_name]_ground_truth_mermaid_compiled.png
    └── Grading/
        ├── 1 stage/
        │   └── 3-examples/          ← earlier run (3 few-shot examples, 8k token limit)
        │       ├── [Example]_..._CombinedHumanGradingVs<AutoGrader>AutoGrading_<GenerationLLM>Generation.xlsx
        │       ├── [Example]_..._HumanGrading_<GenerationLLM>Generation.xlsx
        │       └── Generated Files/             ← raw generation & grading outputs
        │           ├── grading_output__generated-by-<generation-llm>__graded-by-<grading-llm>.txt
        │           ├── grading_results__generated-by-<generation-llm>__graded-by-<grading-llm>.tsv
        │           ├── output_single_prompt__generated-by-<generation-llm>.txt
        │           ├── output_single_prompt__generated-by-<generation-llm>.png
        │           └── ...
        └── 2 stage/
            ├── 3-examples/           ← earlier run (3 few-shot examples, 8k token limit)
            │   ├── [Example]_..._CombinedHumanGradingVs<AutoGrader>AutoGrading_<GenerationLLM>Generation.xlsx
            │   ├── [Example]_..._HumanGrading_<GenerationLLM>Generation.xlsx
            │   └── Generated Files/
            │       └── ...
            └── 6-examples/           ← latest run (6 few-shot examples, 15k token limit)
                ├── [Example]_..._CombinedHumanGradingVs<AutoGrader>AutoGrading_<GenerationLLM>Generation.xlsx
                ├── [Example]_..._HumanGrading_<GenerationLLM>Generation.xlsx
                ├── [Example]_..._CombinedHumanGradingVs<NewGrader>AutoGrading_<GenerationLLM>Generation.xlsx  ← grading comparison (human vs new grader)
                ├── [Example]_..._<NewModel>GenerationVS<BaselineModel>Generation_<AutoGrader>AutoGrading.xlsx  ← generation comparison
                └── Generated Files/             ← raw generation & grading outputs
                    ├── grading_output__generated-by-<generation-llm>__graded-by-<grading-llm>.txt
                    ├── grading_results__generated-by-<generation-llm>__graded-by-<grading-llm>.tsv
                    ├── output_two_stage_prompt__generated-by-<generation-llm>.txt
                    ├── output_two_stage_prompt__generated-by-<generation-llm>.png
                    └── ...
```

## Examples

### Main Evaluation Examples (Full 1 stage & 2 stage)

1. **Automatic Bread Maker** - State machine for a bread-making appliance
2. **Digital Chess Clock** - State machine for a chess timer
3. **Dishwasher** - State machine for a dishwashing appliance
4. **Printer** - State machine for a printer device
5. **Spa Manager** - State machine for a spa management system
6. **Thermomix TM6** - State machine for a cooking device
7. **Train Automation System** - State machine for train automation

### Validation Set Examples (2 stage with 6-examples only)

8. **SSC7** - State machine for a Self-Service Checkout
9. **Wumple** - State machine for a watch called W-UMPLE

> The validation set projects (SSC7 and Wumple) were evaluated only once with the two stage approach as a validation check, rather than with both one stage and two stage evaluations like the main projects.

## Directory Organization

### Reference Files (at Example Root Level)

#### `[Example Name] - Sample Solution.pdf`
**Purpose:** Contains the official solution or reference state machine diagram for the project

**Content:** Shows the expected state machine with correct states, transitions, events, guards, actions, and other elements

**Usage:** Use this as the ground truth when analyzing evaluation results and grading notes

#### `[Example Name] - Description.pdf`
**Purpose:** Contains the complete problem description and requirements for the state machine. This was fed to the LLM to generate the evaluated state machines.  

**Content:** Detailed specifications for system behaviour, constraints, and expected functionality  

**Usage:** Reference this to understand what the LLM was asked to generate and what the grading criteria are based on 

#### `[Example Name] Evaluation - Template.xlsx`
**Purpose:** Evaluation template and grading rubric used for this project  

**Content:** Spreadsheet where elements from the sample solution are broken down into their atomic components, along with inter-rater calculations (Cohen’s kappa and weighted Cohen’s kappa) and evaluation metrics such as F1 score, precision, and recall  

**Usage:** Defines the evaluation framework and metrics used across all evaluation runs  
#### `[example_name]_ground_truth_mermaid.txt`
**Purpose:** Ground truth state machine represented in Mermaid syntax, manually authored from the official sample solution

**Content:** Complete Mermaid `stateDiagram-v2` code capturing all states, transitions, guards, actions, composite states, and history states from the reference solution

**Usage:** Provided directly to the LLM grader as input (3) during automatic grading to give it an unambiguous, machine-readable representation of the expected state machine

#### `[example_name]_ground_truth_mermaid_compiled.png`
**Purpose:** Rendered visualization of the ground truth Mermaid diagram

**Content:** PNG image produced by compiling `[example_name]_ground_truth_mermaid.txt` with the project's Mermaid parser tool

**Usage:** Allows quick visual inspection of the ground truth without a Mermaid renderer; useful for cross-checking that the Mermaid source parses correctly  
### Stage Folders

#### `1 stage/` - One Stage Evaluation
Contains evaluation results where the model was prompted with a single prompt without refinement.

#### `2 stage/` - Two Stage Evaluation
Contains evaluation results where the model was prompted with an initial prompt, then a second refinement prompt to improve generation quality.

### Example Count Folders
Each stage sub-directory is named after the number of few-shot examples that
were supplied to the LLM during that evaluation run:

| Folder name   | Stage(s)            | Few-shot examples | Max output tokens |
|---------------|---------------------|-------------------|-------------------|
| `3-examples`  | 1 stage and 2 stage | 3                 | 8,000             |
| `6-examples`  | 2 stage only        | 6                 | 15,000            |

**`3-examples`** — the prompt included 3 worked examples (few-shot demonstrations)
of correctly formatted Mermaid state diagrams.  All 1-stage evaluations and the
earlier of the two 2-stage evaluation runs used this configuration.

**`6-examples`** — the prompt was extended to include 6 worked examples, giving the
model more in-context guidance.  This is always the *latest* 2-stage run.  For the
validation-set examples (SSC7 and Wumple), which were evaluated only once, that
single 2-stage folder is named `6-examples`.

The example count is also embedded in each file name (e.g., `_3-examples_` vs
`_6-examples_`) so that individual files remain self-descriptive regardless of
which folder they reside in.
---

## Agreement Analysis Script

### `generate_agreement_figures.py`

**Purpose:** Generates row-normalized confusion matrix figures, both per evaluation run and aggregated across all runs. All outputs are written under `_Figures/Confusion Matrices/`.

#### Mode: `human-vs-llm`

Discovers all `*CombinedHumanGrading*.xlsx` files and generates a separate set of confusion matrices **per AutoGrading LLM found**, aggregated only across files that share the same AutoGrading LLM.
- **Source files:** `*CombinedHumanGrading*.xlsx` (across all date-folders)
- **Per-file output:** `_Figures/Confusion Matrices/ConfusionMatrices_CombinedHumanVs<AutoGradingLLM>_<GenerationLLM>/per_file/<Project>_<stage>_<examples>/`
- **Aggregated output:** `_Figures/Confusion Matrices/ConfusionMatrices_CombinedHumanVs<AutoGradingLLM>_<GenerationLLM>/`

**How it works:** The script reads the `Weighted Cohens Kappa` sheet from matching xlsx files. It builds 3×3 confusion matrices (scores: 0, 0.5, 1) for eight scopes:

| Scope | Description |
|-------|-------------|
| Global | All elements combined |
| State | State elements only |
| Transition | Transition elements only |
| Composite State | Composite state elements only |
| Guard | Guard elements only |
| Action | Action elements only |
| History State | History state elements only |
| Region | Region elements only |

**Per-file outputs** — written to `<group_dir>/per_file/<Project>_<stage>_<examples>/`:
- `confusion_matrices.png` — combined 2×4 grid (all 8 scopes)
- `global.png`, `state.png`, … `region.png` — one figure per scope

**Aggregated outputs** — pooled across all matched files, written to `<group_dir>/`:
- prefixed with `AllExamples_CombinedHumanVs<AutoGradingLLM>_<GenerationLLM>_`

**Usage:**
```bash
# All files
python _scripts/generate_agreement_figures.py

# 2-stage files only
python _scripts/generate_agreement_figures.py --stage 2

# Specific date
python _scripts/generate_agreement_figures.py --date 2026-03-16
```

**Additional elements handling:** Rows where the element column is `"additional elements"` carry raw false-positive *counts* (not 0/0.5/1 scores). They are mapped to the confusion matrix as follows:

| Condition | Cell updated |
|-----------|-------------|
| Both found no extras (`human=0`, `llm=0`) | `[0, 0]` += 1 |
| New grader/LLM found more extras (`new > baseline`) | `[0, 2]` += `new − baseline` |
| Baseline found more extras (`baseline > new`) | `[2, 0]` += `baseline − new` |
| Both found extras | `[2, 2]` += `min(human, llm)` |

---

## Output Files

### Excel Files (at examples level)

- `[Example]_..._CombinedHumanGradingVs<AutoGrader>AutoGrading_<GenerationLLM>Generation.xlsx` — consolidated human + auto-grading workbook (baseline)
- `[Example]_..._HumanGrading_<GenerationLLM>Generation.xlsx` — human-only grading workbook
- `[Example]_..._<NewModel>GenerationVS<BaselineModel>Generation_<AutoGrader>AutoGrading.xlsx` — generation comparison workbook (one per new generator)


### Confusion Matrix Figures

All confusion matrix figures are centralized under `_Figures/Confusion Matrices/`, with one sub-folder per comparison type.

#### `_Figures/Confusion Matrices/ConfusionMatrices_CombinedHumanVs<AutoGradingLLM>_<GenerationLLM>/`

One folder exists per AutoGrading LLM (e.g. `ConfusionMatrices_CombinedHumanVs<AutoGrader>AutoGrading_<GenerationLLM>Generation/`).

**Source:** Generated by `_scripts/generate_agreement_figures.py` from `*CombinedHumanGrading*.xlsx` files.

**Contents:**
- `AllExamples_CombinedHumanVs<key>_confusion_matrices.png` — Aggregated 2×4 grid across all examples
- `AllExamples_CombinedHumanVs<key>_{scope}.png` — Aggregated individual scope figures
- `per_file/<Project>_<stage>_<examples>/` — Per-file breakdown
  - `confusion_matrices.png` — 2×4 grid for a single evaluation run
  - `global.png`, `state.png`, … `region.png` — individual scope figures

**Reading the figures:** Each cell shows the row-normalized percentage and raw count. Rows = human score; columns = LLM score. Diagonal cells (outlined in black) are agreements. The title shows the overall agreement rate and element count.



### Grading Results Files (inside `Generated Files/` subfolder)

#### `grading_results__generated-by-<generation-llm>__graded-by-<grading-llm>.tsv` and `grading_output__generated-by-<generation-llm>__graded-by-<grading-llm>.txt`

**Grading Methodology:** The LLM was provided a CSV version of the evaluation template containing atomic components of the ground truth state machine (from the Sample Solution). The LLM then graded the generated Mermaid diagram by comparing it against three inputs: (1) the generated state machine, (2) the original problem description, and (3) the Mermaid representation of the solution.

**Content:** Both files contain identical grading results in different formats with columns for:
- **Type**: Element category (State, Transition, Action, Guard, Composite State, History State, etc.)
- **Element**: Specific component evaluated (e.g., "Off", "on (Off ⇒ On)", "delay=0; selectFirstCourse()")
- **Grading**: Score indicating correctness (0 = missing/incorrect, 0.5 = partial, 1 = correct)
- **Notes**: Explanation of assessment (expected vs. actual)

**Format Differences:**
- `grading_results__generated-by-<generation-llm>__graded-by-<grading-llm>.tsv` — Tab-separated, ideal for data analysis and automated processing
- `grading_output__generated-by-<generation-llm>__graded-by-<grading-llm>.txt` — Comma-separated (CSV), easier for text editor viewing and spreadsheet import

---

### Generated State Machine Files (inside `Generated Files/` subfolder)
#### `output_two_stage_prompt__generated-by-<generation-llm>.txt` / `output_two_stage_prompt__generated-by-<generation-llm>.png` (Two Stage)

**Purpose:** The generated state machine diagram produced by the LLM based on the problem description

**Content — Text Format (`.txt`):**
- Complete Mermaid state diagram syntax
- Includes state declarations, transitions, events, guards, actions, composite states, and substates

**Content — Visual Format (`.png`):**
- Rendered visualization of the Mermaid diagram
- Allows direct viewing without a Mermaid renderer

**Example Mermaid Structure:**
```
stateDiagram-v2
    state Off
    [*] --> Off
    Off --> On : on
    On --> Off : off
    ...
```

## Evaluation Methodology

### Human Grading Process

Generated state machines by Claude Sonnet 4.5 were evaluated by **two independent graders** using a standardized rubric (i.e., the provided `[Example Name] Evaluation - Template.xlsx`). Each grader independently assessed the generated diagrams against the atomic components defined in the sample solution. The two evaluations were then consolidated into a single grading sheet to produce the final human assessment.

### LLM-Based Grading (Automatic Grading)

Following the human evaluation, the LLM grader was used to replicate the same grading methodology. It evaluated each generated Mermaid diagram using four inputs:  
1. the original system description,  
2. the structured evaluation rubric containing atomic components (provided as a CSV derived from `[Example Name] Evaluation - Template.xlsx`, without computed metrics),  
3. the ground truth Mermaid diagram, and  
4. the generated Mermaid diagram to be graded.  

The LLM then assigned scores to each rubric component and generated concise justifications, prioritizing semantic correctness and alignment with the intended system behaviour.

## Grading Scheme

The grading rubric evaluates multiple criteria across **states, transitions, guards, actions, composite states, regions, and history states**. Each element is scored using the following scale:

| Value | Definition |
|-------|-----------|
| **1** | Correct — matches expected behaviour |
| **0.5** | Partially correct — minor issue or incomplete |
| **0** | Incorrect or missing |
| **Additional** | Extra (unexpected) elements |

### Additional Elements (False Positives)

Additional elements are treated as **false positives** in the grading metrics:

- Each incorrect extra element counts as **+1**
- They **lower precision** and therefore **reduce F1-score**

In the confusion matrices they are mapped by comparing the raw human and LLM false-positive counts per element type:

| Condition | Confusion matrix cell |
|-----------|----------------------|
| Both graders found **no** extra elements (`human=0`, `llm=0`) | `[0, 0]` — agreement at score 0 |
| LLM hallucinated more extras than human (`llm > human`) | `[0, 2]` — LLM over-generates |
| Human found more extras than LLM (`human > llm`) | `[2, 0]` — human found more FPs |
| Both found extras | `[2, 2]` += `min(human, llm)` — shared agreement on extras |

> **Note:** A global consistency section (evaluating formatting and naming conventions) was initially included but removed as too subjective. The evaluation now focuses on semantic correctness and functional completeness rather than stylistic conventions.

The final output is a completed grading sheet where each element is scored and justified concisely, ensuring alignment with expected system behaviour.

## Grading Summary and Performance Metrics

### `Grading Summary.xlsx`

**Purpose:** Consolidated summary file containing aggregate evaluation metrics from human grading of the generated state machine using Claude Sonnet 4.5, as well as automatic grading across all stages of the automatic grader using Claude Sonnet 4.5, including performance analysis across all evaluated diagrams for the project.

**Content:** The summary includes computed metrics derived from the grading results, specifically:
- **Precision, Recall, and F1-Score** for overall performance assessment
- **Statistical summaries** aggregating results across multiple evaluation runs

### Performance Metrics Explanation

The following metrics are used to evaluate LLM performance in generating state machines:

| Metric | Definition | Calculation |
|--------|-----------|-------------|
| **Precision** | Proportion of generated elements that are correct | TP / (TP + FP) |
| **Recall** | Proportion of required elements that were generated | TP / (TP + FN) |
| **F1-Score** | Harmonic mean balancing precision and recall | 2 × (Precision × Recall) / (Precision + Recall) |

**Interpretation:**
- **High Precision** → Few unnecessary elements (good specificity)
- **High Recall** → Few missing required elements (good completeness)
- **High F1-Score** → Well-balanced correctness and completeness

### Confusion Matrix Components

The grading results are classified using the following categories:

| Component | Definition |
|-----------|-----------|
| **TP (True Positive)** | Correctly generated elements matching the expected specification |
| **FP (False Positive)** | Unnecessary or incorrect additional elements generated by the LLM |
| **FN (False Negative)** | Missing required elements that should have been generated |
| **TN (True Negative)** | Not applicable in this context (elements are either present or absent) |

---

## File Naming Convention

**Raw outputs (inside `Generated Files/`):**
- `grading_output__generated-by-<generation-llm>__graded-by-<grading-llm>.txt` — auto-grading output in CSV format
- `grading_results__generated-by-<generation-llm>__graded-by-<grading-llm>.tsv` — auto-grading output in TSV format
- `output_single_prompt__generated-by-<generation-llm>.txt/.png` — Generated state diagram (1 stage)
- `output_two_stage_prompt__generated-by-<generation-llm>.txt/.png` — Generated state diagram (2 stage)

**Baseline xlsx files (at examples level):**
- `[Example]_..._CombinedHumanGradingVs<grading-llm>AutoGrading_<GenerationLLM>Generation.xlsx` — consolidated human + auto-grading workbook
- `[Example]_..._HumanGrading_<GenerationLLM>Generation.xlsx` — human-only grading workbook

**Generation comparison xlsx files (at examples level):**
- `[Example]_Grading_<stage>_{date}_{N}-examples_<NewModel>GenerationVS<BaselineModel>Generation_<AutoGrader>AutoGrading.xlsx`

**Grading comparison xlsx files (at examples level):**
- `[Example]_Grading_<stage>_{date}_{N}-examples_<NewGrader>AutoGradingVS<BaselineGrader>AutoGrading_<GenerationLLM>Generation.xlsx`

**Ground truth (at project root level):**
- `[example_name]_ground_truth_mermaid.txt`
- `[example_name]_ground_truth_mermaid_compiled.png`

**Confusion matrix figures (per-file, inside `_Figures/Confusion Matrices/<group>/per_file/<Project>_<stage>_<examples>/`):**
- `confusion_matrices.png` — combined 2×4 grid for a single evaluation run
- `{scope}.png` — individual scope figure (e.g. `global.png`, `state.png`)

**Confusion matrix figures (aggregated, inside `_Figures/Confusion Matrices/<group>/`):**
- `AllExamples_CombinedHumanVs<AutoGradingLLM>_<GenerationLLM>_{scope}.png`

