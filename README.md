# Evaluations - Directory Structure

This directory contains evaluation results for state machine diagram generation across multiple projects using different prompting strategies (1 stage vs 2 stage), along with automatic grading via an LLM.

All results were generated using **Claude Sonnet 4.5**.

The repositories used to generate these results are:

- https://github.com/reheant/mermaid-parser-py — Mermaid parsing logic  
- https://github.com/reheant/StateMachineLLM — Generation, prompting, and visualization logic  
## Top-Level Structure

```
Evaluations/
├── generate_agreement_figures.py          # Script: confusion matrix figures (LLM vs Human)
├── README.md
├── figures/                               # Reserved for additional top-level figures
├── global_analysis/
│   └── confusion_matrices/                # Aggregated confusion matrices across all files
│       ├── all_examples_confusion_matrices.png  # Combined 2×4 grid (all scopes)
│       ├── all_examples_global.png
│       ├── all_examples_state.png
│       ├── all_examples_transition.png
│       ├── all_examples_composite_state.png
│       ├── all_examples_guard.png
│       ├── all_examples_action.png
│       ├── all_examples_history_state.png
│       └── all_examples_region.png
└── [Project Name]/
    ├── [Project Name] - Description.pdf              # Problem description fed to the LLM
    ├── [Project Name] - Sample Solution.pdf          # Official reference solution
    ├── [Project Name] Evaluation - Template.xlsx     # Grading rubric and evaluation template
    ├── [project_name]_ground_truth_mermaid.txt       # Ground truth state machine in Mermaid syntax
    ├── [project_name]_ground_truth_mermaid_compiled.png  # Rendered PNG of the ground truth diagram
    └── Grading/
        ├── 1 stage/           # One stage evaluation results
        │   └── [Date]/
        │       ├── confusion_matrices/    # Per-run confusion matrix figures
        │       └── ...
        └── 2 stage/           # Two stage evaluation results
            ├── [Date]/
            │   ├── confusion_matrices/    # Per-run confusion matrix figures
            │   └── ...
            └── [Date]/
```

## Projects

### Main Evaluation Projects (Full 1 stage & 2 stage)

1. **Automatic Bread Maker** - State machine for a bread-making appliance
2. **Digital Chess Clock** - State machine for a chess timer
3. **Dishwasher** - State machine for a dishwashing appliance
4. **Printer** - State machine for a printer device
5. **Spa Manager** - State machine for a spa management system
6. **Thermomix TM6** - State machine for a cooking device
7. **Train Automation System** - State machine for train automation

### Validation Set Projects (2 stage only)

8. **SSC7** - State machine for a Self-Service Checkout
9. **Wumple** - State machine for a watch called W-UMPLE

> The validation set projects (SSC7 and Wumple) were evaluated only once with the two stage approach as a validation check, rather than with both one stage and two stage evaluations like the main projects.

## Directory Organization

### Reference Files (at Project Root Level)

#### `[Project Name] - Sample Solution.pdf`
**Purpose:** Contains the official solution or reference state machine diagram for the project

**Content:** Shows the expected state machine with correct states, transitions, events, guards, actions, and other elements

**Usage:** Use this as the ground truth when analyzing evaluation results and grading notes

#### `[Project Name] - Description.pdf`
**Purpose:** Contains the complete problem description and requirements for the state machine. This was fed to the LLM to generate the evaluated state machines.  

**Content:** Detailed specifications for system behaviour, constraints, and expected functionality  

**Usage:** Reference this to understand what the LLM was asked to generate and what the grading criteria are based on 

#### `[Project Name] Evaluation - Template.xlsx`
**Purpose:** Evaluation template and grading rubric used for this project  

**Content:** Spreadsheet where elements from the sample solution are broken down into their atomic components, along with inter-rater calculations (Cohen’s kappa and weighted Cohen’s kappa) and evaluation metrics such as F1 score, precision, and recall  

**Usage:** Defines the evaluation framework and metrics used across all evaluation runs  
#### `[project_name]_ground_truth_mermaid.txt`
**Purpose:** Ground truth state machine represented in Mermaid syntax, manually authored from the official sample solution

**Content:** Complete Mermaid `stateDiagram-v2` code capturing all states, transitions, guards, actions, composite states, and history states from the reference solution

**Usage:** Provided directly to the LLM grader as input (3) during automatic grading to give it an unambiguous, machine-readable representation of the expected state machine

#### `[project_name]_ground_truth_mermaid_compiled.png`
**Purpose:** Rendered visualization of the ground truth Mermaid diagram

**Content:** PNG image produced by compiling `[project_name]_ground_truth_mermaid.txt` with the project's Mermaid parser tool

