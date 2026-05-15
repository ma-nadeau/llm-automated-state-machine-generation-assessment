# Paper Experiment Summary

## RQ1: Claude Generation Quality From Human Assessment

Source script: `_scripts/summarize_paper_experiments.py`

Source CSVs: `_Figures/PaperExperimentData/rq1_generation_quality_summary.csv`, `_Figures/PaperExperimentData/rq1_generation_quality_by_example.csv`

| Approach | Model element | Examples | Precision | Recall | F1 |
| --- | --- | --- | --- | --- | --- |
| one-stage | Composite State | 7 | 1.000 | 0.881 | 0.926 |
| one-stage | State | 7 | 1.000 | 0.766 | 0.861 |
| one-stage | Transition | 7 | 1.000 | 0.664 | 0.788 |
| one-stage | Action | 7 | 1.000 | 0.526 | 0.678 |
| one-stage | Region | 7 | 1.000 | 0.625 | 0.889 |
| one-stage | History State | 7 | 1.000 | 0.429 | 1.000 |
| one-stage | Guard | 7 | 1.000 | 0.550 | 0.765 |
| one-stage | Overall Score | 7 | 1.000 | 0.665 | 0.791 |
| two-stage (6 examples) | Composite State | 9 | 1.000 | 0.852 | 0.975 |
| two-stage (6 examples) | State | 9 | 1.000 | 0.870 | 0.925 |
| two-stage (6 examples) | Transition | 9 | 1.000 | 0.886 | 0.918 |
| two-stage (6 examples) | Action | 9 | 1.000 | 0.739 | 0.817 |
| two-stage (6 examples) | Region | 9 | 1.000 | 0.900 | 0.933 |
| two-stage (6 examples) | History State | 9 | 0.867 | 0.667 | 0.900 |
| two-stage (6 examples) | Guard | 9 | 1.000 | 0.756 | 0.889 |
| two-stage (6 examples) | Overall Score | 9 | 0.997 | 0.833 | 0.903 |

## RQ2: LLM Grading Quality Against Human Assessment

Source script: `_scripts/summarize_paper_experiments.py`

Source CSV: `_Figures/PaperExperimentData/rq2_grading_quality_summary.csv`

| Grader | Model element | Items | Exact agreement | Macro P | Macro R | Macro F1 |
| --- | --- | --- | --- | --- | --- | --- |
| Claude4.5Sonnet | Composite State | 31 | 0.839 | 0.732 | 0.883 | 0.779 |
| Claude4.5Sonnet | State | 131 | 0.826 | 0.548 | 0.564 | 0.540 |
| Claude4.5Sonnet | Transition | 189 | 0.825 | 0.521 | 0.618 | 0.551 |
| Claude4.5Sonnet | Action | 112 | 0.643 | 0.557 | 0.549 | 0.511 |
| Claude4.5Sonnet | Region | 24 | 0.958 | 0.958 | 0.962 | 0.958 |
| Claude4.5Sonnet | History State | 18 | 0.737 | 0.571 | 0.500 | 0.750 |
| Claude4.5Sonnet | Guard | 66 | 0.773 | 0.685 | 0.750 | 0.695 |
| Claude4.5Sonnet | Overall Score | 571 | 0.787 | 0.583 | 0.638 | 0.599 |
| GPT-5.5 | Composite State | 31 | 0.903 | 0.750 | 0.933 | 0.765 |
| GPT-5.5 | State | 131 | 0.893 | 0.706 | 0.737 | 0.717 |
| GPT-5.5 | Transition | 189 | 0.836 | 0.623 | 0.682 | 0.637 |
| GPT-5.5 | Action | 112 | 0.679 | 0.653 | 0.673 | 0.545 |
| GPT-5.5 | Region | 24 | 0.958 | 0.667 | 0.955 | 0.976 |
| GPT-5.5 | History State | 18 | 0.789 | 0.556 | 0.542 | 0.812 |
| GPT-5.5 | Guard | 66 | 0.803 | 0.680 | 0.624 | 0.615 |
| GPT-5.5 | Overall Score | 571 | 0.822 | 0.644 | 0.679 | 0.646 |
| Gemini3.1ProPreview | Composite State | 31 | 0.903 | 0.773 | 0.933 | 0.824 |
| Gemini3.1ProPreview | State | 131 | 0.908 | 0.743 | 0.776 | 0.749 |
| Gemini3.1ProPreview | Transition | 189 | 0.878 | 0.628 | 0.725 | 0.660 |
| Gemini3.1ProPreview | Action | 112 | 0.696 | 0.521 | 0.490 | 0.749 |
| Gemini3.1ProPreview | Region | 24 | 0.958 | 0.958 | 0.962 | 0.958 |
| Gemini3.1ProPreview | History State | 18 | 0.789 | 0.857 | 0.542 | 0.801 |
| Gemini3.1ProPreview | Guard | 66 | 0.833 | 0.713 | 0.703 | 0.690 |
| Gemini3.1ProPreview | Overall Score | 571 | 0.846 | 0.644 | 0.693 | 0.662 |

## RQ2: Overall Confusion Matrices

Source script: `_scripts/summarize_paper_experiments.py`

Source CSV: `_Figures/PaperExperimentData/rq2_confusion_matrices.csv`

**Claude4.5Sonnet**

| Human \ LLM | 0 | 0.5 | 1 |
| --- | --- | --- | --- |
| 0.0 | 109 | 3 | 11 |
| 0.5 | 26 | 8 | 2 |
| 1.0 | 33 | 47 | 334 |

**GPT-5.5**

| Human \ LLM | 0 | 0.5 | 1 |
| --- | --- | --- | --- |
| 0.0 | 86 | 28 | 8 |
| 0.5 | 16 | 16 | 4 |
| 1.0 | 11 | 35 | 368 |

**Gemini3.1ProPreview**

| Human \ LLM | 0 | 0.5 | 1 |
| --- | --- | --- | --- |
| 0.0 | 109 | 9 | 4 |
| 0.5 | 23 | 11 | 2 |
| 1.0 | 30 | 20 | 364 |

## RQ3: Grader Behavior Consistency Across Generated Inputs

Source script: `_scripts/summarize_paper_experiments.py`

Source CSVs: `_Figures/PaperExperimentData/rq3_grading_score_distribution.csv`, `_Figures/PaperExperimentData/rq3_per_grader_stability.csv`, `_Figures/PaperExperimentData/rq3_cross_grader_rankings.csv`

RQ3 tests whether grader behavior patterns observed on Claude-generated state machines persist when the generated inputs change to GPT-5.5 and Gemini 3.1 Pro Preview outputs. Claude-generated state machines are the baseline condition; GPT-5.5- and Gemini-generated state machines are comparison conditions. These tables use only LLM-assigned score distributions and do not evaluate GPT/Gemini generation quality because human ground truth is not available for those generated state machines.

**Score distributions**

| Generator | Grader | Model element | Items | Score 0 | Score 0.5 | Score 1 |
| --- | --- | --- | --- | --- | --- | --- |
| Claude4.5Sonnet | Claude4.5Sonnet | Action | 111 | 0.441 | 0.207 | 0.351 |
| Claude4.5Sonnet | Claude4.5Sonnet | Composite State | 31 | 0.323 | 0.097 | 0.581 |
| Claude4.5Sonnet | Claude4.5Sonnet | Guard | 66 | 0.333 | 0.212 | 0.455 |
| Claude4.5Sonnet | Claude4.5Sonnet | History State | 18 | 0.722 | 0.056 | 0.222 |
| Claude4.5Sonnet | Claude4.5Sonnet | Overall Score | 569 | 0.306 | 0.109 | 0.585 |
| Claude4.5Sonnet | Claude4.5Sonnet | Region | 24 | 0.542 | 0.000 | 0.458 |
| Claude4.5Sonnet | Claude4.5Sonnet | State | 129 | 0.225 | 0.039 | 0.736 |
| Claude4.5Sonnet | Claude4.5Sonnet | Transition | 190 | 0.200 | 0.084 | 0.716 |
| Claude4.5Sonnet | GPT-5.5 | Action | 111 | 0.153 | 0.324 | 0.523 |
| Claude4.5Sonnet | GPT-5.5 | Composite State | 31 | 0.290 | 0.129 | 0.581 |
| Claude4.5Sonnet | GPT-5.5 | Guard | 66 | 0.364 | 0.030 | 0.606 |
| Claude4.5Sonnet | GPT-5.5 | History State | 18 | 0.611 | 0.111 | 0.278 |
| Claude4.5Sonnet | GPT-5.5 | Overall Score | 571 | 0.198 | 0.151 | 0.651 |
| Claude4.5Sonnet | GPT-5.5 | Region | 24 | 0.375 | 0.083 | 0.542 |
| Claude4.5Sonnet | GPT-5.5 | State | 131 | 0.183 | 0.053 | 0.763 |
| Claude4.5Sonnet | GPT-5.5 | Transition | 190 | 0.100 | 0.174 | 0.726 |
| Claude4.5Sonnet | Gemini3.1ProPreview | Action | 111 | 0.396 | 0.126 | 0.477 |
| Claude4.5Sonnet | Gemini3.1ProPreview | Composite State | 31 | 0.355 | 0.065 | 0.581 |
| Claude4.5Sonnet | Gemini3.1ProPreview | Guard | 66 | 0.364 | 0.091 | 0.545 |
| Claude4.5Sonnet | Gemini3.1ProPreview | History State | 18 | 0.722 | 0.000 | 0.278 |
| Claude4.5Sonnet | Gemini3.1ProPreview | Overall Score | 571 | 0.285 | 0.079 | 0.636 |
| Claude4.5Sonnet | Gemini3.1ProPreview | Region | 24 | 0.542 | 0.000 | 0.458 |
| Claude4.5Sonnet | Gemini3.1ProPreview | State | 131 | 0.198 | 0.046 | 0.756 |
| Claude4.5Sonnet | Gemini3.1ProPreview | Transition | 190 | 0.168 | 0.089 | 0.742 |
| GPT-5.5 | Claude4.5Sonnet | Action | 111 | 0.144 | 0.027 | 0.829 |
| GPT-5.5 | Claude4.5Sonnet | Composite State | 31 | 0.355 | 0.000 | 0.645 |
| GPT-5.5 | Claude4.5Sonnet | Guard | 66 | 0.182 | 0.015 | 0.803 |
| GPT-5.5 | Claude4.5Sonnet | History State | 18 | 0.667 | 0.000 | 0.333 |
| GPT-5.5 | Claude4.5Sonnet | Overall Score | 570 | 0.167 | 0.030 | 0.804 |
| GPT-5.5 | Claude4.5Sonnet | Region | 23 | 0.391 | 0.087 | 0.522 |
| GPT-5.5 | Claude4.5Sonnet | State | 131 | 0.130 | 0.008 | 0.863 |
| GPT-5.5 | Claude4.5Sonnet | Transition | 190 | 0.095 | 0.053 | 0.853 |
| GPT-5.5 | GPT-5.5 | Action | 111 | 0.108 | 0.045 | 0.847 |
| GPT-5.5 | GPT-5.5 | Composite State | 31 | 0.290 | 0.032 | 0.677 |
| GPT-5.5 | GPT-5.5 | Guard | 66 | 0.197 | 0.030 | 0.773 |
| GPT-5.5 | GPT-5.5 | History State | 18 | 0.500 | 0.111 | 0.389 |
| GPT-5.5 | GPT-5.5 | Overall Score | 571 | 0.131 | 0.049 | 0.820 |
| GPT-5.5 | GPT-5.5 | Region | 24 | 0.417 | 0.000 | 0.583 |
| GPT-5.5 | GPT-5.5 | State | 131 | 0.084 | 0.053 | 0.863 |
| GPT-5.5 | GPT-5.5 | Transition | 190 | 0.058 | 0.058 | 0.884 |
| GPT-5.5 | Gemini3.1ProPreview | Action | 111 | 0.108 | 0.063 | 0.829 |
| GPT-5.5 | Gemini3.1ProPreview | Composite State | 31 | 0.290 | 0.000 | 0.710 |
| GPT-5.5 | Gemini3.1ProPreview | Guard | 66 | 0.182 | 0.076 | 0.742 |
| GPT-5.5 | Gemini3.1ProPreview | History State | 18 | 0.611 | 0.056 | 0.333 |
| GPT-5.5 | Gemini3.1ProPreview | Overall Score | 571 | 0.154 | 0.039 | 0.807 |
| GPT-5.5 | Gemini3.1ProPreview | Region | 24 | 0.500 | 0.000 | 0.500 |
| GPT-5.5 | Gemini3.1ProPreview | State | 131 | 0.115 | 0.031 | 0.855 |
| GPT-5.5 | Gemini3.1ProPreview | Transition | 190 | 0.089 | 0.026 | 0.884 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Action | 111 | 0.477 | 0.072 | 0.450 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Composite State | 31 | 0.355 | 0.032 | 0.613 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Guard | 66 | 0.318 | 0.121 | 0.561 |
| Gemini3.1ProPreview | Claude4.5Sonnet | History State | 18 | 0.722 | 0.000 | 0.278 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Overall Score | 571 | 0.273 | 0.068 | 0.658 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Region | 24 | 0.458 | 0.042 | 0.500 |
| Gemini3.1ProPreview | Claude4.5Sonnet | State | 131 | 0.153 | 0.046 | 0.802 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Transition | 190 | 0.142 | 0.079 | 0.779 |
| Gemini3.1ProPreview | GPT-5.5 | Action | 111 | 0.162 | 0.135 | 0.703 |
| Gemini3.1ProPreview | GPT-5.5 | Composite State | 31 | 0.290 | 0.032 | 0.677 |
| Gemini3.1ProPreview | GPT-5.5 | Guard | 66 | 0.288 | 0.091 | 0.621 |
| Gemini3.1ProPreview | GPT-5.5 | History State | 18 | 0.556 | 0.111 | 0.333 |
| Gemini3.1ProPreview | GPT-5.5 | Overall Score | 571 | 0.172 | 0.086 | 0.743 |
| Gemini3.1ProPreview | GPT-5.5 | Region | 24 | 0.375 | 0.125 | 0.500 |
| Gemini3.1ProPreview | GPT-5.5 | State | 131 | 0.115 | 0.046 | 0.840 |
| Gemini3.1ProPreview | GPT-5.5 | Transition | 190 | 0.095 | 0.084 | 0.821 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | Action | 111 | 0.270 | 0.099 | 0.631 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | Composite State | 31 | 0.290 | 0.032 | 0.677 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | Guard | 66 | 0.303 | 0.076 | 0.621 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | History State | 18 | 0.611 | 0.000 | 0.389 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | Overall Score | 571 | 0.217 | 0.042 | 0.741 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | Region | 24 | 0.500 | 0.000 | 0.500 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | State | 131 | 0.145 | 0.015 | 0.840 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | Transition | 190 | 0.121 | 0.026 | 0.853 |

**Per-grader stability (Overall Score)**

| Grader | Comparison generator | Baseline %1 | Comparison %1 | Delta %1 | Baseline %0.5 | Comparison %0.5 | Delta %0.5 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude4.5Sonnet | GPT-5.5 | 0.585 | 0.804 | 0.218 | 0.109 | 0.030 | -0.079 |
| Claude4.5Sonnet | Gemini3.1ProPreview | 0.585 | 0.658 | 0.073 | 0.109 | 0.068 | -0.041 |
| GPT-5.5 | GPT-5.5 | 0.651 | 0.820 | 0.168 | 0.151 | 0.049 | -0.102 |
| GPT-5.5 | Gemini3.1ProPreview | 0.651 | 0.743 | 0.091 | 0.151 | 0.086 | -0.065 |
| Gemini3.1ProPreview | GPT-5.5 | 0.636 | 0.807 | 0.172 | 0.079 | 0.039 | -0.040 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | 0.636 | 0.741 | 0.105 | 0.079 | 0.042 | -0.037 |

**Cross-grader rankings by %1 (Overall Score)**

| Generator | Grader | Score 1 | Rank |
| --- | --- | --- | --- |
| Claude4.5Sonnet | GPT-5.5 | 0.651 | 1 |
| Claude4.5Sonnet | Gemini3.1ProPreview | 0.636 | 2 |
| Claude4.5Sonnet | Claude4.5Sonnet | 0.585 | 3 |
| GPT-5.5 | GPT-5.5 | 0.820 | 1 |
| GPT-5.5 | Gemini3.1ProPreview | 0.807 | 2 |
| GPT-5.5 | Claude4.5Sonnet | 0.804 | 3 |
| Gemini3.1ProPreview | GPT-5.5 | 0.743 | 1 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | 0.741 | 2 |
| Gemini3.1ProPreview | Claude4.5Sonnet | 0.658 | 3 |

## Full CSV Data Appendix

This appendix embeds the generated experiment CSV outputs so the Markdown summary contains the full paper-facing data tables in one place.

### data_availability.csv

Source CSV: `_Figures/PaperExperimentData/data_availability.csv`

Source script: `_scripts/summarize_paper_experiments.py`

Rows: 12

Description: Counts available workbook/TSV inputs by generator, grader, and data kind.

| generator | grader | data_kind | file_count |
| --- | --- | --- | --- |
| Claude4.5Sonnet | Claude4.5Sonnet | human-vs-llm xlsx | 9 |
| Claude4.5Sonnet | Claude4.5Sonnet | llm-grading tsv | 9 |
| Claude4.5Sonnet | GPT-5.5 | human-vs-llm xlsx | 9 |
| Claude4.5Sonnet | GPT-5.5 | llm-grading tsv | 9 |
| Claude4.5Sonnet | Gemini3.1ProPreview | human-vs-llm xlsx | 9 |
| Claude4.5Sonnet | Gemini3.1ProPreview | llm-grading tsv | 9 |
| GPT-5.5 | Claude4.5Sonnet | llm-grading tsv | 9 |
| GPT-5.5 | GPT-5.5 | llm-grading tsv | 9 |
| GPT-5.5 | Gemini3.1ProPreview | llm-grading tsv | 9 |
| Gemini3.1ProPreview | Claude4.5Sonnet | llm-grading tsv | 9 |
| Gemini3.1ProPreview | GPT-5.5 | llm-grading tsv | 9 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | llm-grading tsv | 9 |

### Distribution_of_State_Machine_Elements_Across_Systems.csv

Source CSV: `_Figures/PaperExperimentData/Distribution_of_State_Machine_Elements_Across_Systems.csv`

