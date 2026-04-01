# Evaluations - Directory Structure

This directory contains evaluation results for state machine diagram generation across multiple projects using different prompting strategies (1 stage vs 2 stage), along with automatic grading via an LLM.

All results were generated using **Claude Sonnet 4.5**.

The repositories used to generate these results are:

- https://github.com/reheant/mermaid-parser-py — Mermaid parsing logic  
- https://github.com/reheant/StateMachineLLM — Generation, prompting, and visualization logic  
## Top-Level Structure

```
llm-automated-state-machine-design-eval/
├── [Project Name]/
│   └── Grading/
│       ├── 1 stage/           # One stage evaluation results
│       │   └── [Date]/
│       └── 2 stage/           # Two stage evaluation results
│           ├── [Date]/
│           └── [Date]/
└── README.md
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

Additional elements are treated as **false positives**:

- Each incorrect extra element counts as **+1**
- They **lower precision** and therefore **reduce F1-score**

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

## File Naming Convention

- `grading_output.txt` - LLM grading in CSV format of grading results in a .txt file
- `grading_results.tsv` - LLM grading in TSV format of grading results (tab-separated)
- `output_single_prompt.txt` - Generated state diagram from one stage (single prompt) - Mermaid code
- `output_single_prompt.png` - Generated state diagram from one stage (single prompt) - PNG visualization
- `output_two_stage_prompt.txt` - Generated state diagram from two stage (prompt with refinement) - Mermaid code
- `output_two_stage_prompt.png` - Generated state diagram from two stage (prompt with refinement) - PNG visualization