**Usage:** Allows quick visual inspection of the ground truth without a Mermaid renderer; useful for cross-checking that the Mermaid source parses correctly  
### Stage Folders

#### `1 stage/` - One Stage Evaluation
Contains evaluation results where the model was prompted with a single prompt without refinement.

#### `2 stage/` - Two Stage Evaluation
Contains evaluation results where the model was prompted with an initial prompt, then a second refinement prompt to improve generation quality.

### Date Folders
Each stage contains date-timestamped folders (format: `YYYY-MM-DD`) representing when the evaluation was run. Where multiple date folders exist within the same stage, they represent runs using a different number of few-shot examples in the prompt:

- **Earlier dates** (e.g., `2026-03-03`, `2026-03-04`) used **3 few-shot examples** with a **max output token limit of 8,000**
- **Later dates** (e.g., `2026-03-12`, `2026-03-16`) used **6 few-shot examples** with a **max output token limit of 15,000**

The number of examples is also reflected in the file naming convention (e.g., `_3-examples_` vs `_6-examples_`). The 1 stage evaluations all used 3 few-shot examples with a max output token limit of 8,000.

---

## Agreement Analysis Script

### `generate_agreement_figures.py`

**Purpose:** Generates row-normalized confusion matrix figures comparing LLM grader scores against human grader scores, both per evaluation run and aggregated across all runs.

**How it works:** The script reads the `Weighted Cohens Kappa` sheet (matched by name, case-insensitively) from every `*CombinedHumanGradingAndLLMGrading.xlsx` file it finds under the `Evaluations/` tree. It builds 3×3 confusion matrices (scores: 0, 0.5, 1) for eight scopes:

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

**Per-run outputs** — written into `<date_dir>/confusion_matrices/` next to the xlsx file:
- `{file_stem}_confusion_matrices.png` — combined 2×4 grid showing all 8 scopes at once
- `{file_stem}_global.png`, `{file_stem}_state.png`, … `{file_stem}_region.png` — one figure per scope

Where `{file_stem}` mirrors the xlsx filename (without the `.xlsx` extension), e.g.:
`Printer_Grading_2-stage_2026-03-04_3-examples_CombinedHumanGradingAndLLMGrading_confusion_matrices.png`

**Aggregated outputs** — written into `global_analysis/confusion_matrices/` (same 9 files prefixed with `all_examples_`, pooling all evaluation runs together).

**Usage:**
```bash
# All files (both stages)
python generate_agreement_figures.py

# Only 2-stage files
python generate_agreement_figures.py --stage 2

# Only 1-stage files
python generate_agreement_figures.py --stage 1

# Restrict to a specific date
python generate_agreement_figures.py --date 2026-03-16
```

**Additional elements handling:** Rows where the element column is `"additional elements"` carry raw false-positive *counts* (not 0/0.5/1 scores). They are mapped to the confusion matrix as follows:

| Condition | Cell updated |
|-----------|-------------|
| `human=0` and `llm=0` (both found no extras) | `[0, 0]` += 1 |
| `llm > human` (LLM hallucinated extra elements) | `[0, 2]` += `llm − human` |
| `human > llm` (human found extras the LLM missed) | `[2, 0]` += `human − llm` |
| Both found extras | `[2, 2]` += `min(human, llm)` |

This mirrors the Excel `COUNTIFS`/`MAX`/`MIN` formulas in the `Weighted Cohens Kappa` sheet.

**Reading the figures:** Each cell shows the row-normalized percentage and raw count. Rows represent the human score; columns represent the LLM score. Diagonal cells (outlined in black) are agreements. The title of each heatmap shows the overall agreement rate and total number of graded elements for that scope.

---

## Output Files

Each date folder contains the following files:

### Grading Results Files

#### `grading_results.tsv` and `grading_output.txt`

**Grading Methodology:** The LLM was provided a CSV version of the evaluation template containing atomic components of the ground truth state machine (from the Sample Solution). The LLM then graded the generated Mermaid diagram by comparing it against three inputs: (1) the generated state machine, (2) the original problem description, and (3) the Mermaid representation of the solution.

**Content:** Both files contain identical grading results in different formats with columns for:
- **Type**: Element category (State, Transition, Action, Guard, Composite State, History State, etc.)
- **Element**: Specific component evaluated (e.g., "Off", "on (Off ⇒ On)", "delay=0; selectFirstCourse()")
- **Grading**: Score indicating correctness (0 = missing/incorrect, 0.5 = partial, 1 = correct)
- **Notes**: Explanation of assessment (expected vs. actual)

**Format Differences:**
- `grading_results.tsv` — Tab-separated, ideal for data analysis and automated processing
- `grading_output.txt` — Comma-separated (CSV), easier for text editor viewing and spreadsheet import  