Source script: `_scripts/compute_element_distribution.py`

Rows: 8

Description: Counts reference/ground-truth state-machine elements by system.

| Component | Bread Maker | Chess Clock | Dishwasher | Printer | SSC7 | Spa Manager | Train Automation | Thermomix TM6 | W-UMPLE | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| States | 12 | 13 | 12 | 8 | 9 | 16 | 17 | 11 | 24 | 122 |
| Transitions | 18 | 14 | 19 | 17 | 23 | 15 | 20 | 17 | 37 | 180 |
| Guards | 4 | 4 | 4 | 6 | 11 | 4 | 14 | 7 | 3 | 57 |
| Actions | 10 | 8 | 7 | 3 | 21 | 0 | 12 | 6 | 36 | 103 |
| Hierarchical States | 3 | 3 | 2 | 2 | 1 | 3 | 2 | 1 | 5 | 22 |
| Parallel Regions | 0 | 2 | 2 | 0 | 0 | 5 | 4 | 0 | 2 | 15 |
| History States | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 9 |
| Total | 48 | 45 | 47 | 37 | 66 | 44 | 70 | 43 | 108 | 508 |

### rq1_generation_quality_summary.csv

Source CSV: `_Figures/PaperExperimentData/rq1_generation_quality_summary.csv`

Source script: `_scripts/summarize_paper_experiments.py`

Rows: 16

Description: Summarizes human assessment of Claude-generated state machines by approach and element type.

| approach | model_element | examples | precision | recall | f1 |
| --- | --- | --- | --- | --- | --- |
| one-stage | Composite State | 7 | 1.0 | 0.8809523809476191 | 0.926406926412987 |
| one-stage | State | 7 | 1.0 | 0.7655620523346948 | 0.86137193437853 |
| one-stage | Transition | 7 | 1.0 | 0.664126001272269 | 0.7877856852956925 |
| one-stage | Action | 7 | 1.0 | 0.5257936507944444 | 0.6781103720229121 |
| one-stage | Region | 7 | 1.0 | 0.625 | 0.8888888889 |
| one-stage | History State | 7 | 1.0 | 0.42857142857142855 | 1.0 |
| one-stage | Guard | 7 | 1.0 | 0.5501700680224489 | 0.7645343232797225 |
| one-stage | Overall Score | 7 | 1.0 | 0.66493490471733 | 0.7907300375775952 |
| two-stage (6 examples) | Composite State | 9 | 1.0 | 0.8518518518555556 | 0.975 |
| two-stage (6 examples) | State | 9 | 1.0 | 0.8696190791873303 | 0.9252391518154446 |
| two-stage (6 examples) | Transition | 9 | 1.0 | 0.8862676438825398 | 0.9181970657789174 |
| two-stage (6 examples) | Action | 9 | 1.0 | 0.7392361111125 | 0.8168645215632653 |
| two-stage (6 examples) | Region | 9 | 1.0 | 0.9 | 0.93333333334 |
| two-stage (6 examples) | History State | 9 | 0.8666666666599999 | 0.6666666666666666 | 0.9 |
| two-stage (6 examples) | Guard | 9 | 1.0 | 0.7559523809555555 | 0.8894819466204081 |
| two-stage (6 examples) | Overall Score | 9 | 0.9973386560222222 | 0.8329705781262786 | 0.9027605792366901 |

### rq1_generation_quality_by_example.csv

Source CSV: `_Figures/PaperExperimentData/rq1_generation_quality_by_example.csv`

Source script: `_scripts/summarize_paper_experiments.py`

Rows: 184

Description: Per-system RQ1 human-assessment metrics used to build the RQ1 summary.

| approach | project | model_element | precision | recall | f1 |
| --- | --- | --- | --- | --- | --- |
| one-stage | Automatic Bread Maker | Composite State | 1.0 | 0.8333333333 | 0.9090909091 |
| one-stage | Automatic Bread Maker | State | 1.0 | 0.875 | 0.9333333333 |
| one-stage | Automatic Bread Maker | Transition | 1.0 | 0.8611111111 | 0.9253731343 |
| one-stage | Automatic Bread Maker | Action | 1.0 | 0.5 | 0.6666666667 |
| one-stage | Automatic Bread Maker | Region |  |  |  |
| one-stage | Automatic Bread Maker | History State |  | 0.0 |  |
| one-stage | Automatic Bread Maker | Guard | 1.0 | 0.75 | 0.8571428571 |
| one-stage | Automatic Bread Maker | Overall Score | 1.0 | 0.7604166667 | 0.8639053254 |
| two-stage (3 examples) | Automatic Bread Maker | Composite State | 1.0 | 1.0 | 1.0 |
| two-stage (3 examples) | Automatic Bread Maker | State | 1.0 | 0.6666666667 | 0.8 |
| two-stage (3 examples) | Automatic Bread Maker | Transition | 1.0 | 0.6944444444 | 0.8196721311 |
| two-stage (3 examples) | Automatic Bread Maker | Action | 1.0 | 0.7 | 0.8235294118 |
| two-stage (3 examples) | Automatic Bread Maker | Region |  |  |  |
| two-stage (3 examples) | Automatic Bread Maker | History State |  | 0.0 |  |
| two-stage (3 examples) | Automatic Bread Maker | Guard | 1.0 | 1.0 | 1.0 |
| two-stage (3 examples) | Automatic Bread Maker | Overall Score | 1.0 | 0.71875 | 0.8363636364 |
| two-stage (6 examples) | Automatic Bread Maker | Composite State | 1.0 | 0.6666666667 | 0.8 |
| two-stage (6 examples) | Automatic Bread Maker | State | 1.0 | 0.6666666667 | 0.8 |
| two-stage (6 examples) | Automatic Bread Maker | Transition | 1.0 | 0.7777777778 | 0.875 |
| two-stage (6 examples) | Automatic Bread Maker | Action | 1.0 | 0.9 | 0.9473684211 |
| two-stage (6 examples) | Automatic Bread Maker | Region |  |  |  |
| two-stage (6 examples) | Automatic Bread Maker | History State |  | 0.0 |  |
| two-stage (6 examples) | Automatic Bread Maker | Guard | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Automatic Bread Maker | Overall Score | 1.0 | 0.7708333333 | 0.8705882353 |
| one-stage | Digital Chess Clock | Composite State | 1.0 | 0.8333333333333334 | 0.9090909090909091 |
| one-stage | Digital Chess Clock | State | 1.0 | 0.5769230769230769 | 0.7317073170731707 |
| one-stage | Digital Chess Clock | Transition | 1.0 | 0.75 | 0.8571428571428571 |
| one-stage | Digital Chess Clock | Action | 1.0 | 0.375 | 0.5454545454545454 |
| one-stage | Digital Chess Clock | Region |  | 0.0 |  |
| one-stage | Digital Chess Clock | History State |  | 1.0 |  |
| one-stage | Digital Chess Clock | Guard |  | 0.0 |  |
| one-stage | Digital Chess Clock | Overall Score | 1.0 | 0.5444444444444444 | 0.7050359712230216 |
| two-stage (3 examples) | Digital Chess Clock | Composite State | 1.0 | 1.0 | 1.0 |
| two-stage (3 examples) | Digital Chess Clock | State | 1.0 | 0.8461538461538461 | 0.9166666666666666 |
| two-stage (3 examples) | Digital Chess Clock | Transition | 0.9230769230769231 | 0.8571428571428571 | 0.888888888888889 |
| two-stage (3 examples) | Digital Chess Clock | Action | 1.0 | 1.0 | 1.0 |
| two-stage (3 examples) | Digital Chess Clock | Region | 1.0 | 0.75 | 0.8571428571428571 |
| two-stage (3 examples) | Digital Chess Clock | History State |  | 1.0 |  |
| two-stage (3 examples) | Digital Chess Clock | Guard | 1.0 | 1.0 | 1.0 |
| two-stage (3 examples) | Digital Chess Clock | Overall Score | 0.9759036144578314 | 0.9 | 0.9364161849710982 |
| two-stage (6 examples) | Digital Chess Clock | Composite State | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Digital Chess Clock | State | 1.0 | 0.8846153846153846 | 0.9387755102040816 |
| two-stage (6 examples) | Digital Chess Clock | Transition | 1.0 | 0.8571428571428571 | 0.923076923076923 |
| two-stage (6 examples) | Digital Chess Clock | Action | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Digital Chess Clock | Region | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Digital Chess Clock | History State |  | 1.0 |  |
| two-stage (6 examples) | Digital Chess Clock | Guard | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Digital Chess Clock | Overall Score | 1.0 | 0.9222222222222223 | 0.9595375722543353 |
| one-stage | Dishwasher | Composite State | 1.0 | 1.0 | 1.0 |
| one-stage | Dishwasher | State | 1.0 | 0.6666666667 | 0.8 |
| one-stage | Dishwasher | Transition | 1.0 | 0.5789473684 | 0.7333333333 |
| one-stage | Dishwasher | Action | 1.0 | 0.5714285714 | 0.7272727273 |
| one-stage | Dishwasher | Region | 1.0 | 0.5 | 0.6666666667 |
| one-stage | Dishwasher | History State |  | 0.0 |  |
| one-stage | Dishwasher | Guard | 1.0 | 0.625 | 0.7692307692 |
| one-stage | Dishwasher | Overall Score | 1.0 | 0.6063829787 | 0.7549668874 |
| two-stage (3 examples) | Dishwasher | Composite State | 0.6666666667 | 1.0 | 0.8 |
| two-stage (3 examples) | Dishwasher | State | 1.0 | 1.0 | 1.0 |
| two-stage (3 examples) | Dishwasher | Transition | 1.0 | 0.9736842105 | 0.9866666667 |
| two-stage (3 examples) | Dishwasher | Action | 1.0 | 0.8571428571 | 0.9230769231 |
| two-stage (3 examples) | Dishwasher | Region | 1.0 | 1.0 | 1.0 |
| two-stage (3 examples) | Dishwasher | History State | 1.0 | 0.5 | 0.6666666667 |
| two-stage (3 examples) | Dishwasher | Guard | 1.0 | 0.875 | 0.9333333333 |
| two-stage (3 examples) | Dishwasher | Overall Score | 0.978021978 | 0.9468085106 | 0.9621621622 |
| two-stage (6 examples) | Dishwasher | Composite State | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Dishwasher | State | 1.0 | 0.6666666667 | 0.8 |
| two-stage (6 examples) | Dishwasher | Transition | 1.0 | 0.7105263158 | 0.8307692308 |
| two-stage (6 examples) | Dishwasher | Action | 1.0 | 0.7857142857 | 0.88 |
| two-stage (6 examples) | Dishwasher | Region | 1.0 | 0.5 | 0.6666666667 |
| two-stage (6 examples) | Dishwasher | History State |  | 0.0 |  |
| two-stage (6 examples) | Dishwasher | Guard | 1.0 | 0.625 | 0.7692307692 |
| two-stage (6 examples) | Dishwasher | Overall Score | 1.0 | 0.6914893617 | 0.8176100629 |
| one-stage | Printer | Composite State | 1.0 | 0.5 | 0.6666666667 |
| one-stage | Printer | State | 1.0 | 0.7777777778 | 0.875 |
| one-stage | Printer | Transition | 1.0 | 0.5294117647 | 0.6923076923 |
| one-stage | Printer | Action | 1.0 | 0.6666666667 | 0.8 |
| one-stage | Printer | Region |  |  |  |
| one-stage | Printer | History State | 1.0 | 1.0 | 1.0 |
| one-stage | Printer | Guard | 1.0 | 0.5833333333 | 0.7368421053 |
| one-stage | Printer | Overall Score | 1.0 | 0.6184210526 | 0.7642276423 |
| two-stage (3 examples) | Printer | Composite State | 0.5 | 1.0 | 0.6666666667 |
| two-stage (3 examples) | Printer | State | 0.6666666667 | 1.0 | 0.8 |
| two-stage (3 examples) | Printer | Transition | 1.0 | 1.0 | 1.0 |
| two-stage (3 examples) | Printer | Action | 1.0 | 1.0 | 1.0 |
| two-stage (3 examples) | Printer | Region |  |  |  |
| two-stage (3 examples) | Printer | History State | 0.5 | 1.0 | 0.6666666667 |
| two-stage (3 examples) | Printer | Guard | 1.0 | 1.0 | 1.0 |
| two-stage (3 examples) | Printer | Overall Score | 0.8409090909 | 1.0 | 0.9135802469 |
| two-stage (6 examples) | Printer | Composite State | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Printer | State | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Printer | Transition | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Printer | Action | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Printer | Region |  |  |  |
| two-stage (6 examples) | Printer | History State | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Printer | Guard | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Printer | Overall Score | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | SSC7 | Composite State | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | SSC7 | State | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | SSC7 | Transition | 1.0 | 1.0 | 0.8333333333 |
| two-stage (6 examples) | SSC7 | Action | 1.0 | 0.7142857143 |  |
| two-stage (6 examples) | SSC7 | Region |  |  |  |
| two-stage (6 examples) | SSC7 | History State | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | SSC7 | Guard | 1.0 | 1.0 |  |
| two-stage (6 examples) | SSC7 | Overall Score | 1.0 | 0.8939393939 | 0.944 |
| one-stage | Spa Manager | Composite State | 1.0 | 1.0 | 1.0 |
| one-stage | Spa Manager | State | 1.0 | 1.0 | 1.0 |
| one-stage | Spa Manager | Transition | 1.0 | 0.9 | 0.9473684210526316 |
| one-stage | Spa Manager | Action |  |  |  |
| one-stage | Spa Manager | Region | 1.0 | 1.0 | 1.0 |
| one-stage | Spa Manager | History State | 1.0 | 1.0 | 1.0 |
| one-stage | Spa Manager | Guard | 1.0 | 1.0 | 1.0 |
| one-stage | Spa Manager | Overall Score | 1.0 | 0.9659090909090909 | 0.9826589595375723 |
| two-stage (3 examples) | Spa Manager | Composite State | 1.0 | 1.0 | 1.0 |
| two-stage (3 examples) | Spa Manager | State | 0.8888888889 | 1.0 | 0.9411764706 |
| two-stage (3 examples) | Spa Manager | Transition | 1.0 | 0.9666666667 | 0.9830508475 |
| two-stage (3 examples) | Spa Manager | Action |  |  |  |
| two-stage (3 examples) | Spa Manager | Region | 0.8333333333 | 1.0 | 0.9090909091 |
| two-stage (3 examples) | Spa Manager | History State | 1.0 | 1.0 | 1.0 |
| two-stage (3 examples) | Spa Manager | Guard | 1.0 | 0.75 | 0.8571428571 |
| two-stage (3 examples) | Spa Manager | Overall Score | 0.9340659341 | 0.9659090909 | 0.9497206704 |
| two-stage (6 examples) | Spa Manager | Composite State | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Spa Manager | State | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Spa Manager | Transition | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Spa Manager | Action |  |  |  |
| two-stage (6 examples) | Spa Manager | Region | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Spa Manager | History State | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Spa Manager | Guard | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Spa Manager | Overall Score | 1.0 | 1.0 | 1.0 |
| one-stage | Thermomix TM6 | Composite State | 1.0 | 1.0 | 1.0 |
| one-stage | Thermomix TM6 | State | 1.0 | 0.7272727272727273 | 0.8421052631578948 |
| one-stage | Thermomix TM6 | Transition | 1.0 | 0.5294117647058824 | 0.6923076923076924 |
| one-stage | Thermomix TM6 | Action | 1.0 | 0.3333333333333333 | 0.5 |
| one-stage | Thermomix TM6 | Region |  |  |  |
| one-stage | Thermomix TM6 | History State |  | 0.0 |  |
| one-stage | Thermomix TM6 | Guard | 1.0 | 0.35714285714285715 | 0.5263157894736842 |
| one-stage | Thermomix TM6 | Overall Score | 1.0 | 0.5232558139534884 | 0.6870229007633588 |
| two-stage (3 examples) | Thermomix TM6 | Composite State | 0.5 | 1.0 | 0.6666666666666666 |
| two-stage (3 examples) | Thermomix TM6 | State | 0.9166666666666666 | 1.0 | 0.9565217391304348 |
| two-stage (3 examples) | Thermomix TM6 | Transition | 1.0 | 0.8823529411764706 | 0.9375 |
| two-stage (3 examples) | Thermomix TM6 | Action | 1.0 | 0.6666666666666666 | 0.8 |
| two-stage (3 examples) | Thermomix TM6 | Region |  |  |  |
| two-stage (3 examples) | Thermomix TM6 | History State |  | 0.0 |  |
| two-stage (3 examples) | Thermomix TM6 | Guard | 1.0 | 0.42857142857142855 | 0.6 |
| two-stage (3 examples) | Thermomix TM6 | Overall Score | 0.9444444444444444 | 0.7906976744186046 | 0.8607594936708861 |
| two-stage (6 examples) | Thermomix TM6 | Composite State |  | 0.0 |  |
| two-stage (6 examples) | Thermomix TM6 | State | 1.0 | 0.8181818182 | 0.9 |
| two-stage (6 examples) | Thermomix TM6 | Transition | 1.0 | 0.8235294118 | 0.9032258065 |
| two-stage (6 examples) | Thermomix TM6 | Action | 1.0 | 0.1666666667 | 0.2857142857 |
| two-stage (6 examples) | Thermomix TM6 | Region |  |  |  |
| two-stage (6 examples) | Thermomix TM6 | History State |  | 0.0 |  |
| two-stage (6 examples) | Thermomix TM6 | Guard | 1.0 | 0.4285714286 | 0.6 |
| two-stage (6 examples) | Thermomix TM6 | Overall Score | 1.0 | 0.6279069767 | 0.7714285714 |
| one-stage | Train Automation System | Composite State | 1.0 | 1.0 | 1.0 |
| one-stage | Train Automation System | State | 1.0 | 0.7352941176470589 | 0.8474576271186441 |
| one-stage | Train Automation System | Transition | 1.0 | 0.5 | 0.6666666666666666 |
| one-stage | Train Automation System | Action | 1.0 | 0.7083333333333334 | 0.8292682926829268 |
| one-stage | Train Automation System | Region | 1.0 | 1.0 | 1.0 |
| one-stage | Train Automation System | History State |  | 0.0 |  |
| one-stage | Train Automation System | Guard | 1.0 | 0.5357142857142857 | 0.6976744186046512 |
| one-stage | Train Automation System | Overall Score | 1.0 | 0.6357142857142857 | 0.7772925764192139 |
| two-stage (3 examples) | Train Automation System | Composite State | 1.0 | 1.0 | 1.0 |
| two-stage (3 examples) | Train Automation System | State | 0.9333333333 | 0.8235294118 | 0.875 |
| two-stage (3 examples) | Train Automation System | Transition | 0.9166666667 | 0.55 | 0.6875 |
| two-stage (3 examples) | Train Automation System | Action | 1.0 | 0.7083333333 | 0.8292682927 |
| two-stage (3 examples) | Train Automation System | Region | 1.0 | 1.0 | 1.0 |
| two-stage (3 examples) | Train Automation System | History State | 1.0 | 1.0 | 1.0 |
| two-stage (3 examples) | Train Automation System | Guard | 0.8666666667 | 0.4642857143 | 0.6046511628 |
| two-stage (3 examples) | Train Automation System | Overall Score | 0.94 | 0.6714285714 | 0.7833333333 |
| two-stage (6 examples) | Train Automation System | Composite State | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Train Automation System | State | 1.0 | 0.8529411764705882 | 0.9206349206349206 |
| two-stage (6 examples) | Train Automation System | Transition | 1.0 | 0.875 | 0.9333333333333333 |
| two-stage (6 examples) | Train Automation System | Action | 1.0 | 0.75 | 0.8571428571428571 |
| two-stage (6 examples) | Train Automation System | Region | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Train Automation System | History State | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Train Automation System | Guard | 1.0 | 0.75 | 0.8571428571428571 |
| two-stage (6 examples) | Train Automation System | Overall Score | 1.0 | 0.8357142857142857 | 0.9105058365758755 |
| two-stage (6 examples) | Wumple | Composite State | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Wumple | State | 1.0 | 0.9375 | 0.9677419355 |
| two-stage (6 examples) | Wumple | Transition | 1.0 | 0.9324324324 | 0.965034965 |
| two-stage (6 examples) | Wumple | Action | 1.0 | 0.5972222222 | 0.747826087 |
| two-stage (6 examples) | Wumple | Region | 1.0 | 1.0 | 1.0 |
| two-stage (6 examples) | Wumple | History State | 0.3333333333 | 1.0 | 0.5 |
| two-stage (6 examples) | Wumple | Guard |  | 0.0 |  |
| two-stage (6 examples) | Wumple | Overall Score | 0.9760479042 | 0.7546296296 | 0.8511749347 |

### rq2_grading_quality_summary.csv

Source CSV: `_Figures/PaperExperimentData/rq2_grading_quality_summary.csv`

Source script: `_scripts/summarize_paper_experiments.py`

Rows: 24

Description: Human-vs-LLM agreement metrics computed from workbook weighted-kappa sheets.

| grader | model_element | items | exact_agreement | macro_precision | macro_recall | macro_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| Claude4.5Sonnet | Composite State | 31 | 0.8387096774193549 | 0.731578947368421 | 0.8833333333333333 | 0.7794871794871795 |
| Claude4.5Sonnet | State | 131 | 0.8257575757575758 | 0.5483131646497983 | 0.564021164021164 | 0.5397394407103145 |
| Claude4.5Sonnet | Transition | 189 | 0.8253968253968254 | 0.5214285714285715 | 0.6183760683760684 | 0.551431734765068 |
| Claude4.5Sonnet | Action | 112 | 0.6428571428571429 | 0.5573987365291714 | 0.5491634491634492 | 0.5106456164665593 |
| Claude4.5Sonnet | Region | 24 | 0.9583333333333334 | 0.9583333333333333 | 0.9615384615384616 | 0.9582608695652175 |
| Claude4.5Sonnet | History State | 18 | 0.7368421052631579 | 0.5714285714285715 | 0.5 | 0.75 |
| Claude4.5Sonnet | Guard | 66 | 0.7727272727272727 | 0.6848214285714286 | 0.7502334267040149 | 0.6945516945516945 |
| Claude4.5Sonnet | Overall Score | 571 | 0.787085514834206 | 0.5830921937823458 | 0.6383881230116649 | 0.5990486792925486 |
| GPT-5.5 | Composite State | 31 | 0.9032258064516129 | 0.75 | 0.9333333333333332 | 0.7649122807017544 |
| GPT-5.5 | State | 131 | 0.8931297709923665 | 0.7055205520552055 | 0.7369436663554311 | 0.7165673339288418 |
| GPT-5.5 | Transition | 189 | 0.8359788359788359 | 0.6225374310480692 | 0.682051282051282 | 0.637406586187074 |
| GPT-5.5 | Action | 112 | 0.6785714285714286 | 0.6531885824009452 | 0.6732303732303732 | 0.544799479002542 |
| GPT-5.5 | Region | 24 | 0.9583333333333334 | 0.6666666666666666 | 0.9545454545454546 | 0.9761904761904762 |
| GPT-5.5 | History State | 18 | 0.7894736842105263 | 0.5555555555555556 | 0.5416666666666666 | 0.8116883116883117 |
| GPT-5.5 | Guard | 66 | 0.803030303030303 | 0.6803751803751803 | 0.6237161531279178 | 0.614977614977615 |
| GPT-5.5 | Overall Score | 571 | 0.8216783216783217 | 0.6440048817012847 | 0.6794171220400728 | 0.6457093014133911 |
| Gemini3.1ProPreview | Composite State | 31 | 0.9032258064516129 | 0.7727272727272728 | 0.9333333333333332 | 0.8237259816207185 |
| Gemini3.1ProPreview | State | 131 | 0.9083969465648855 | 0.7426984126984126 | 0.7761593526299407 | 0.7487804878048779 |
| Gemini3.1ProPreview | Transition | 189 | 0.8783068783068783 | 0.6278166278166278 | 0.7247863247863248 | 0.6603983929660714 |
| Gemini3.1ProPreview | Action | 112 | 0.6964285714285714 | 0.5207631874298541 | 0.4903474903474903 | 0.748904818797292 |
| Gemini3.1ProPreview | Region | 24 | 0.9583333333333334 | 0.9583333333333333 | 0.9615384615384616 | 0.9582608695652175 |
| Gemini3.1ProPreview | History State | 18 | 0.7894736842105263 | 0.8571428571428572 | 0.5416666666666666 | 0.8012820512820513 |
| Gemini3.1ProPreview | Guard | 66 | 0.8333333333333334 | 0.7134502923976608 | 0.7026143790849674 | 0.6897080561714709 |
| Gemini3.1ProPreview | Overall Score | 571 | 0.8461538461538461 | 0.6438744299855411 | 0.6927417438821574 | 0.6618835821949239 |

### rq2_confusion_matrices.csv

Source CSV: `_Figures/PaperExperimentData/rq2_confusion_matrices.csv`

Source script: `_scripts/summarize_paper_experiments.py`

Rows: 216

Description: Human-vs-LLM score confusion counts by grader and model element.

| grader | model_element | human_score | llm_score | count |
| --- | --- | --- | --- | --- |
| Claude4.5Sonnet | Action | 0.0 | 0.0 | 34 |
| Claude4.5Sonnet | Action | 0.0 | 0.5 | 2 |
| Claude4.5Sonnet | Action | 0.0 | 1.0 | 1 |
| Claude4.5Sonnet | Action | 0.5 | 0.0 | 3 |
| Claude4.5Sonnet | Action | 0.5 | 0.5 | 1 |
| Claude4.5Sonnet | Action | 0.5 | 1.0 | 1 |
| Claude4.5Sonnet | Action | 1.0 | 0.0 | 13 |
| Claude4.5Sonnet | Action | 1.0 | 0.5 | 20 |
| Claude4.5Sonnet | Action | 1.0 | 1.0 | 37 |
| Claude4.5Sonnet | Composite State | 0.0 | 0.0 | 8 |
| Claude4.5Sonnet | Composite State | 0.0 | 0.5 | 0 |
| Claude4.5Sonnet | Composite State | 0.0 | 1.0 | 2 |
| Claude4.5Sonnet | Composite State | 0.5 | 0.0 | 0 |
| Claude4.5Sonnet | Composite State | 0.5 | 0.5 | 1 |
| Claude4.5Sonnet | Composite State | 0.5 | 1.0 | 0 |
| Claude4.5Sonnet | Composite State | 1.0 | 0.0 | 2 |
| Claude4.5Sonnet | Composite State | 1.0 | 0.5 | 1 |
| Claude4.5Sonnet | Composite State | 1.0 | 1.0 | 17 |
| Claude4.5Sonnet | Guard | 0.0 | 0.0 | 16 |
| Claude4.5Sonnet | Guard | 0.0 | 0.5 | 0 |
| Claude4.5Sonnet | Guard | 0.0 | 1.0 | 1 |
| Claude4.5Sonnet | Guard | 0.5 | 0.0 | 3 |
| Claude4.5Sonnet | Guard | 0.5 | 0.5 | 4 |
| Claude4.5Sonnet | Guard | 0.5 | 1.0 | 0 |
| Claude4.5Sonnet | Guard | 1.0 | 0.0 | 1 |
| Claude4.5Sonnet | Guard | 1.0 | 0.5 | 10 |
| Claude4.5Sonnet | Guard | 1.0 | 1.0 | 31 |
| Claude4.5Sonnet | History State | 0.0 | 0.0 | 10 |
| Claude4.5Sonnet | History State | 0.0 | 0.5 | 0 |
| Claude4.5Sonnet | History State | 0.0 | 1.0 | 0 |
| Claude4.5Sonnet | History State | 0.5 | 0.0 | 1 |
| Claude4.5Sonnet | History State | 0.5 | 0.5 | 0 |
| Claude4.5Sonnet | History State | 0.5 | 1.0 | 0 |
| Claude4.5Sonnet | History State | 1.0 | 0.0 | 3 |
| Claude4.5Sonnet | History State | 1.0 | 0.5 | 1 |
| Claude4.5Sonnet | History State | 1.0 | 1.0 | 4 |
| Claude4.5Sonnet | Overall Score | 0.0 | 0.0 | 109 |
| Claude4.5Sonnet | Overall Score | 0.0 | 0.5 | 3 |
| Claude4.5Sonnet | Overall Score | 0.0 | 1.0 | 11 |
| Claude4.5Sonnet | Overall Score | 0.5 | 0.0 | 26 |
| Claude4.5Sonnet | Overall Score | 0.5 | 0.5 | 8 |
| Claude4.5Sonnet | Overall Score | 0.5 | 1.0 | 2 |
| Claude4.5Sonnet | Overall Score | 1.0 | 0.0 | 33 |
| Claude4.5Sonnet | Overall Score | 1.0 | 0.5 | 47 |
| Claude4.5Sonnet | Overall Score | 1.0 | 1.0 | 334 |
| Claude4.5Sonnet | Region | 0.0 | 0.0 | 11 |
| Claude4.5Sonnet | Region | 0.0 | 0.5 | 0 |
| Claude4.5Sonnet | Region | 0.0 | 1.0 | 0 |
| Claude4.5Sonnet | Region | 0.5 | 0.0 | 0 |
| Claude4.5Sonnet | Region | 0.5 | 0.5 | 0 |
| Claude4.5Sonnet | Region | 0.5 | 1.0 | 0 |
| Claude4.5Sonnet | Region | 1.0 | 0.0 | 1 |
| Claude4.5Sonnet | Region | 1.0 | 0.5 | 0 |
| Claude4.5Sonnet | Region | 1.0 | 1.0 | 12 |
| Claude4.5Sonnet | State | 0.0 | 0.0 | 12 |
| Claude4.5Sonnet | State | 0.0 | 0.5 | 1 |
| Claude4.5Sonnet | State | 0.0 | 1.0 | 5 |
| Claude4.5Sonnet | State | 0.5 | 0.0 | 8 |
| Claude4.5Sonnet | State | 0.5 | 0.5 | 1 |
| Claude4.5Sonnet | State | 0.5 | 1.0 | 0 |
| Claude4.5Sonnet | State | 1.0 | 0.0 | 7 |
| Claude4.5Sonnet | State | 1.0 | 0.5 | 2 |
| Claude4.5Sonnet | State | 1.0 | 1.0 | 96 |
| Claude4.5Sonnet | Transition | 0.0 | 0.0 | 18 |
| Claude4.5Sonnet | Transition | 0.0 | 0.5 | 0 |
| Claude4.5Sonnet | Transition | 0.0 | 1.0 | 2 |
| Claude4.5Sonnet | Transition | 0.5 | 0.0 | 11 |
| Claude4.5Sonnet | Transition | 0.5 | 0.5 | 1 |
| Claude4.5Sonnet | Transition | 0.5 | 1.0 | 1 |
| Claude4.5Sonnet | Transition | 1.0 | 0.0 | 6 |
| Claude4.5Sonnet | Transition | 1.0 | 0.5 | 13 |
| Claude4.5Sonnet | Transition | 1.0 | 1.0 | 137 |
| GPT-5.5 | Action | 0.0 | 0.0 | 15 |
| GPT-5.5 | Action | 0.0 | 0.5 | 21 |
| GPT-5.5 | Action | 0.0 | 1.0 | 1 |
| GPT-5.5 | Action | 0.5 | 0.0 | 0 |
| GPT-5.5 | Action | 0.5 | 0.5 | 4 |
| GPT-5.5 | Action | 0.5 | 1.0 | 1 |
| GPT-5.5 | Action | 1.0 | 0.0 | 2 |
| GPT-5.5 | Action | 1.0 | 0.5 | 11 |
| GPT-5.5 | Action | 1.0 | 1.0 | 57 |
| GPT-5.5 | Composite State | 0.0 | 0.0 | 9 |
| GPT-5.5 | Composite State | 0.0 | 0.5 | 1 |
| GPT-5.5 | Composite State | 0.0 | 1.0 | 0 |
| GPT-5.5 | Composite State | 0.5 | 0.0 | 0 |
| GPT-5.5 | Composite State | 0.5 | 0.5 | 1 |
| GPT-5.5 | Composite State | 0.5 | 1.0 | 0 |
| GPT-5.5 | Composite State | 1.0 | 0.0 | 0 |
| GPT-5.5 | Composite State | 1.0 | 0.5 | 2 |
| GPT-5.5 | Composite State | 1.0 | 1.0 | 18 |
| GPT-5.5 | Guard | 0.0 | 0.0 | 14 |
| GPT-5.5 | Guard | 0.0 | 0.5 | 0 |
| GPT-5.5 | Guard | 0.0 | 1.0 | 3 |
| GPT-5.5 | Guard | 0.5 | 0.0 | 5 |
| GPT-5.5 | Guard | 0.5 | 0.5 | 1 |
| GPT-5.5 | Guard | 0.5 | 1.0 | 1 |
| GPT-5.5 | Guard | 1.0 | 0.0 | 3 |
| GPT-5.5 | Guard | 1.0 | 0.5 | 1 |
| GPT-5.5 | Guard | 1.0 | 1.0 | 38 |
| GPT-5.5 | History State | 0.0 | 0.0 | 10 |
| GPT-5.5 | History State | 0.0 | 0.5 | 0 |
| GPT-5.5 | History State | 0.0 | 1.0 | 0 |
| GPT-5.5 | History State | 0.5 | 0.0 | 0 |
| GPT-5.5 | History State | 0.5 | 0.5 | 0 |
| GPT-5.5 | History State | 0.5 | 1.0 | 1 |
| GPT-5.5 | History State | 1.0 | 0.0 | 2 |
| GPT-5.5 | History State | 1.0 | 0.5 | 1 |
| GPT-5.5 | History State | 1.0 | 1.0 | 5 |
| GPT-5.5 | Overall Score | 0.0 | 0.0 | 86 |
| GPT-5.5 | Overall Score | 0.0 | 0.5 | 28 |
| GPT-5.5 | Overall Score | 0.0 | 1.0 | 8 |
| GPT-5.5 | Overall Score | 0.5 | 0.0 | 16 |
| GPT-5.5 | Overall Score | 0.5 | 0.5 | 16 |
| GPT-5.5 | Overall Score | 0.5 | 1.0 | 4 |
| GPT-5.5 | Overall Score | 1.0 | 0.0 | 11 |
| GPT-5.5 | Overall Score | 1.0 | 0.5 | 35 |
| GPT-5.5 | Overall Score | 1.0 | 1.0 | 368 |
| GPT-5.5 | Region | 0.0 | 0.0 | 10 |
| GPT-5.5 | Region | 0.0 | 0.5 | 1 |
| GPT-5.5 | Region | 0.0 | 1.0 | 0 |
| GPT-5.5 | Region | 0.5 | 0.0 | 0 |
| GPT-5.5 | Region | 0.5 | 0.5 | 0 |
| GPT-5.5 | Region | 0.5 | 1.0 | 0 |
| GPT-5.5 | Region | 1.0 | 0.0 | 0 |
| GPT-5.5 | Region | 1.0 | 0.5 | 0 |
| GPT-5.5 | Region | 1.0 | 1.0 | 13 |
| GPT-5.5 | State | 0.0 | 0.0 | 14 |
| GPT-5.5 | State | 0.0 | 0.5 | 1 |
| GPT-5.5 | State | 0.0 | 1.0 | 2 |
| GPT-5.5 | State | 0.5 | 0.0 | 5 |
| GPT-5.5 | State | 0.5 | 0.5 | 4 |
| GPT-5.5 | State | 0.5 | 1.0 | 0 |
| GPT-5.5 | State | 1.0 | 0.0 | 3 |
| GPT-5.5 | State | 1.0 | 0.5 | 3 |
| GPT-5.5 | State | 1.0 | 1.0 | 99 |
| GPT-5.5 | Transition | 0.0 | 0.0 | 14 |
| GPT-5.5 | Transition | 0.0 | 0.5 | 4 |
| GPT-5.5 | Transition | 0.0 | 1.0 | 2 |
| GPT-5.5 | Transition | 0.5 | 0.0 | 6 |
| GPT-5.5 | Transition | 0.5 | 0.5 | 6 |
| GPT-5.5 | Transition | 0.5 | 1.0 | 1 |
| GPT-5.5 | Transition | 1.0 | 0.0 | 1 |
| GPT-5.5 | Transition | 1.0 | 0.5 | 17 |
| GPT-5.5 | Transition | 1.0 | 1.0 | 138 |
| Gemini3.1ProPreview | Action | 0.0 | 0.0 | 28 |
| Gemini3.1ProPreview | Action | 0.0 | 0.5 | 7 |
| Gemini3.1ProPreview | Action | 0.0 | 1.0 | 2 |
| Gemini3.1ProPreview | Action | 0.5 | 0.0 | 3 |
| Gemini3.1ProPreview | Action | 0.5 | 0.5 | 0 |
| Gemini3.1ProPreview | Action | 0.5 | 1.0 | 2 |
| Gemini3.1ProPreview | Action | 1.0 | 0.0 | 13 |
| Gemini3.1ProPreview | Action | 1.0 | 0.5 | 7 |
| Gemini3.1ProPreview | Action | 1.0 | 1.0 | 50 |
| Gemini3.1ProPreview | Composite State | 0.0 | 0.0 | 9 |
| Gemini3.1ProPreview | Composite State | 0.0 | 0.5 | 1 |
| Gemini3.1ProPreview | Composite State | 0.0 | 1.0 | 0 |
| Gemini3.1ProPreview | Composite State | 0.5 | 0.0 | 0 |
| Gemini3.1ProPreview | Composite State | 0.5 | 0.5 | 1 |
| Gemini3.1ProPreview | Composite State | 0.5 | 1.0 | 0 |
| Gemini3.1ProPreview | Composite State | 1.0 | 0.0 | 2 |
| Gemini3.1ProPreview | Composite State | 1.0 | 0.5 | 0 |
| Gemini3.1ProPreview | Composite State | 1.0 | 1.0 | 18 |
| Gemini3.1ProPreview | Guard | 0.0 | 0.0 | 16 |
| Gemini3.1ProPreview | Guard | 0.0 | 0.5 | 0 |
| Gemini3.1ProPreview | Guard | 0.0 | 1.0 | 1 |
| Gemini3.1ProPreview | Guard | 0.5 | 0.0 | 5 |
| Gemini3.1ProPreview | Guard | 0.5 | 0.5 | 2 |
| Gemini3.1ProPreview | Guard | 0.5 | 1.0 | 0 |
| Gemini3.1ProPreview | Guard | 1.0 | 0.0 | 3 |
| Gemini3.1ProPreview | Guard | 1.0 | 0.5 | 2 |
| Gemini3.1ProPreview | Guard | 1.0 | 1.0 | 37 |
| Gemini3.1ProPreview | History State | 0.0 | 0.0 | 10 |
| Gemini3.1ProPreview | History State | 0.0 | 0.5 | 0 |
| Gemini3.1ProPreview | History State | 0.0 | 1.0 | 0 |
| Gemini3.1ProPreview | History State | 0.5 | 0.0 | 1 |
| Gemini3.1ProPreview | History State | 0.5 | 0.5 | 0 |
| Gemini3.1ProPreview | History State | 0.5 | 1.0 | 0 |
| Gemini3.1ProPreview | History State | 1.0 | 0.0 | 3 |
| Gemini3.1ProPreview | History State | 1.0 | 0.5 | 0 |
| Gemini3.1ProPreview | History State | 1.0 | 1.0 | 5 |
| Gemini3.1ProPreview | Overall Score | 0.0 | 0.0 | 109 |
| Gemini3.1ProPreview | Overall Score | 0.0 | 0.5 | 9 |
| Gemini3.1ProPreview | Overall Score | 0.0 | 1.0 | 4 |
| Gemini3.1ProPreview | Overall Score | 0.5 | 0.0 | 23 |
| Gemini3.1ProPreview | Overall Score | 0.5 | 0.5 | 11 |
| Gemini3.1ProPreview | Overall Score | 0.5 | 1.0 | 2 |
| Gemini3.1ProPreview | Overall Score | 1.0 | 0.0 | 30 |
| Gemini3.1ProPreview | Overall Score | 1.0 | 0.5 | 20 |
| Gemini3.1ProPreview | Overall Score | 1.0 | 1.0 | 364 |
| Gemini3.1ProPreview | Region | 0.0 | 0.0 | 11 |
| Gemini3.1ProPreview | Region | 0.0 | 0.5 | 0 |
| Gemini3.1ProPreview | Region | 0.0 | 1.0 | 0 |
| Gemini3.1ProPreview | Region | 0.5 | 0.0 | 0 |
| Gemini3.1ProPreview | Region | 0.5 | 0.5 | 0 |
| Gemini3.1ProPreview | Region | 0.5 | 1.0 | 0 |
| Gemini3.1ProPreview | Region | 1.0 | 0.0 | 1 |
| Gemini3.1ProPreview | Region | 1.0 | 0.5 | 0 |
| Gemini3.1ProPreview | Region | 1.0 | 1.0 | 12 |
| Gemini3.1ProPreview | State | 0.0 | 0.0 | 16 |
| Gemini3.1ProPreview | State | 0.0 | 0.5 | 0 |
| Gemini3.1ProPreview | State | 0.0 | 1.0 | 1 |
| Gemini3.1ProPreview | State | 0.5 | 0.0 | 5 |
| Gemini3.1ProPreview | State | 0.5 | 0.5 | 4 |
| Gemini3.1ProPreview | State | 0.5 | 1.0 | 0 |
| Gemini3.1ProPreview | State | 1.0 | 0.0 | 3 |
| Gemini3.1ProPreview | State | 1.0 | 0.5 | 3 |
| Gemini3.1ProPreview | State | 1.0 | 1.0 | 99 |
| Gemini3.1ProPreview | Transition | 0.0 | 0.0 | 19 |
| Gemini3.1ProPreview | Transition | 0.0 | 0.5 | 1 |
| Gemini3.1ProPreview | Transition | 0.0 | 1.0 | 0 |
| Gemini3.1ProPreview | Transition | 0.5 | 0.0 | 9 |
| Gemini3.1ProPreview | Transition | 0.5 | 0.5 | 4 |
| Gemini3.1ProPreview | Transition | 0.5 | 1.0 | 0 |
| Gemini3.1ProPreview | Transition | 1.0 | 0.0 | 5 |
| Gemini3.1ProPreview | Transition | 1.0 | 0.5 | 8 |
| Gemini3.1ProPreview | Transition | 1.0 | 1.0 | 143 |