### Confusion Matrix Figures

#### `confusion_matrices/` (inside each date folder)

**Purpose:** Per-run visual comparison of LLM grader scores vs human grader scores for that specific evaluation run

**Content:**
- `{file_stem}_confusion_matrices.png` — Combined 2×4 grid showing row-normalized confusion matrices for all 8 scopes (Global, State, Transition, Composite State, Guard, Action, History State, Region)
- Individual scope figures: `{file_stem}_global.png`, `{file_stem}_state.png`, `{file_stem}_transition.png`, `{file_stem}_composite_state.png`, `{file_stem}_guard.png`, `{file_stem}_action.png`, `{file_stem}_history_state.png`, `{file_stem}_region.png`

Where `{file_stem}` matches the xlsx filename without the `.xlsx` extension (e.g. `Printer_Grading_2-stage_2026-03-04_3-examples_CombinedHumanGradingAndLLMGrading`)

**Source:** Generated by `generate_agreement_figures.py` from the `*CombinedHumanGradingAndLLMGrading.xlsx` file in the same date folder

---

### Generated State Machine Files

#### `output_single_prompt.txt` / `output_single_prompt.png` (One Stage)
#### `output_two_stage_prompt.txt` / `output_two_stage_prompt.png` (Two Stage)

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

Ground truth state machines were evaluated by **two independent graders** using a standardized rubric (i.e., the provided `[Project Name] Evaluation - Template.xlsx`). Each grader independently assessed the generated diagrams against the atomic components defined in the sample solution. The two evaluations were then consolidated into a single grading sheet to produce the final human assessment.

### LLM-Based Grading

Following the human evaluation, the LLM was used to replicate the same grading methodology. It evaluated each generated Mermaid diagram using four inputs:  
1. the original system description,  
2. the structured evaluation rubric containing atomic components (provided as a CSV derived from `[Project Name] Evaluation - Template.xlsx`, without computed metrics),  
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

**Purpose:** Consolidated summary file containing aggregate evaluation metrics and performance analysis across all evaluated diagrams for a project

**Content:** The summary includes computed metrics derived from the grading results, specifically:
- **Precision, Recall, and F1-Score** for overall performance assessment
- **Confusion matrix values** showing distribution of correct/incorrect classifications
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

## How to Use This Data

1. **Compare Prompting Strategies**: Compare results between `1 stage/` and `2 stage/` folders to evaluate effectiveness of prompt refinement
2. **Track Improvements**: Compare across date folders within the same stage to track improvements over time or different model versions
3. **Analyze Failures**: Review the Notes column in TSV/CSV files to understand what aspects of state machine generation are failing
4. **Visualize Diagrams**: Use the `output_*.txt` files in Mermaid viewers to see the generated diagrams
5. **Assess LLM Grader Reliability**: Open any `confusion_matrices/confusion_matrices.png` to see at a glance how closely the LLM grader agreed with the human grader for that run; use `global_analysis/confusion_matrices/` for the pooled view across all runs
6. **Regenerate Figures**: Run `python generate_agreement_figures.py` from the `Evaluations/` directory whenever new `*CombinedHumanGradingAndLLMGrading.xlsx` files are added

## File Naming Convention

- `grading_output.txt` - LLM grading in CSV format of grading results in a .txt file
- `grading_results.tsv` - LLM grading in TSV format of grading results (tab-separated)
- `output_single_prompt.txt` - Generated state diagram from one stage (single prompt) - Mermaid code
- `output_single_prompt.png` - Generated state diagram from one stage (single prompt) - PNG visualization
- `output_two_stage_prompt.txt` - Generated state diagram from two stage (prompt with refinement) - Mermaid code
- `output_two_stage_prompt.png` - Generated state diagram from two stage (prompt with refinement) - PNG visualization
- `[project_name]_ground_truth_mermaid.txt` - Ground truth state machine in Mermaid syntax (at project root level)
- `[project_name]_ground_truth_mermaid_compiled.png` - Rendered PNG of the ground truth Mermaid diagram (at project root level)
- `confusion_matrices/{file_stem}_confusion_matrices.png` - Combined 2×4 confusion matrix grid for a single evaluation run
- `confusion_matrices/{file_stem}_global.png`, `{file_stem}_state.png`, … `{file_stem}_region.png` - Individual scope confusion matrices for a single evaluation run
- `global_analysis/confusion_matrices/all_examples_confusion_matrices.png` - Combined 2×4 confusion matrix grid aggregated across all evaluation runs
- `global_analysis/confusion_matrices/all_examples_global.png`, `all_examples_state.png`, … `all_examples_region.png` - Individual scope confusion matrices aggregated across all evaluation runs