### 2stage_6examples_Metrics_CombinedHumanVsLLM.csv

Source CSV: `_Figures/PaperExperimentData/2stage_6examples_Metrics_CombinedHumanVsLLM.csv`

Source script: `_scripts/compute_raw_grading_counts.py`

Rows: 32

Description: Aggregated raw N/TP/FP/FN metrics recomputed directly from raw workbook sheets.

| Grader | ElementType | TotalN | TotalTP | TotalFP | TotalFN | TotalElements | Precision | Recall | F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Human | Action | 103.0 | 72.5 | 0.0 | 30.5 | 103.0 | 1.0 | 0.703883 | 0.826211 |
| Human | Composite State | 22.0 | 20.5 | 0.0 | 1.5 | 22.0 | 1.0 | 0.931818 | 0.964706 |
| Human | Guard | 57.0 | 45.5 | 0.0 | 11.5 | 57.0 | 1.0 | 0.798246 | 0.887805 |
| Human | History State | 9.0 | 6.5 | 2.0 | 2.5 | 11.0 | 0.764706 | 0.722222 | 0.742857 |
| Human | Region | 15.0 | 13.0 | 0.0 | 2.0 | 15.0 | 1.0 | 0.866667 | 0.928571 |
| Human | State | 122.0 | 109.5 | 0.0 | 12.5 | 122.0 | 1.0 | 0.897541 | 0.946004 |
| Human | Transition | 180.0 | 162.5 | 0.0 | 17.5 | 180.0 | 1.0 | 0.902778 | 0.948905 |
| Human | Overall | 508.0 | 430.0 | 2.0 | 78.0 | 510.0 | 0.99537 | 0.846457 | 0.914894 |
| Claude4.5Sonnet | Action | 103.0 | 49.5 | 2.0 | 53.5 | 105.0 | 0.961165 | 0.480583 | 0.640777 |
| Claude4.5Sonnet | Composite State | 22.0 | 17.5 | 2.0 | 4.5 | 24.0 | 0.897436 | 0.795455 | 0.843373 |
| Claude4.5Sonnet | Guard | 57.0 | 37.0 | 0.0 | 20.0 | 57.0 | 1.0 | 0.649123 | 0.787234 |
| Claude4.5Sonnet | History State | 9.0 | 4.5 | 0.0 | 4.5 | 9.0 | 1.0 | 0.5 | 0.666667 |
| Claude4.5Sonnet | Region | 15.0 | 11.0 | 0.0 | 4.0 | 15.0 | 1.0 | 0.733333 | 0.846154 |
| Claude4.5Sonnet | State | 122.0 | 96.5 | 5.0 | 25.5 | 127.0 | 0.950739 | 0.790984 | 0.863535 |
| Claude4.5Sonnet | Transition | 180.0 | 141.0 | 2.0 | 39.0 | 182.0 | 0.986014 | 0.783333 | 0.873065 |
| Claude4.5Sonnet | Overall | 508.0 | 357.0 | 11.0 | 151.0 | 519.0 | 0.970109 | 0.702756 | 0.815068 |
| GPT-5.5 | Action | 103.0 | 77.0 | 0.0 | 26.0 | 103.0 | 1.0 | 0.747573 | 0.855556 |
| GPT-5.5 | Composite State | 22.0 | 20.0 | 0.0 | 2.0 | 22.0 | 1.0 | 0.909091 | 0.952381 |
| GPT-5.5 | Guard | 57.0 | 41.0 | 0.0 | 16.0 | 57.0 | 1.0 | 0.719298 | 0.836735 |
| GPT-5.5 | History State | 9.0 | 6.0 | 0.0 | 3.0 | 9.0 | 1.0 | 0.666667 | 0.8 |
| GPT-5.5 | Region | 15.0 | 14.0 | 0.0 | 1.0 | 15.0 | 1.0 | 0.933333 | 0.965517 |
| GPT-5.5 | State | 122.0 | 103.5 | 0.0 | 18.5 | 122.0 | 1.0 | 0.848361 | 0.91796 |
| GPT-5.5 | Transition | 180.0 | 151.5 | 2.0 | 28.5 | 182.0 | 0.986971 | 0.841667 | 0.908546 |
| GPT-5.5 | Overall | 508.0 | 413.0 | 2.0 | 95.0 | 510.0 | 0.995181 | 0.812992 | 0.894908 |
| Gemini3.1ProPreview | Action | 103.0 | 61.0 | 0.0 | 42.0 | 103.0 | 1.0 | 0.592233 | 0.743902 |
| Gemini3.1ProPreview | Composite State | 22.0 | 19.0 | 0.0 | 3.0 | 22.0 | 1.0 | 0.863636 | 0.926829 |
| Gemini3.1ProPreview | Guard | 57.0 | 39.0 | 0.0 | 18.0 | 57.0 | 1.0 | 0.684211 | 0.8125 |
| Gemini3.1ProPreview | History State | 9.0 | 5.0 | 0.0 | 4.0 | 9.0 | 1.0 | 0.555556 | 0.714286 |
| Gemini3.1ProPreview | Region | 15.0 | 11.0 | 0.0 | 4.0 | 15.0 | 1.0 | 0.733333 | 0.846154 |
| Gemini3.1ProPreview | State | 122.0 | 102.0 | 0.0 | 20.0 | 122.0 | 1.0 | 0.836066 | 0.910714 |
| Gemini3.1ProPreview | Transition | 180.0 | 148.5 | 0.0 | 31.5 | 180.0 | 1.0 | 0.825 | 0.90411 |
| Gemini3.1ProPreview | Overall | 508.0 | 385.5 | 0.0 | 122.5 | 508.0 | 1.0 | 0.758858 | 0.862899 |

### 2stage_6examples_PerExample_RawCounts_CombinedHumanVsLLM.csv

Source CSV: `_Figures/PaperExperimentData/2stage_6examples_PerExample_RawCounts_CombinedHumanVsLLM.csv`

Source script: `_scripts/compute_raw_grading_counts.py`

Rows: 288

Description: Per-system raw N/TP/FP/FN metrics recomputed directly from raw workbook sheets.

| Example | Grader | ElementType | TotalN | TotalTP | TotalFP | TotalFN | TotalElements | Precision | Recall | F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Automatic Bread Maker | Human | Action | 10.0 | 9.0 | 0.0 | 1.0 | 10.0 | 1.0 | 0.9 | 0.947368 |
| Automatic Bread Maker | Human | Composite State | 3.0 | 2.5 | 0.0 | 0.5 | 3.0 | 1.0 | 0.833333 | 0.909091 |
| Automatic Bread Maker | Human | Guard | 4.0 | 4.0 | 0.0 | 0.0 | 4.0 | 1.0 | 1.0 | 1.0 |
| Automatic Bread Maker | Human | History State | 1.0 | 0.5 | 0.0 | 0.5 | 1.0 | 1.0 | 0.5 | 0.666667 |
| Automatic Bread Maker | Human | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Automatic Bread Maker | Human | State | 12.0 | 10.0 | 0.0 | 2.0 | 12.0 | 1.0 | 0.833333 | 0.909091 |
| Automatic Bread Maker | Human | Transition | 18.0 | 16.0 | 0.0 | 2.0 | 18.0 | 1.0 | 0.888889 | 0.941176 |
| Automatic Bread Maker | Human | Overall | 48.0 | 42.0 | 0.0 | 6.0 | 48.0 | 1.0 | 0.875 | 0.933333 |
| Automatic Bread Maker | Claude4.5Sonnet | Action | 10.0 | 7.0 | 0.0 | 3.0 | 10.0 | 1.0 | 0.7 | 0.823529 |
| Automatic Bread Maker | Claude4.5Sonnet | Composite State | 3.0 | 2.5 | 0.0 | 0.5 | 3.0 | 1.0 | 0.833333 | 0.909091 |
| Automatic Bread Maker | Claude4.5Sonnet | Guard | 4.0 | 3.0 | 0.0 | 1.0 | 4.0 | 1.0 | 0.75 | 0.857143 |
| Automatic Bread Maker | Claude4.5Sonnet | History State | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | N/A | 0.0 | N/A |
| Automatic Bread Maker | Claude4.5Sonnet | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Automatic Bread Maker | Claude4.5Sonnet | State | 12.0 | 8.0 | 0.0 | 4.0 | 12.0 | 1.0 | 0.666667 | 0.8 |
| Automatic Bread Maker | Claude4.5Sonnet | Transition | 18.0 | 14.0 | 0.0 | 4.0 | 18.0 | 1.0 | 0.777778 | 0.875 |
| Automatic Bread Maker | Claude4.5Sonnet | Overall | 48.0 | 34.5 | 0.0 | 13.5 | 48.0 | 1.0 | 0.71875 | 0.836364 |
| Automatic Bread Maker | GPT-5.5 | Action | 10.0 | 8.5 | 0.0 | 1.5 | 10.0 | 1.0 | 0.85 | 0.918919 |
| Automatic Bread Maker | GPT-5.5 | Composite State | 3.0 | 2.5 | 0.0 | 0.5 | 3.0 | 1.0 | 0.833333 | 0.909091 |
| Automatic Bread Maker | GPT-5.5 | Guard | 4.0 | 4.0 | 0.0 | 0.0 | 4.0 | 1.0 | 1.0 | 1.0 |
| Automatic Bread Maker | GPT-5.5 | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Automatic Bread Maker | GPT-5.5 | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Automatic Bread Maker | GPT-5.5 | State | 12.0 | 9.5 | 0.0 | 2.5 | 12.0 | 1.0 | 0.791667 | 0.883721 |
| Automatic Bread Maker | GPT-5.5 | Transition | 18.0 | 16.0 | 0.0 | 2.0 | 18.0 | 1.0 | 0.888889 | 0.941176 |
| Automatic Bread Maker | GPT-5.5 | Overall | 48.0 | 41.5 | 0.0 | 6.5 | 48.0 | 1.0 | 0.864583 | 0.927374 |
| Automatic Bread Maker | Gemini3.1ProPreview | Action | 10.0 | 7.0 | 0.0 | 3.0 | 10.0 | 1.0 | 0.7 | 0.823529 |
| Automatic Bread Maker | Gemini3.1ProPreview | Composite State | 3.0 | 2.5 | 0.0 | 0.5 | 3.0 | 1.0 | 0.833333 | 0.909091 |
| Automatic Bread Maker | Gemini3.1ProPreview | Guard | 4.0 | 4.0 | 0.0 | 0.0 | 4.0 | 1.0 | 1.0 | 1.0 |
| Automatic Bread Maker | Gemini3.1ProPreview | History State | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | N/A | 0.0 | N/A |
| Automatic Bread Maker | Gemini3.1ProPreview | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Automatic Bread Maker | Gemini3.1ProPreview | State | 12.0 | 8.0 | 0.0 | 4.0 | 12.0 | 1.0 | 0.666667 | 0.8 |
| Automatic Bread Maker | Gemini3.1ProPreview | Transition | 18.0 | 15.5 | 0.0 | 2.5 | 18.0 | 1.0 | 0.861111 | 0.925373 |
| Automatic Bread Maker | Gemini3.1ProPreview | Overall | 48.0 | 37.0 | 0.0 | 11.0 | 48.0 | 1.0 | 0.770833 | 0.870588 |
| Digital Chess Clock | Human | Action | 8.0 | 8.0 | 0.0 | 0.0 | 8.0 | 1.0 | 1.0 | 1.0 |
| Digital Chess Clock | Human | Composite State | 3.0 | 3.0 | 0.0 | 0.0 | 3.0 | 1.0 | 1.0 | 1.0 |
| Digital Chess Clock | Human | Guard | 4.0 | 4.0 | 0.0 | 0.0 | 4.0 | 1.0 | 1.0 | 1.0 |
| Digital Chess Clock | Human | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Digital Chess Clock | Human | Region | 2.0 | 1.0 | 0.0 | 1.0 | 2.0 | 1.0 | 0.5 | 0.666667 |
| Digital Chess Clock | Human | State | 13.0 | 11.5 | 0.0 | 1.5 | 13.0 | 1.0 | 0.884615 | 0.938776 |
| Digital Chess Clock | Human | Transition | 14.0 | 12.0 | 0.0 | 2.0 | 14.0 | 1.0 | 0.857143 | 0.923077 |
| Digital Chess Clock | Human | Overall | 45.0 | 40.5 | 0.0 | 4.5 | 45.0 | 1.0 | 0.9 | 0.947368 |
| Digital Chess Clock | Claude4.5Sonnet | Action | 8.0 | 8.0 | 1.0 | 0.0 | 9.0 | 0.888889 | 1.0 | 0.941176 |
| Digital Chess Clock | Claude4.5Sonnet | Composite State | 3.0 | 2.5 | 0.0 | 0.5 | 3.0 | 1.0 | 0.833333 | 0.909091 |
| Digital Chess Clock | Claude4.5Sonnet | Guard | 4.0 | 2.0 | 0.0 | 2.0 | 4.0 | 1.0 | 0.5 | 0.666667 |
| Digital Chess Clock | Claude4.5Sonnet | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Digital Chess Clock | Claude4.5Sonnet | Region | 2.0 | 0.0 | 0.0 | 2.0 | 2.0 | N/A | 0.0 | N/A |
| Digital Chess Clock | Claude4.5Sonnet | State | 13.0 | 8.0 | 2.0 | 5.0 | 15.0 | 0.8 | 0.615385 | 0.695652 |
| Digital Chess Clock | Claude4.5Sonnet | Transition | 14.0 | 8.0 | 0.0 | 6.0 | 14.0 | 1.0 | 0.571429 | 0.727273 |
| Digital Chess Clock | Claude4.5Sonnet | Overall | 45.0 | 29.5 | 3.0 | 15.5 | 48.0 | 0.907692 | 0.655556 | 0.76129 |
| Digital Chess Clock | GPT-5.5 | Action | 8.0 | 8.0 | 0.0 | 0.0 | 8.0 | 1.0 | 1.0 | 1.0 |
| Digital Chess Clock | GPT-5.5 | Composite State | 3.0 | 3.0 | 0.0 | 0.0 | 3.0 | 1.0 | 1.0 | 1.0 |
| Digital Chess Clock | GPT-5.5 | Guard | 4.0 | 2.0 | 0.0 | 2.0 | 4.0 | 1.0 | 0.5 | 0.666667 |
| Digital Chess Clock | GPT-5.5 | History State | 1.0 | 0.5 | 0.0 | 0.5 | 1.0 | 1.0 | 0.5 | 0.666667 |
| Digital Chess Clock | GPT-5.5 | Region | 2.0 | 1.5 | 0.0 | 0.5 | 2.0 | 1.0 | 0.75 | 0.857143 |
| Digital Chess Clock | GPT-5.5 | State | 13.0 | 10.0 | 0.0 | 3.0 | 13.0 | 1.0 | 0.769231 | 0.869565 |
| Digital Chess Clock | GPT-5.5 | Transition | 14.0 | 10.0 | 1.0 | 4.0 | 15.0 | 0.909091 | 0.714286 | 0.8 |
| Digital Chess Clock | GPT-5.5 | Overall | 45.0 | 35.0 | 1.0 | 10.0 | 46.0 | 0.972222 | 0.777778 | 0.864198 |
| Digital Chess Clock | Gemini3.1ProPreview | Action | 8.0 | 8.0 | 0.0 | 0.0 | 8.0 | 1.0 | 1.0 | 1.0 |
| Digital Chess Clock | Gemini3.1ProPreview | Composite State | 3.0 | 3.0 | 0.0 | 0.0 | 3.0 | 1.0 | 1.0 | 1.0 |
| Digital Chess Clock | Gemini3.1ProPreview | Guard | 4.0 | 3.0 | 0.0 | 1.0 | 4.0 | 1.0 | 0.75 | 0.857143 |
| Digital Chess Clock | Gemini3.1ProPreview | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Digital Chess Clock | Gemini3.1ProPreview | Region | 2.0 | 0.0 | 0.0 | 2.0 | 2.0 | N/A | 0.0 | N/A |
| Digital Chess Clock | Gemini3.1ProPreview | State | 13.0 | 10.0 | 0.0 | 3.0 | 13.0 | 1.0 | 0.769231 | 0.869565 |
| Digital Chess Clock | Gemini3.1ProPreview | Transition | 14.0 | 11.0 | 0.0 | 3.0 | 14.0 | 1.0 | 0.785714 | 0.88 |
| Digital Chess Clock | Gemini3.1ProPreview | Overall | 45.0 | 36.0 | 0.0 | 9.0 | 45.0 | 1.0 | 0.8 | 0.888889 |
| Dishwasher | Human | Action | 7.0 | 5.5 | 0.0 | 1.5 | 7.0 | 1.0 | 0.785714 | 0.88 |
| Dishwasher | Human | Composite State | 2.0 | 2.0 | 0.0 | 0.0 | 2.0 | 1.0 | 1.0 | 1.0 |
| Dishwasher | Human | Guard | 4.0 | 3.0 | 0.0 | 1.0 | 4.0 | 1.0 | 0.75 | 0.857143 |
| Dishwasher | Human | History State | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | N/A | 0.0 | N/A |
| Dishwasher | Human | Region | 2.0 | 1.0 | 0.0 | 1.0 | 2.0 | 1.0 | 0.5 | 0.666667 |
| Dishwasher | Human | State | 12.0 | 9.0 | 0.0 | 3.0 | 12.0 | 1.0 | 0.75 | 0.857143 |
| Dishwasher | Human | Transition | 19.0 | 13.5 | 0.0 | 5.5 | 19.0 | 1.0 | 0.710526 | 0.830769 |
| Dishwasher | Human | Overall | 47.0 | 34.0 | 0.0 | 13.0 | 47.0 | 1.0 | 0.723404 | 0.839506 |
| Dishwasher | Claude4.5Sonnet | Action | 7.0 | 4.5 | 0.0 | 2.5 | 7.0 | 1.0 | 0.642857 | 0.782609 |
| Dishwasher | Claude4.5Sonnet | Composite State | 2.0 | 1.0 | 0.0 | 1.0 | 2.0 | 1.0 | 0.5 | 0.666667 |
| Dishwasher | Claude4.5Sonnet | Guard | 4.0 | 2.0 | 0.0 | 2.0 | 4.0 | 1.0 | 0.5 | 0.666667 |
| Dishwasher | Claude4.5Sonnet | History State | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | N/A | 0.0 | N/A |
| Dishwasher | Claude4.5Sonnet | Region | 2.0 | 0.0 | 0.0 | 2.0 | 2.0 | N/A | 0.0 | N/A |
| Dishwasher | Claude4.5Sonnet | State | 12.0 | 8.0 | 0.0 | 4.0 | 12.0 | 1.0 | 0.666667 | 0.8 |
| Dishwasher | Claude4.5Sonnet | Transition | 19.0 | 11.5 | 0.0 | 7.5 | 19.0 | 1.0 | 0.605263 | 0.754098 |
| Dishwasher | Claude4.5Sonnet | Overall | 47.0 | 27.0 | 0.0 | 20.0 | 47.0 | 1.0 | 0.574468 | 0.72973 |
| Dishwasher | GPT-5.5 | Action | 7.0 | 5.5 | 0.0 | 1.5 | 7.0 | 1.0 | 0.785714 | 0.88 |
| Dishwasher | GPT-5.5 | Composite State | 2.0 | 1.5 | 0.0 | 0.5 | 2.0 | 1.0 | 0.75 | 0.857143 |
| Dishwasher | GPT-5.5 | Guard | 4.0 | 2.0 | 0.0 | 2.0 | 4.0 | 1.0 | 0.5 | 0.666667 |
| Dishwasher | GPT-5.5 | History State | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | N/A | 0.0 | N/A |
| Dishwasher | GPT-5.5 | Region | 2.0 | 1.5 | 0.0 | 0.5 | 2.0 | 1.0 | 0.75 | 0.857143 |
| Dishwasher | GPT-5.5 | State | 12.0 | 9.0 | 0.0 | 3.0 | 12.0 | 1.0 | 0.75 | 0.857143 |
| Dishwasher | GPT-5.5 | Transition | 19.0 | 15.0 | 0.0 | 4.0 | 19.0 | 1.0 | 0.789474 | 0.882353 |
| Dishwasher | GPT-5.5 | Overall | 47.0 | 34.5 | 0.0 | 12.5 | 47.0 | 1.0 | 0.734043 | 0.846626 |
| Dishwasher | Gemini3.1ProPreview | Action | 7.0 | 5.5 | 0.0 | 1.5 | 7.0 | 1.0 | 0.785714 | 0.88 |
| Dishwasher | Gemini3.1ProPreview | Composite State | 2.0 | 1.0 | 0.0 | 1.0 | 2.0 | 1.0 | 0.5 | 0.666667 |
| Dishwasher | Gemini3.1ProPreview | Guard | 4.0 | 2.0 | 0.0 | 2.0 | 4.0 | 1.0 | 0.5 | 0.666667 |
| Dishwasher | Gemini3.1ProPreview | History State | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | N/A | 0.0 | N/A |
| Dishwasher | Gemini3.1ProPreview | Region | 2.0 | 0.0 | 0.0 | 2.0 | 2.0 | N/A | 0.0 | N/A |
| Dishwasher | Gemini3.1ProPreview | State | 12.0 | 8.5 | 0.0 | 3.5 | 12.0 | 1.0 | 0.708333 | 0.829268 |
| Dishwasher | Gemini3.1ProPreview | Transition | 19.0 | 12.5 | 0.0 | 6.5 | 19.0 | 1.0 | 0.657895 | 0.793651 |
| Dishwasher | Gemini3.1ProPreview | Overall | 47.0 | 29.5 | 0.0 | 17.5 | 47.0 | 1.0 | 0.62766 | 0.771242 |
| Printer | Human | Action | 3.0 | 3.0 | 0.0 | 0.0 | 3.0 | 1.0 | 1.0 | 1.0 |
| Printer | Human | Composite State | 2.0 | 2.0 | 0.0 | 0.0 | 2.0 | 1.0 | 1.0 | 1.0 |
| Printer | Human | Guard | 6.0 | 6.0 | 0.0 | 0.0 | 6.0 | 1.0 | 1.0 | 1.0 |
| Printer | Human | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Printer | Human | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Printer | Human | State | 8.0 | 8.0 | 0.0 | 0.0 | 8.0 | 1.0 | 1.0 | 1.0 |
| Printer | Human | Transition | 17.0 | 17.0 | 0.0 | 0.0 | 17.0 | 1.0 | 1.0 | 1.0 |
| Printer | Human | Overall | 37.0 | 37.0 | 0.0 | 0.0 | 37.0 | 1.0 | 1.0 | 1.0 |
| Printer | Claude4.5Sonnet | Action | 3.0 | 0.0 | 0.0 | 3.0 | 3.0 | N/A | 0.0 | N/A |
| Printer | Claude4.5Sonnet | Composite State | 2.0 | 1.5 | 0.0 | 0.5 | 2.0 | 1.0 | 0.75 | 0.857143 |
| Printer | Claude4.5Sonnet | Guard | 6.0 | 4.0 | 0.0 | 2.0 | 6.0 | 1.0 | 0.666667 | 0.8 |
| Printer | Claude4.5Sonnet | History State | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | N/A | 0.0 | N/A |
| Printer | Claude4.5Sonnet | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Printer | Claude4.5Sonnet | State | 8.0 | 8.0 | 0.0 | 0.0 | 8.0 | 1.0 | 1.0 | 1.0 |
| Printer | Claude4.5Sonnet | Transition | 17.0 | 14.5 | 0.0 | 2.5 | 17.0 | 1.0 | 0.852941 | 0.920635 |
| Printer | Claude4.5Sonnet | Overall | 37.0 | 28.0 | 0.0 | 9.0 | 37.0 | 1.0 | 0.756757 | 0.861538 |
| Printer | GPT-5.5 | Action | 3.0 | 2.0 | 0.0 | 1.0 | 3.0 | 1.0 | 0.666667 | 0.8 |
| Printer | GPT-5.5 | Composite State | 2.0 | 2.0 | 0.0 | 0.0 | 2.0 | 1.0 | 1.0 | 1.0 |
| Printer | GPT-5.5 | Guard | 6.0 | 6.0 | 0.0 | 0.0 | 6.0 | 1.0 | 1.0 | 1.0 |
| Printer | GPT-5.5 | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Printer | GPT-5.5 | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Printer | GPT-5.5 | State | 8.0 | 8.0 | 0.0 | 0.0 | 8.0 | 1.0 | 1.0 | 1.0 |
| Printer | GPT-5.5 | Transition | 17.0 | 16.0 | 0.0 | 1.0 | 17.0 | 1.0 | 0.941176 | 0.969697 |
| Printer | GPT-5.5 | Overall | 37.0 | 35.0 | 0.0 | 2.0 | 37.0 | 1.0 | 0.945946 | 0.972222 |
| Printer | Gemini3.1ProPreview | Action | 3.0 | 0.0 | 0.0 | 3.0 | 3.0 | N/A | 0.0 | N/A |
| Printer | Gemini3.1ProPreview | Composite State | 2.0 | 2.0 | 0.0 | 0.0 | 2.0 | 1.0 | 1.0 | 1.0 |
| Printer | Gemini3.1ProPreview | Guard | 6.0 | 6.0 | 0.0 | 0.0 | 6.0 | 1.0 | 1.0 | 1.0 |
| Printer | Gemini3.1ProPreview | History State | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | N/A | 0.0 | N/A |
| Printer | Gemini3.1ProPreview | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Printer | Gemini3.1ProPreview | State | 8.0 | 8.0 | 0.0 | 0.0 | 8.0 | 1.0 | 1.0 | 1.0 |
| Printer | Gemini3.1ProPreview | Transition | 17.0 | 15.0 | 0.0 | 2.0 | 17.0 | 1.0 | 0.882353 | 0.9375 |
| Printer | Gemini3.1ProPreview | Overall | 37.0 | 31.0 | 0.0 | 6.0 | 37.0 | 1.0 | 0.837838 | 0.911765 |
| SSC7 | Human | Action | 21.0 | 15.0 | 0.0 | 6.0 | 21.0 | 1.0 | 0.714286 | 0.833333 |
| SSC7 | Human | Composite State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| SSC7 | Human | Guard | 11.0 | 11.0 | 0.0 | 0.0 | 11.0 | 1.0 | 1.0 | 1.0 |
| SSC7 | Human | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| SSC7 | Human | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| SSC7 | Human | State | 9.0 | 9.0 | 0.0 | 0.0 | 9.0 | 1.0 | 1.0 | 1.0 |
| SSC7 | Human | Transition | 23.0 | 23.0 | 0.0 | 0.0 | 23.0 | 1.0 | 1.0 | 1.0 |
| SSC7 | Human | Overall | 66.0 | 60.0 | 0.0 | 6.0 | 66.0 | 1.0 | 0.909091 | 0.952381 |
| SSC7 | Claude4.5Sonnet | Action | 21.0 | 15.0 | 1.0 | 6.0 | 22.0 | 0.9375 | 0.714286 | 0.810811 |
| SSC7 | Claude4.5Sonnet | Composite State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| SSC7 | Claude4.5Sonnet | Guard | 11.0 | 11.0 | 0.0 | 0.0 | 11.0 | 1.0 | 1.0 | 1.0 |
| SSC7 | Claude4.5Sonnet | History State | 1.0 | 0.5 | 0.0 | 0.5 | 1.0 | 1.0 | 0.5 | 0.666667 |
| SSC7 | Claude4.5Sonnet | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| SSC7 | Claude4.5Sonnet | State | 9.0 | 9.0 | 2.0 | 0.0 | 11.0 | 0.818182 | 1.0 | 0.9 |
| SSC7 | Claude4.5Sonnet | Transition | 23.0 | 22.0 | 1.0 | 1.0 | 24.0 | 0.956522 | 0.956522 | 0.956522 |
| SSC7 | Claude4.5Sonnet | Overall | 66.0 | 58.5 | 4.0 | 7.5 | 70.0 | 0.936 | 0.886364 | 0.910506 |
| SSC7 | GPT-5.5 | Action | 21.0 | 16.0 | 0.0 | 5.0 | 21.0 | 1.0 | 0.761905 | 0.864865 |
| SSC7 | GPT-5.5 | Composite State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| SSC7 | GPT-5.5 | Guard | 11.0 | 11.0 | 0.0 | 0.0 | 11.0 | 1.0 | 1.0 | 1.0 |
| SSC7 | GPT-5.5 | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| SSC7 | GPT-5.5 | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| SSC7 | GPT-5.5 | State | 9.0 | 9.0 | 0.0 | 0.0 | 9.0 | 1.0 | 1.0 | 1.0 |
| SSC7 | GPT-5.5 | Transition | 23.0 | 22.5 | 0.0 | 0.5 | 23.0 | 1.0 | 0.978261 | 0.989011 |
| SSC7 | GPT-5.5 | Overall | 66.0 | 60.5 | 0.0 | 5.5 | 66.0 | 1.0 | 0.916667 | 0.956522 |
| SSC7 | Gemini3.1ProPreview | Action | 21.0 | 16.5 | 0.0 | 4.5 | 21.0 | 1.0 | 0.785714 | 0.88 |
| SSC7 | Gemini3.1ProPreview | Composite State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| SSC7 | Gemini3.1ProPreview | Guard | 11.0 | 10.0 | 0.0 | 1.0 | 11.0 | 1.0 | 0.909091 | 0.952381 |
| SSC7 | Gemini3.1ProPreview | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| SSC7 | Gemini3.1ProPreview | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| SSC7 | Gemini3.1ProPreview | State | 9.0 | 9.0 | 0.0 | 0.0 | 9.0 | 1.0 | 1.0 | 1.0 |
| SSC7 | Gemini3.1ProPreview | Transition | 23.0 | 22.5 | 0.0 | 0.5 | 23.0 | 1.0 | 0.978261 | 0.989011 |
| SSC7 | Gemini3.1ProPreview | Overall | 66.0 | 60.0 | 0.0 | 6.0 | 66.0 | 1.0 | 0.909091 | 0.952381 |
| Spa Manager | Human | Action | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Spa Manager | Human | Composite State | 3.0 | 3.0 | 0.0 | 0.0 | 3.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Human | Guard | 4.0 | 4.0 | 0.0 | 0.0 | 4.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Human | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Human | Region | 5.0 | 5.0 | 0.0 | 0.0 | 5.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Human | State | 16.0 | 16.0 | 0.0 | 0.0 | 16.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Human | Transition | 15.0 | 15.0 | 0.0 | 0.0 | 15.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Human | Overall | 44.0 | 44.0 | 0.0 | 0.0 | 44.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Claude4.5Sonnet | Action | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Spa Manager | Claude4.5Sonnet | Composite State | 3.0 | 3.0 | 1.0 | 0.0 | 4.0 | 0.75 | 1.0 | 0.857143 |
| Spa Manager | Claude4.5Sonnet | Guard | 4.0 | 4.0 | 0.0 | 0.0 | 4.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Claude4.5Sonnet | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Claude4.5Sonnet | Region | 5.0 | 5.0 | 0.0 | 0.0 | 5.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Claude4.5Sonnet | State | 16.0 | 16.0 | 1.0 | 0.0 | 17.0 | 0.941176 | 1.0 | 0.969697 |
| Spa Manager | Claude4.5Sonnet | Transition | 15.0 | 14.5 | 0.0 | 0.5 | 15.0 | 1.0 | 0.966667 | 0.983051 |
| Spa Manager | Claude4.5Sonnet | Overall | 44.0 | 43.5 | 2.0 | 0.5 | 46.0 | 0.956044 | 0.988636 | 0.972067 |
| Spa Manager | GPT-5.5 | Action | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Spa Manager | GPT-5.5 | Composite State | 3.0 | 3.0 | 0.0 | 0.0 | 3.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | GPT-5.5 | Guard | 4.0 | 4.0 | 0.0 | 0.0 | 4.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | GPT-5.5 | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | GPT-5.5 | Region | 5.0 | 5.0 | 0.0 | 0.0 | 5.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | GPT-5.5 | State | 16.0 | 16.0 | 0.0 | 0.0 | 16.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | GPT-5.5 | Transition | 15.0 | 15.0 | 0.0 | 0.0 | 15.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | GPT-5.5 | Overall | 44.0 | 44.0 | 0.0 | 0.0 | 44.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Gemini3.1ProPreview | Action | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Spa Manager | Gemini3.1ProPreview | Composite State | 3.0 | 3.0 | 0.0 | 0.0 | 3.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Gemini3.1ProPreview | Guard | 4.0 | 4.0 | 0.0 | 0.0 | 4.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Gemini3.1ProPreview | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Gemini3.1ProPreview | Region | 5.0 | 5.0 | 0.0 | 0.0 | 5.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Gemini3.1ProPreview | State | 16.0 | 16.0 | 0.0 | 0.0 | 16.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Gemini3.1ProPreview | Transition | 15.0 | 15.0 | 0.0 | 0.0 | 15.0 | 1.0 | 1.0 | 1.0 |
| Spa Manager | Gemini3.1ProPreview | Overall | 44.0 | 44.0 | 0.0 | 0.0 | 44.0 | 1.0 | 1.0 | 1.0 |
| Thermomix TM6 | Human | Action | 6.0 | 1.0 | 0.0 | 5.0 | 6.0 | 1.0 | 0.166667 | 0.285714 |
| Thermomix TM6 | Human | Composite State | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | N/A | 0.0 | N/A |
| Thermomix TM6 | Human | Guard | 7.0 | 3.0 | 0.0 | 4.0 | 7.0 | 1.0 | 0.428571 | 0.6 |
| Thermomix TM6 | Human | History State | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | N/A | 0.0 | N/A |
| Thermomix TM6 | Human | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Thermomix TM6 | Human | State | 11.0 | 9.0 | 0.0 | 2.0 | 11.0 | 1.0 | 0.818182 | 0.9 |
| Thermomix TM6 | Human | Transition | 17.0 | 14.0 | 0.0 | 3.0 | 17.0 | 1.0 | 0.823529 | 0.903226 |
| Thermomix TM6 | Human | Overall | 43.0 | 27.0 | 0.0 | 16.0 | 43.0 | 1.0 | 0.627907 | 0.771429 |
| Thermomix TM6 | Claude4.5Sonnet | Action | 6.0 | 0.0 | 0.0 | 6.0 | 6.0 | N/A | 0.0 | N/A |
| Thermomix TM6 | Claude4.5Sonnet | Composite State | 1.0 | 0.0 | 1.0 | 1.0 | 2.0 | 0.0 | 0.0 | N/A |
| Thermomix TM6 | Claude4.5Sonnet | Guard | 7.0 | 2.0 | 0.0 | 5.0 | 7.0 | 1.0 | 0.285714 | 0.444444 |
| Thermomix TM6 | Claude4.5Sonnet | History State | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | N/A | 0.0 | N/A |
| Thermomix TM6 | Claude4.5Sonnet | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Thermomix TM6 | Claude4.5Sonnet | State | 11.0 | 10.5 | 0.0 | 0.5 | 11.0 | 1.0 | 0.954545 | 0.976744 |
| Thermomix TM6 | Claude4.5Sonnet | Transition | 17.0 | 13.5 | 1.0 | 3.5 | 18.0 | 0.931034 | 0.794118 | 0.857143 |
| Thermomix TM6 | Claude4.5Sonnet | Overall | 43.0 | 26.0 | 2.0 | 17.0 | 45.0 | 0.928571 | 0.604651 | 0.732394 |
| Thermomix TM6 | GPT-5.5 | Action | 6.0 | 2.0 | 0.0 | 4.0 | 6.0 | 1.0 | 0.333333 | 0.5 |
| Thermomix TM6 | GPT-5.5 | Composite State | 1.0 | 0.5 | 0.0 | 0.5 | 1.0 | 1.0 | 0.5 | 0.666667 |
| Thermomix TM6 | GPT-5.5 | Guard | 7.0 | 3.5 | 0.0 | 3.5 | 7.0 | 1.0 | 0.5 | 0.666667 |
| Thermomix TM6 | GPT-5.5 | History State | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | N/A | 0.0 | N/A |
| Thermomix TM6 | GPT-5.5 | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Thermomix TM6 | GPT-5.5 | State | 11.0 | 11.0 | 0.0 | 0.0 | 11.0 | 1.0 | 1.0 | 1.0 |
| Thermomix TM6 | GPT-5.5 | Transition | 17.0 | 12.5 | 0.0 | 4.5 | 17.0 | 1.0 | 0.735294 | 0.847458 |
| Thermomix TM6 | GPT-5.5 | Overall | 43.0 | 29.5 | 0.0 | 13.5 | 43.0 | 1.0 | 0.686047 | 0.813793 |
| Thermomix TM6 | Gemini3.1ProPreview | Action | 6.0 | 2.0 | 0.0 | 4.0 | 6.0 | 1.0 | 0.333333 | 0.5 |
| Thermomix TM6 | Gemini3.1ProPreview | Composite State | 1.0 | 0.5 | 0.0 | 0.5 | 1.0 | 1.0 | 0.5 | 0.666667 |
| Thermomix TM6 | Gemini3.1ProPreview | Guard | 7.0 | 3.0 | 0.0 | 4.0 | 7.0 | 1.0 | 0.428571 | 0.6 |
| Thermomix TM6 | Gemini3.1ProPreview | History State | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | N/A | 0.0 | N/A |
| Thermomix TM6 | Gemini3.1ProPreview | Region | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A | N/A | N/A |
| Thermomix TM6 | Gemini3.1ProPreview | State | 11.0 | 10.0 | 0.0 | 1.0 | 11.0 | 1.0 | 0.909091 | 0.952381 |
| Thermomix TM6 | Gemini3.1ProPreview | Transition | 17.0 | 13.5 | 0.0 | 3.5 | 17.0 | 1.0 | 0.794118 | 0.885246 |
| Thermomix TM6 | Gemini3.1ProPreview | Overall | 43.0 | 29.0 | 0.0 | 14.0 | 43.0 | 1.0 | 0.674419 | 0.805556 |
| Train Automation System | Human | Action | 12.0 | 9.5 | 0.0 | 2.5 | 12.0 | 1.0 | 0.791667 | 0.883721 |
| Train Automation System | Human | Composite State | 2.0 | 2.0 | 0.0 | 0.0 | 2.0 | 1.0 | 1.0 | 1.0 |
| Train Automation System | Human | Guard | 14.0 | 10.5 | 0.0 | 3.5 | 14.0 | 1.0 | 0.75 | 0.857143 |
| Train Automation System | Human | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Train Automation System | Human | Region | 4.0 | 4.0 | 0.0 | 0.0 | 4.0 | 1.0 | 1.0 | 1.0 |
| Train Automation System | Human | State | 17.0 | 14.5 | 0.0 | 2.5 | 17.0 | 1.0 | 0.852941 | 0.920635 |
| Train Automation System | Human | Transition | 20.0 | 17.5 | 0.0 | 2.5 | 20.0 | 1.0 | 0.875 | 0.933333 |
| Train Automation System | Human | Overall | 70.0 | 59.0 | 0.0 | 11.0 | 70.0 | 1.0 | 0.842857 | 0.914729 |
| Train Automation System | Claude4.5Sonnet | Action | 12.0 | 8.5 | 0.0 | 3.5 | 12.0 | 1.0 | 0.708333 | 0.829268 |
| Train Automation System | Claude4.5Sonnet | Composite State | 2.0 | 2.0 | 0.0 | 0.0 | 2.0 | 1.0 | 1.0 | 1.0 |
| Train Automation System | Claude4.5Sonnet | Guard | 14.0 | 8.0 | 0.0 | 6.0 | 14.0 | 1.0 | 0.571429 | 0.727273 |
| Train Automation System | Claude4.5Sonnet | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Train Automation System | Claude4.5Sonnet | Region | 4.0 | 4.0 | 0.0 | 0.0 | 4.0 | 1.0 | 1.0 | 1.0 |
| Train Automation System | Claude4.5Sonnet | State | 17.0 | 6.5 | 0.0 | 10.5 | 17.0 | 1.0 | 0.382353 | 0.553191 |
| Train Automation System | Claude4.5Sonnet | Transition | 20.0 | 10.0 | 0.0 | 10.0 | 20.0 | 1.0 | 0.5 | 0.666667 |
| Train Automation System | Claude4.5Sonnet | Overall | 70.0 | 40.0 | 0.0 | 30.0 | 70.0 | 1.0 | 0.571429 | 0.727273 |
| Train Automation System | GPT-5.5 | Action | 12.0 | 8.0 | 0.0 | 4.0 | 12.0 | 1.0 | 0.666667 | 0.8 |
| Train Automation System | GPT-5.5 | Composite State | 2.0 | 1.5 | 0.0 | 0.5 | 2.0 | 1.0 | 0.75 | 0.857143 |
| Train Automation System | GPT-5.5 | Guard | 14.0 | 5.5 | 0.0 | 8.5 | 14.0 | 1.0 | 0.392857 | 0.564103 |
| Train Automation System | GPT-5.5 | History State | 1.0 | 0.5 | 0.0 | 0.5 | 1.0 | 1.0 | 0.5 | 0.666667 |
| Train Automation System | GPT-5.5 | Region | 4.0 | 4.0 | 0.0 | 0.0 | 4.0 | 1.0 | 1.0 | 1.0 |
| Train Automation System | GPT-5.5 | State | 17.0 | 9.0 | 0.0 | 8.0 | 17.0 | 1.0 | 0.529412 | 0.692308 |
| Train Automation System | GPT-5.5 | Transition | 20.0 | 9.0 | 1.0 | 11.0 | 21.0 | 0.9 | 0.45 | 0.6 |
| Train Automation System | GPT-5.5 | Overall | 70.0 | 37.5 | 1.0 | 32.5 | 71.0 | 0.974026 | 0.535714 | 0.691244 |
| Train Automation System | Gemini3.1ProPreview | Action | 12.0 | 8.0 | 0.0 | 4.0 | 12.0 | 1.0 | 0.666667 | 0.8 |
| Train Automation System | Gemini3.1ProPreview | Composite State | 2.0 | 2.0 | 0.0 | 0.0 | 2.0 | 1.0 | 1.0 | 1.0 |
| Train Automation System | Gemini3.1ProPreview | Guard | 14.0 | 6.0 | 0.0 | 8.0 | 14.0 | 1.0 | 0.428571 | 0.6 |
| Train Automation System | Gemini3.1ProPreview | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Train Automation System | Gemini3.1ProPreview | Region | 4.0 | 4.0 | 0.0 | 0.0 | 4.0 | 1.0 | 1.0 | 1.0 |
| Train Automation System | Gemini3.1ProPreview | State | 17.0 | 11.0 | 0.0 | 6.0 | 17.0 | 1.0 | 0.647059 | 0.785714 |
| Train Automation System | Gemini3.1ProPreview | Transition | 20.0 | 10.0 | 0.0 | 10.0 | 20.0 | 1.0 | 0.5 | 0.666667 |
| Train Automation System | Gemini3.1ProPreview | Overall | 70.0 | 42.0 | 0.0 | 28.0 | 70.0 | 1.0 | 0.6 | 0.75 |
| Wumple | Human | Action | 36.0 | 21.5 | 0.0 | 14.5 | 36.0 | 1.0 | 0.597222 | 0.747826 |
| Wumple | Human | Composite State | 5.0 | 5.0 | 0.0 | 0.0 | 5.0 | 1.0 | 1.0 | 1.0 |
| Wumple | Human | Guard | 3.0 | 0.0 | 0.0 | 3.0 | 3.0 | N/A | 0.0 | N/A |
| Wumple | Human | History State | 1.0 | 1.0 | 2.0 | 0.0 | 3.0 | 0.333333 | 1.0 | 0.5 |
| Wumple | Human | Region | 2.0 | 2.0 | 0.0 | 0.0 | 2.0 | 1.0 | 1.0 | 1.0 |
| Wumple | Human | State | 24.0 | 22.5 | 0.0 | 1.5 | 24.0 | 1.0 | 0.9375 | 0.967742 |
| Wumple | Human | Transition | 37.0 | 34.5 | 0.0 | 2.5 | 37.0 | 1.0 | 0.932432 | 0.965035 |
| Wumple | Human | Overall | 108.0 | 86.5 | 2.0 | 21.5 | 110.0 | 0.977401 | 0.800926 | 0.880407 |
| Wumple | Claude4.5Sonnet | Action | 36.0 | 6.5 | 0.0 | 29.5 | 36.0 | 1.0 | 0.180556 | 0.305882 |
| Wumple | Claude4.5Sonnet | Composite State | 5.0 | 4.0 | 0.0 | 1.0 | 5.0 | 1.0 | 0.8 | 0.888889 |
| Wumple | Claude4.5Sonnet | Guard | 3.0 | 1.0 | 0.0 | 2.0 | 3.0 | 1.0 | 0.333333 | 0.5 |
| Wumple | Claude4.5Sonnet | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Wumple | Claude4.5Sonnet | Region | 2.0 | 2.0 | 0.0 | 0.0 | 2.0 | 1.0 | 1.0 | 1.0 |
| Wumple | Claude4.5Sonnet | State | 24.0 | 22.5 | 0.0 | 1.5 | 24.0 | 1.0 | 0.9375 | 0.967742 |
| Wumple | Claude4.5Sonnet | Transition | 37.0 | 33.0 | 0.0 | 4.0 | 37.0 | 1.0 | 0.891892 | 0.942857 |
| Wumple | Claude4.5Sonnet | Overall | 108.0 | 70.0 | 0.0 | 38.0 | 108.0 | 1.0 | 0.648148 | 0.786517 |
| Wumple | GPT-5.5 | Action | 36.0 | 27.0 | 0.0 | 9.0 | 36.0 | 1.0 | 0.75 | 0.857143 |
| Wumple | GPT-5.5 | Composite State | 5.0 | 5.0 | 0.0 | 0.0 | 5.0 | 1.0 | 1.0 | 1.0 |
| Wumple | GPT-5.5 | Guard | 3.0 | 3.0 | 0.0 | 0.0 | 3.0 | 1.0 | 1.0 | 1.0 |
| Wumple | GPT-5.5 | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Wumple | GPT-5.5 | Region | 2.0 | 2.0 | 0.0 | 0.0 | 2.0 | 1.0 | 1.0 | 1.0 |
| Wumple | GPT-5.5 | State | 24.0 | 22.0 | 0.0 | 2.0 | 24.0 | 1.0 | 0.916667 | 0.956522 |
| Wumple | GPT-5.5 | Transition | 37.0 | 35.5 | 0.0 | 1.5 | 37.0 | 1.0 | 0.959459 | 0.97931 |
| Wumple | GPT-5.5 | Overall | 108.0 | 95.5 | 0.0 | 12.5 | 108.0 | 1.0 | 0.884259 | 0.938575 |
| Wumple | Gemini3.1ProPreview | Action | 36.0 | 14.0 | 0.0 | 22.0 | 36.0 | 1.0 | 0.388889 | 0.56 |
| Wumple | Gemini3.1ProPreview | Composite State | 5.0 | 4.0 | 0.0 | 1.0 | 5.0 | 1.0 | 0.8 | 0.888889 |
| Wumple | Gemini3.1ProPreview | Guard | 3.0 | 1.0 | 0.0 | 2.0 | 3.0 | 1.0 | 0.333333 | 0.5 |
| Wumple | Gemini3.1ProPreview | History State | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Wumple | Gemini3.1ProPreview | Region | 2.0 | 2.0 | 0.0 | 0.0 | 2.0 | 1.0 | 1.0 | 1.0 |
| Wumple | Gemini3.1ProPreview | State | 24.0 | 21.5 | 0.0 | 2.5 | 24.0 | 1.0 | 0.895833 | 0.945055 |
| Wumple | Gemini3.1ProPreview | Transition | 37.0 | 33.5 | 0.0 | 3.5 | 37.0 | 1.0 | 0.905405 | 0.950355 |
| Wumple | Gemini3.1ProPreview | Overall | 108.0 | 77.0 | 0.0 | 31.0 | 108.0 | 1.0 | 0.712963 | 0.832432 |

### rq3_grading_score_distribution.csv

Source CSV: `_Figures/PaperExperimentData/rq3_grading_score_distribution.csv`

Source script: `_scripts/summarize_paper_experiments.py`

Rows: 72

Description: RQ3 LLM-only score distributions for every generator/grader/model-element combination.

| generator | grader | model_element | items | score_0_count | score_0_5_count | score_1_count | score_0_pct | score_0_5_pct | score_1_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Claude4.5Sonnet | Claude4.5Sonnet | Action | 111 | 49 | 23 | 39 | 0.44144144144144143 | 0.2072072072072072 | 0.35135135135135137 |
| Claude4.5Sonnet | Claude4.5Sonnet | Composite State | 31 | 10 | 3 | 18 | 0.3225806451612903 | 0.0967741935483871 | 0.5806451612903226 |
| Claude4.5Sonnet | Claude4.5Sonnet | Guard | 66 | 22 | 14 | 30 | 0.3333333333333333 | 0.21212121212121213 | 0.45454545454545453 |
| Claude4.5Sonnet | Claude4.5Sonnet | History State | 18 | 13 | 1 | 4 | 0.7222222222222222 | 0.05555555555555555 | 0.2222222222222222 |
| Claude4.5Sonnet | Claude4.5Sonnet | Overall Score | 569 | 174 | 62 | 333 | 0.30579964850615116 | 0.10896309314586995 | 0.5852372583479789 |
| Claude4.5Sonnet | Claude4.5Sonnet | Region | 24 | 13 | 0 | 11 | 0.5416666666666666 | 0.0 | 0.4583333333333333 |
| Claude4.5Sonnet | Claude4.5Sonnet | State | 129 | 29 | 5 | 95 | 0.2248062015503876 | 0.03875968992248062 | 0.7364341085271318 |
| Claude4.5Sonnet | Claude4.5Sonnet | Transition | 190 | 38 | 16 | 136 | 0.2 | 0.08421052631578947 | 0.7157894736842105 |
| Claude4.5Sonnet | GPT-5.5 | Action | 111 | 17 | 36 | 58 | 0.15315315315315314 | 0.32432432432432434 | 0.5225225225225225 |
| Claude4.5Sonnet | GPT-5.5 | Composite State | 31 | 9 | 4 | 18 | 0.2903225806451613 | 0.12903225806451613 | 0.5806451612903226 |
| Claude4.5Sonnet | GPT-5.5 | Guard | 66 | 24 | 2 | 40 | 0.36363636363636365 | 0.030303030303030304 | 0.6060606060606061 |
| Claude4.5Sonnet | GPT-5.5 | History State | 18 | 11 | 2 | 5 | 0.6111111111111112 | 0.1111111111111111 | 0.2777777777777778 |
| Claude4.5Sonnet | GPT-5.5 | Overall Score | 571 | 113 | 86 | 372 | 0.1978984238178634 | 0.15061295971978983 | 0.6514886164623468 |
| Claude4.5Sonnet | GPT-5.5 | Region | 24 | 9 | 2 | 13 | 0.375 | 0.08333333333333333 | 0.5416666666666666 |
| Claude4.5Sonnet | GPT-5.5 | State | 131 | 24 | 7 | 100 | 0.183206106870229 | 0.05343511450381679 | 0.7633587786259542 |
| Claude4.5Sonnet | GPT-5.5 | Transition | 190 | 19 | 33 | 138 | 0.1 | 0.1736842105263158 | 0.7263157894736842 |
| Claude4.5Sonnet | Gemini3.1ProPreview | Action | 111 | 44 | 14 | 53 | 0.3963963963963964 | 0.12612612612612611 | 0.4774774774774775 |
| Claude4.5Sonnet | Gemini3.1ProPreview | Composite State | 31 | 11 | 2 | 18 | 0.3548387096774194 | 0.06451612903225806 | 0.5806451612903226 |
| Claude4.5Sonnet | Gemini3.1ProPreview | Guard | 66 | 24 | 6 | 36 | 0.36363636363636365 | 0.09090909090909091 | 0.5454545454545454 |
| Claude4.5Sonnet | Gemini3.1ProPreview | History State | 18 | 13 | 0 | 5 | 0.7222222222222222 | 0.0 | 0.2777777777777778 |
| Claude4.5Sonnet | Gemini3.1ProPreview | Overall Score | 571 | 163 | 45 | 363 | 0.28546409807355516 | 0.07880910683012259 | 0.6357267950963222 |
| Claude4.5Sonnet | Gemini3.1ProPreview | Region | 24 | 13 | 0 | 11 | 0.5416666666666666 | 0.0 | 0.4583333333333333 |
| Claude4.5Sonnet | Gemini3.1ProPreview | State | 131 | 26 | 6 | 99 | 0.1984732824427481 | 0.04580152671755725 | 0.7557251908396947 |
| Claude4.5Sonnet | Gemini3.1ProPreview | Transition | 190 | 32 | 17 | 141 | 0.16842105263157894 | 0.08947368421052632 | 0.7421052631578947 |
| GPT-5.5 | Claude4.5Sonnet | Action | 111 | 16 | 3 | 92 | 0.14414414414414414 | 0.02702702702702703 | 0.8288288288288288 |
| GPT-5.5 | Claude4.5Sonnet | Composite State | 31 | 11 | 0 | 20 | 0.3548387096774194 | 0.0 | 0.6451612903225806 |
| GPT-5.5 | Claude4.5Sonnet | Guard | 66 | 12 | 1 | 53 | 0.18181818181818182 | 0.015151515151515152 | 0.803030303030303 |
| GPT-5.5 | Claude4.5Sonnet | History State | 18 | 12 | 0 | 6 | 0.6666666666666666 | 0.0 | 0.3333333333333333 |
| GPT-5.5 | Claude4.5Sonnet | Overall Score | 570 | 95 | 17 | 458 | 0.16666666666666666 | 0.02982456140350877 | 0.8035087719298246 |
| GPT-5.5 | Claude4.5Sonnet | Region | 23 | 9 | 2 | 12 | 0.391304347826087 | 0.08695652173913043 | 0.5217391304347826 |
| GPT-5.5 | Claude4.5Sonnet | State | 131 | 17 | 1 | 113 | 0.1297709923664122 | 0.007633587786259542 | 0.8625954198473282 |
| GPT-5.5 | Claude4.5Sonnet | Transition | 190 | 18 | 10 | 162 | 0.09473684210526316 | 0.05263157894736842 | 0.8526315789473684 |
| GPT-5.5 | GPT-5.5 | Action | 111 | 12 | 5 | 94 | 0.10810810810810811 | 0.04504504504504504 | 0.8468468468468469 |
| GPT-5.5 | GPT-5.5 | Composite State | 31 | 9 | 1 | 21 | 0.2903225806451613 | 0.03225806451612903 | 0.6774193548387096 |
| GPT-5.5 | GPT-5.5 | Guard | 66 | 13 | 2 | 51 | 0.19696969696969696 | 0.030303030303030304 | 0.7727272727272727 |
| GPT-5.5 | GPT-5.5 | History State | 18 | 9 | 2 | 7 | 0.5 | 0.1111111111111111 | 0.3888888888888889 |
| GPT-5.5 | GPT-5.5 | Overall Score | 571 | 75 | 28 | 468 | 0.13134851138353765 | 0.04903677758318739 | 0.819614711033275 |
| GPT-5.5 | GPT-5.5 | Region | 24 | 10 | 0 | 14 | 0.4166666666666667 | 0.0 | 0.5833333333333334 |
| GPT-5.5 | GPT-5.5 | State | 131 | 11 | 7 | 113 | 0.08396946564885496 | 0.05343511450381679 | 0.8625954198473282 |
| GPT-5.5 | GPT-5.5 | Transition | 190 | 11 | 11 | 168 | 0.05789473684210526 | 0.05789473684210526 | 0.8842105263157894 |
| GPT-5.5 | Gemini3.1ProPreview | Action | 111 | 12 | 7 | 92 | 0.10810810810810811 | 0.06306306306306306 | 0.8288288288288288 |
| GPT-5.5 | Gemini3.1ProPreview | Composite State | 31 | 9 | 0 | 22 | 0.2903225806451613 | 0.0 | 0.7096774193548387 |
| GPT-5.5 | Gemini3.1ProPreview | Guard | 66 | 12 | 5 | 49 | 0.18181818181818182 | 0.07575757575757576 | 0.7424242424242424 |
| GPT-5.5 | Gemini3.1ProPreview | History State | 18 | 11 | 1 | 6 | 0.6111111111111112 | 0.05555555555555555 | 0.3333333333333333 |
| GPT-5.5 | Gemini3.1ProPreview | Overall Score | 571 | 88 | 22 | 461 | 0.15411558669001751 | 0.03852889667250438 | 0.8073555166374781 |
| GPT-5.5 | Gemini3.1ProPreview | Region | 24 | 12 | 0 | 12 | 0.5 | 0.0 | 0.5 |
| GPT-5.5 | Gemini3.1ProPreview | State | 131 | 15 | 4 | 112 | 0.11450381679389313 | 0.030534351145038167 | 0.8549618320610687 |
| GPT-5.5 | Gemini3.1ProPreview | Transition | 190 | 17 | 5 | 168 | 0.08947368421052632 | 0.02631578947368421 | 0.8842105263157894 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Action | 111 | 53 | 8 | 50 | 0.4774774774774775 | 0.07207207207207207 | 0.45045045045045046 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Composite State | 31 | 11 | 1 | 19 | 0.3548387096774194 | 0.03225806451612903 | 0.6129032258064516 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Guard | 66 | 21 | 8 | 37 | 0.3181818181818182 | 0.12121212121212122 | 0.5606060606060606 |
| Gemini3.1ProPreview | Claude4.5Sonnet | History State | 18 | 13 | 0 | 5 | 0.7222222222222222 | 0.0 | 0.2777777777777778 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Overall Score | 571 | 156 | 39 | 376 | 0.2732049036777583 | 0.06830122591943957 | 0.658493870402802 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Region | 24 | 11 | 1 | 12 | 0.4583333333333333 | 0.041666666666666664 | 0.5 |
| Gemini3.1ProPreview | Claude4.5Sonnet | State | 131 | 20 | 6 | 105 | 0.15267175572519084 | 0.04580152671755725 | 0.8015267175572519 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Transition | 190 | 27 | 15 | 148 | 0.14210526315789473 | 0.07894736842105263 | 0.7789473684210526 |
| Gemini3.1ProPreview | GPT-5.5 | Action | 111 | 18 | 15 | 78 | 0.16216216216216217 | 0.13513513513513514 | 0.7027027027027027 |
| Gemini3.1ProPreview | GPT-5.5 | Composite State | 31 | 9 | 1 | 21 | 0.2903225806451613 | 0.03225806451612903 | 0.6774193548387096 |
| Gemini3.1ProPreview | GPT-5.5 | Guard | 66 | 19 | 6 | 41 | 0.2878787878787879 | 0.09090909090909091 | 0.6212121212121212 |
| Gemini3.1ProPreview | GPT-5.5 | History State | 18 | 10 | 2 | 6 | 0.5555555555555556 | 0.1111111111111111 | 0.3333333333333333 |
| Gemini3.1ProPreview | GPT-5.5 | Overall Score | 571 | 98 | 49 | 424 | 0.17162872154115585 | 0.08581436077057793 | 0.7425569176882661 |
| Gemini3.1ProPreview | GPT-5.5 | Region | 24 | 9 | 3 | 12 | 0.375 | 0.125 | 0.5 |
| Gemini3.1ProPreview | GPT-5.5 | State | 131 | 15 | 6 | 110 | 0.11450381679389313 | 0.04580152671755725 | 0.8396946564885496 |
| Gemini3.1ProPreview | GPT-5.5 | Transition | 190 | 18 | 16 | 156 | 0.09473684210526316 | 0.08421052631578947 | 0.8210526315789474 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | Action | 111 | 30 | 11 | 70 | 0.2702702702702703 | 0.0990990990990991 | 0.6306306306306306 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | Composite State | 31 | 9 | 1 | 21 | 0.2903225806451613 | 0.03225806451612903 | 0.6774193548387096 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | Guard | 66 | 20 | 5 | 41 | 0.30303030303030304 | 0.07575757575757576 | 0.6212121212121212 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | History State | 18 | 11 | 0 | 7 | 0.6111111111111112 | 0.0 | 0.3888888888888889 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | Overall Score | 571 | 124 | 24 | 423 | 0.2171628721541156 | 0.04203152364273205 | 0.7408056042031523 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | Region | 24 | 12 | 0 | 12 | 0.5 | 0.0 | 0.5 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | State | 131 | 19 | 2 | 110 | 0.1450381679389313 | 0.015267175572519083 | 0.8396946564885496 |
| Gemini3.1ProPreview | Gemini3.1ProPreview | Transition | 190 | 23 | 5 | 162 | 0.12105263157894737 | 0.02631578947368421 | 0.8526315789473684 |

### rq3_per_grader_stability.csv

Source CSV: `_Figures/PaperExperimentData/rq3_per_grader_stability.csv`

Source script: `_scripts/summarize_paper_experiments.py`

Rows: 48

Description: RQ3 baseline-vs-comparison deltas for each grader and model element.

| grader | model_element | baseline_generator | comparison_generator | baseline_score_0_pct | baseline_score_0_5_pct | baseline_score_1_pct | comparison_score_0_pct | comparison_score_0_5_pct | comparison_score_1_pct | delta_score_0_pct | delta_score_0_5_pct | delta_score_1_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Claude4.5Sonnet | Composite State | Claude4.5Sonnet | GPT-5.5 | 0.3225806451612903 | 0.0967741935483871 | 0.5806451612903226 | 0.3548387096774194 | 0.0 | 0.6451612903225806 | 0.03225806451612906 | -0.0967741935483871 | 0.06451612903225801 |
| Claude4.5Sonnet | Composite State | Claude4.5Sonnet | Gemini3.1ProPreview | 0.3225806451612903 | 0.0967741935483871 | 0.5806451612903226 | 0.3548387096774194 | 0.03225806451612903 | 0.6129032258064516 | 0.03225806451612906 | -0.06451612903225806 | 0.032258064516129004 |
| Claude4.5Sonnet | State | Claude4.5Sonnet | GPT-5.5 | 0.2248062015503876 | 0.03875968992248062 | 0.7364341085271318 | 0.1297709923664122 | 0.007633587786259542 | 0.8625954198473282 | -0.0950352091839754 | -0.03112610213622108 | 0.12616131132019648 |
| Claude4.5Sonnet | State | Claude4.5Sonnet | Gemini3.1ProPreview | 0.2248062015503876 | 0.03875968992248062 | 0.7364341085271318 | 0.15267175572519084 | 0.04580152671755725 | 0.8015267175572519 | -0.07213444582519676 | 0.007041836795076632 | 0.06509260903012015 |
| Claude4.5Sonnet | Transition | Claude4.5Sonnet | GPT-5.5 | 0.2 | 0.08421052631578947 | 0.7157894736842105 | 0.09473684210526316 | 0.05263157894736842 | 0.8526315789473684 | -0.10526315789473685 | -0.031578947368421054 | 0.13684210526315788 |
| Claude4.5Sonnet | Transition | Claude4.5Sonnet | Gemini3.1ProPreview | 0.2 | 0.08421052631578947 | 0.7157894736842105 | 0.14210526315789473 | 0.07894736842105263 | 0.7789473684210526 | -0.05789473684210528 | -0.005263157894736845 | 0.06315789473684208 |
| Claude4.5Sonnet | Action | Claude4.5Sonnet | GPT-5.5 | 0.44144144144144143 | 0.2072072072072072 | 0.35135135135135137 | 0.14414414414414414 | 0.02702702702702703 | 0.8288288288288288 | -0.29729729729729726 | -0.18018018018018017 | 0.47747747747747743 |
| Claude4.5Sonnet | Action | Claude4.5Sonnet | Gemini3.1ProPreview | 0.44144144144144143 | 0.2072072072072072 | 0.35135135135135137 | 0.4774774774774775 | 0.07207207207207207 | 0.45045045045045046 | 0.03603603603603606 | -0.13513513513513514 | 0.09909909909909909 |
| Claude4.5Sonnet | Region | Claude4.5Sonnet | GPT-5.5 | 0.5416666666666666 | 0.0 | 0.4583333333333333 | 0.391304347826087 | 0.08695652173913043 | 0.5217391304347826 | -0.15036231884057966 | 0.08695652173913043 | 0.06340579710144928 |
| Claude4.5Sonnet | Region | Claude4.5Sonnet | Gemini3.1ProPreview | 0.5416666666666666 | 0.0 | 0.4583333333333333 | 0.4583333333333333 | 0.041666666666666664 | 0.5 | -0.08333333333333331 | 0.041666666666666664 | 0.041666666666666685 |
| Claude4.5Sonnet | History State | Claude4.5Sonnet | GPT-5.5 | 0.7222222222222222 | 0.05555555555555555 | 0.2222222222222222 | 0.6666666666666666 | 0.0 | 0.3333333333333333 | -0.05555555555555558 | -0.05555555555555555 | 0.1111111111111111 |
| Claude4.5Sonnet | History State | Claude4.5Sonnet | Gemini3.1ProPreview | 0.7222222222222222 | 0.05555555555555555 | 0.2222222222222222 | 0.7222222222222222 | 0.0 | 0.2777777777777778 | 0.0 | -0.05555555555555555 | 0.05555555555555558 |
| Claude4.5Sonnet | Guard | Claude4.5Sonnet | GPT-5.5 | 0.3333333333333333 | 0.21212121212121213 | 0.45454545454545453 | 0.18181818181818182 | 0.015151515151515152 | 0.803030303030303 | -0.1515151515151515 | -0.19696969696969696 | 0.34848484848484845 |
| Claude4.5Sonnet | Guard | Claude4.5Sonnet | Gemini3.1ProPreview | 0.3333333333333333 | 0.21212121212121213 | 0.45454545454545453 | 0.3181818181818182 | 0.12121212121212122 | 0.5606060606060606 | -0.015151515151515138 | -0.09090909090909091 | 0.10606060606060602 |
| Claude4.5Sonnet | Overall Score | Claude4.5Sonnet | GPT-5.5 | 0.30579964850615116 | 0.10896309314586995 | 0.5852372583479789 | 0.16666666666666666 | 0.02982456140350877 | 0.8035087719298246 | -0.1391329818394845 | -0.07913853174236118 | 0.2182715135818457 |
| Claude4.5Sonnet | Overall Score | Claude4.5Sonnet | Gemini3.1ProPreview | 0.30579964850615116 | 0.10896309314586995 | 0.5852372583479789 | 0.2732049036777583 | 0.06830122591943957 | 0.658493870402802 | -0.03259474482839286 | -0.04066186722643038 | 0.07325661205482314 |
| GPT-5.5 | Composite State | Claude4.5Sonnet | GPT-5.5 | 0.2903225806451613 | 0.12903225806451613 | 0.5806451612903226 | 0.2903225806451613 | 0.03225806451612903 | 0.6774193548387096 | 0.0 | -0.0967741935483871 | 0.09677419354838701 |
| GPT-5.5 | Composite State | Claude4.5Sonnet | Gemini3.1ProPreview | 0.2903225806451613 | 0.12903225806451613 | 0.5806451612903226 | 0.2903225806451613 | 0.03225806451612903 | 0.6774193548387096 | 0.0 | -0.0967741935483871 | 0.09677419354838701 |
| GPT-5.5 | State | Claude4.5Sonnet | GPT-5.5 | 0.183206106870229 | 0.05343511450381679 | 0.7633587786259542 | 0.08396946564885496 | 0.05343511450381679 | 0.8625954198473282 | -0.09923664122137404 | 0.0 | 0.09923664122137399 |
| GPT-5.5 | State | Claude4.5Sonnet | Gemini3.1ProPreview | 0.183206106870229 | 0.05343511450381679 | 0.7633587786259542 | 0.11450381679389313 | 0.04580152671755725 | 0.8396946564885496 | -0.06870229007633588 | -0.007633587786259541 | 0.07633587786259532 |
| GPT-5.5 | Transition | Claude4.5Sonnet | GPT-5.5 | 0.1 | 0.1736842105263158 | 0.7263157894736842 | 0.05789473684210526 | 0.05789473684210526 | 0.8842105263157894 | -0.04210526315789474 | -0.11578947368421054 | 0.1578947368421052 |
| GPT-5.5 | Transition | Claude4.5Sonnet | Gemini3.1ProPreview | 0.1 | 0.1736842105263158 | 0.7263157894736842 | 0.09473684210526316 | 0.08421052631578947 | 0.8210526315789474 | -0.005263157894736845 | -0.08947368421052633 | 0.09473684210526312 |
| GPT-5.5 | Action | Claude4.5Sonnet | GPT-5.5 | 0.15315315315315314 | 0.32432432432432434 | 0.5225225225225225 | 0.10810810810810811 | 0.04504504504504504 | 0.8468468468468469 | -0.04504504504504503 | -0.2792792792792793 | 0.32432432432432434 |
| GPT-5.5 | Action | Claude4.5Sonnet | Gemini3.1ProPreview | 0.15315315315315314 | 0.32432432432432434 | 0.5225225225225225 | 0.16216216216216217 | 0.13513513513513514 | 0.7027027027027027 | 0.009009009009009028 | -0.1891891891891892 | 0.18018018018018023 |
| GPT-5.5 | Region | Claude4.5Sonnet | GPT-5.5 | 0.375 | 0.08333333333333333 | 0.5416666666666666 | 0.4166666666666667 | 0.0 | 0.5833333333333334 | 0.041666666666666685 | -0.08333333333333333 | 0.04166666666666674 |
| GPT-5.5 | Region | Claude4.5Sonnet | Gemini3.1ProPreview | 0.375 | 0.08333333333333333 | 0.5416666666666666 | 0.375 | 0.125 | 0.5 | 0.0 | 0.04166666666666667 | -0.04166666666666663 |
| GPT-5.5 | History State | Claude4.5Sonnet | GPT-5.5 | 0.6111111111111112 | 0.1111111111111111 | 0.2777777777777778 | 0.5 | 0.1111111111111111 | 0.3888888888888889 | -0.11111111111111116 | 0.0 | 0.1111111111111111 |
| GPT-5.5 | History State | Claude4.5Sonnet | Gemini3.1ProPreview | 0.6111111111111112 | 0.1111111111111111 | 0.2777777777777778 | 0.5555555555555556 | 0.1111111111111111 | 0.3333333333333333 | -0.05555555555555558 | 0.0 | 0.055555555555555525 |
| GPT-5.5 | Guard | Claude4.5Sonnet | GPT-5.5 | 0.36363636363636365 | 0.030303030303030304 | 0.6060606060606061 | 0.19696969696969696 | 0.030303030303030304 | 0.7727272727272727 | -0.16666666666666669 | 0.0 | 0.16666666666666663 |
| GPT-5.5 | Guard | Claude4.5Sonnet | Gemini3.1ProPreview | 0.36363636363636365 | 0.030303030303030304 | 0.6060606060606061 | 0.2878787878787879 | 0.09090909090909091 | 0.6212121212121212 | -0.07575757575757575 | 0.06060606060606061 | 0.015151515151515138 |
| GPT-5.5 | Overall Score | Claude4.5Sonnet | GPT-5.5 | 0.1978984238178634 | 0.15061295971978983 | 0.6514886164623468 | 0.13134851138353765 | 0.04903677758318739 | 0.819614711033275 | -0.06654991243432576 | -0.10157618213660244 | 0.1681260945709282 |
| GPT-5.5 | Overall Score | Claude4.5Sonnet | Gemini3.1ProPreview | 0.1978984238178634 | 0.15061295971978983 | 0.6514886164623468 | 0.17162872154115585 | 0.08581436077057793 | 0.7425569176882661 | -0.02626970227670755 | -0.0647985989492119 | 0.09106830122591936 |
| Gemini3.1ProPreview | Composite State | Claude4.5Sonnet | GPT-5.5 | 0.3548387096774194 | 0.06451612903225806 | 0.5806451612903226 | 0.2903225806451613 | 0.0 | 0.7096774193548387 | -0.06451612903225806 | -0.06451612903225806 | 0.12903225806451613 |
| Gemini3.1ProPreview | Composite State | Claude4.5Sonnet | Gemini3.1ProPreview | 0.3548387096774194 | 0.06451612903225806 | 0.5806451612903226 | 0.2903225806451613 | 0.03225806451612903 | 0.6774193548387096 | -0.06451612903225806 | -0.03225806451612903 | 0.09677419354838701 |
| Gemini3.1ProPreview | State | Claude4.5Sonnet | GPT-5.5 | 0.1984732824427481 | 0.04580152671755725 | 0.7557251908396947 | 0.11450381679389313 | 0.030534351145038167 | 0.8549618320610687 | -0.08396946564885496 | -0.015267175572519085 | 0.09923664122137399 |
| Gemini3.1ProPreview | State | Claude4.5Sonnet | Gemini3.1ProPreview | 0.1984732824427481 | 0.04580152671755725 | 0.7557251908396947 | 0.1450381679389313 | 0.015267175572519083 | 0.8396946564885496 | -0.0534351145038168 | -0.03053435114503817 | 0.08396946564885488 |
| Gemini3.1ProPreview | Transition | Claude4.5Sonnet | GPT-5.5 | 0.16842105263157894 | 0.08947368421052632 | 0.7421052631578947 | 0.08947368421052632 | 0.02631578947368421 | 0.8842105263157894 | -0.07894736842105263 | -0.06315789473684211 | 0.14210526315789473 |
| Gemini3.1ProPreview | Transition | Claude4.5Sonnet | Gemini3.1ProPreview | 0.16842105263157894 | 0.08947368421052632 | 0.7421052631578947 | 0.12105263157894737 | 0.02631578947368421 | 0.8526315789473684 | -0.047368421052631574 | -0.06315789473684211 | 0.1105263157894737 |
| Gemini3.1ProPreview | Action | Claude4.5Sonnet | GPT-5.5 | 0.3963963963963964 | 0.12612612612612611 | 0.4774774774774775 | 0.10810810810810811 | 0.06306306306306306 | 0.8288288288288288 | -0.2882882882882883 | -0.06306306306306306 | 0.3513513513513513 |
| Gemini3.1ProPreview | Action | Claude4.5Sonnet | Gemini3.1ProPreview | 0.3963963963963964 | 0.12612612612612611 | 0.4774774774774775 | 0.2702702702702703 | 0.0990990990990991 | 0.6306306306306306 | -0.12612612612612611 | -0.027027027027027015 | 0.15315315315315314 |
| Gemini3.1ProPreview | Region | Claude4.5Sonnet | GPT-5.5 | 0.5416666666666666 | 0.0 | 0.4583333333333333 | 0.5 | 0.0 | 0.5 | -0.04166666666666663 | 0.0 | 0.041666666666666685 |
| Gemini3.1ProPreview | Region | Claude4.5Sonnet | Gemini3.1ProPreview | 0.5416666666666666 | 0.0 | 0.4583333333333333 | 0.5 | 0.0 | 0.5 | -0.04166666666666663 | 0.0 | 0.041666666666666685 |
| Gemini3.1ProPreview | History State | Claude4.5Sonnet | GPT-5.5 | 0.7222222222222222 | 0.0 | 0.2777777777777778 | 0.6111111111111112 | 0.05555555555555555 | 0.3333333333333333 | -0.11111111111111105 | 0.05555555555555555 | 0.055555555555555525 |
| Gemini3.1ProPreview | History State | Claude4.5Sonnet | Gemini3.1ProPreview | 0.7222222222222222 | 0.0 | 0.2777777777777778 | 0.6111111111111112 | 0.0 | 0.3888888888888889 | -0.11111111111111105 | 0.0 | 0.1111111111111111 |
| Gemini3.1ProPreview | Guard | Claude4.5Sonnet | GPT-5.5 | 0.36363636363636365 | 0.09090909090909091 | 0.5454545454545454 | 0.18181818181818182 | 0.07575757575757576 | 0.7424242424242424 | -0.18181818181818182 | -0.015151515151515152 | 0.19696969696969702 |
| Gemini3.1ProPreview | Guard | Claude4.5Sonnet | Gemini3.1ProPreview | 0.36363636363636365 | 0.09090909090909091 | 0.5454545454545454 | 0.30303030303030304 | 0.07575757575757576 | 0.6212121212121212 | -0.06060606060606061 | -0.015151515151515152 | 0.0757575757575758 |
| Gemini3.1ProPreview | Overall Score | Claude4.5Sonnet | GPT-5.5 | 0.28546409807355516 | 0.07880910683012259 | 0.6357267950963222 | 0.15411558669001751 | 0.03852889667250438 | 0.8073555166374781 | -0.13134851138353765 | -0.04028021015761821 | 0.17162872154115583 |
| Gemini3.1ProPreview | Overall Score | Claude4.5Sonnet | Gemini3.1ProPreview | 0.28546409807355516 | 0.07880910683012259 | 0.6357267950963222 | 0.2171628721541156 | 0.04203152364273205 | 0.7408056042031523 | -0.06830122591943957 | -0.036777583187390536 | 0.1050788091068301 |

### rq3_cross_grader_rankings.csv

Source CSV: `_Figures/PaperExperimentData/rq3_cross_grader_rankings.csv`

Source script: `_scripts/summarize_paper_experiments.py`

Rows: 72

Description: RQ3 grader ordering by score-1 rate for each generator and model element.

| generator | model_element | grader | score_1_pct | rank_by_score_1 |
| --- | --- | --- | --- | --- |
| Claude4.5Sonnet | Composite State | Claude4.5Sonnet | 0.5806451612903226 | 1 |
| Claude4.5Sonnet | Composite State | GPT-5.5 | 0.5806451612903226 | 1 |
| Claude4.5Sonnet | Composite State | Gemini3.1ProPreview | 0.5806451612903226 | 1 |
| Claude4.5Sonnet | State | GPT-5.5 | 0.7633587786259542 | 1 |
| Claude4.5Sonnet | State | Gemini3.1ProPreview | 0.7557251908396947 | 2 |
| Claude4.5Sonnet | State | Claude4.5Sonnet | 0.7364341085271318 | 3 |
| Claude4.5Sonnet | Transition | Gemini3.1ProPreview | 0.7421052631578947 | 1 |
| Claude4.5Sonnet | Transition | GPT-5.5 | 0.7263157894736842 | 2 |
| Claude4.5Sonnet | Transition | Claude4.5Sonnet | 0.7157894736842105 | 3 |
| Claude4.5Sonnet | Action | GPT-5.5 | 0.5225225225225225 | 1 |
| Claude4.5Sonnet | Action | Gemini3.1ProPreview | 0.4774774774774775 | 2 |
| Claude4.5Sonnet | Action | Claude4.5Sonnet | 0.35135135135135137 | 3 |
| Claude4.5Sonnet | Region | GPT-5.5 | 0.5416666666666666 | 1 |
| Claude4.5Sonnet | Region | Claude4.5Sonnet | 0.4583333333333333 | 2 |
| Claude4.5Sonnet | Region | Gemini3.1ProPreview | 0.4583333333333333 | 2 |
| Claude4.5Sonnet | History State | GPT-5.5 | 0.2777777777777778 | 1 |
| Claude4.5Sonnet | History State | Gemini3.1ProPreview | 0.2777777777777778 | 1 |
| Claude4.5Sonnet | History State | Claude4.5Sonnet | 0.2222222222222222 | 3 |
| Claude4.5Sonnet | Guard | GPT-5.5 | 0.6060606060606061 | 1 |
| Claude4.5Sonnet | Guard | Gemini3.1ProPreview | 0.5454545454545454 | 2 |
| Claude4.5Sonnet | Guard | Claude4.5Sonnet | 0.45454545454545453 | 3 |
| Claude4.5Sonnet | Overall Score | GPT-5.5 | 0.6514886164623468 | 1 |
| Claude4.5Sonnet | Overall Score | Gemini3.1ProPreview | 0.6357267950963222 | 2 |
| Claude4.5Sonnet | Overall Score | Claude4.5Sonnet | 0.5852372583479789 | 3 |
| GPT-5.5 | Composite State | Gemini3.1ProPreview | 0.7096774193548387 | 1 |
| GPT-5.5 | Composite State | GPT-5.5 | 0.6774193548387096 | 2 |
| GPT-5.5 | Composite State | Claude4.5Sonnet | 0.6451612903225806 | 3 |
| GPT-5.5 | State | Claude4.5Sonnet | 0.8625954198473282 | 1 |
| GPT-5.5 | State | GPT-5.5 | 0.8625954198473282 | 1 |
| GPT-5.5 | State | Gemini3.1ProPreview | 0.8549618320610687 | 3 |
| GPT-5.5 | Transition | GPT-5.5 | 0.8842105263157894 | 1 |
| GPT-5.5 | Transition | Gemini3.1ProPreview | 0.8842105263157894 | 1 |
| GPT-5.5 | Transition | Claude4.5Sonnet | 0.8526315789473684 | 3 |
| GPT-5.5 | Action | GPT-5.5 | 0.8468468468468469 | 1 |
| GPT-5.5 | Action | Claude4.5Sonnet | 0.8288288288288288 | 2 |
| GPT-5.5 | Action | Gemini3.1ProPreview | 0.8288288288288288 | 2 |
| GPT-5.5 | Region | GPT-5.5 | 0.5833333333333334 | 1 |
| GPT-5.5 | Region | Claude4.5Sonnet | 0.5217391304347826 | 2 |
| GPT-5.5 | Region | Gemini3.1ProPreview | 0.5 | 3 |
| GPT-5.5 | History State | GPT-5.5 | 0.3888888888888889 | 1 |
| GPT-5.5 | History State | Claude4.5Sonnet | 0.3333333333333333 | 2 |
| GPT-5.5 | History State | Gemini3.1ProPreview | 0.3333333333333333 | 2 |
| GPT-5.5 | Guard | Claude4.5Sonnet | 0.803030303030303 | 1 |
| GPT-5.5 | Guard | GPT-5.5 | 0.7727272727272727 | 2 |
| GPT-5.5 | Guard | Gemini3.1ProPreview | 0.7424242424242424 | 3 |
| GPT-5.5 | Overall Score | GPT-5.5 | 0.819614711033275 | 1 |
| GPT-5.5 | Overall Score | Gemini3.1ProPreview | 0.8073555166374781 | 2 |
| GPT-5.5 | Overall Score | Claude4.5Sonnet | 0.8035087719298246 | 3 |
| Gemini3.1ProPreview | Composite State | GPT-5.5 | 0.6774193548387096 | 1 |
| Gemini3.1ProPreview | Composite State | Gemini3.1ProPreview | 0.6774193548387096 | 1 |
| Gemini3.1ProPreview | Composite State | Claude4.5Sonnet | 0.6129032258064516 | 3 |
| Gemini3.1ProPreview | State | GPT-5.5 | 0.8396946564885496 | 1 |
| Gemini3.1ProPreview | State | Gemini3.1ProPreview | 0.8396946564885496 | 1 |
| Gemini3.1ProPreview | State | Claude4.5Sonnet | 0.8015267175572519 | 3 |
| Gemini3.1ProPreview | Transition | Gemini3.1ProPreview | 0.8526315789473684 | 1 |
| Gemini3.1ProPreview | Transition | GPT-5.5 | 0.8210526315789474 | 2 |
| Gemini3.1ProPreview | Transition | Claude4.5Sonnet | 0.7789473684210526 | 3 |
| Gemini3.1ProPreview | Action | GPT-5.5 | 0.7027027027027027 | 1 |
| Gemini3.1ProPreview | Action | Gemini3.1ProPreview | 0.6306306306306306 | 2 |
| Gemini3.1ProPreview | Action | Claude4.5Sonnet | 0.45045045045045046 | 3 |
| Gemini3.1ProPreview | Region | Claude4.5Sonnet | 0.5 | 1 |
| Gemini3.1ProPreview | Region | GPT-5.5 | 0.5 | 1 |
| Gemini3.1ProPreview | Region | Gemini3.1ProPreview | 0.5 | 1 |
| Gemini3.1ProPreview | History State | Gemini3.1ProPreview | 0.3888888888888889 | 1 |
| Gemini3.1ProPreview | History State | GPT-5.5 | 0.3333333333333333 | 2 |
| Gemini3.1ProPreview | History State | Claude4.5Sonnet | 0.2777777777777778 | 3 |
| Gemini3.1ProPreview | Guard | GPT-5.5 | 0.6212121212121212 | 1 |
| Gemini3.1ProPreview | Guard | Gemini3.1ProPreview | 0.6212121212121212 | 1 |
| Gemini3.1ProPreview | Guard | Claude4.5Sonnet | 0.5606060606060606 | 3 |
| Gemini3.1ProPreview | Overall Score | GPT-5.5 | 0.7425569176882661 | 1 |
| Gemini3.1ProPreview | Overall Score | Gemini3.1ProPreview | 0.7408056042031523 | 2 |
| Gemini3.1ProPreview | Overall Score | Claude4.5Sonnet | 0.658493870402802 | 3 |
