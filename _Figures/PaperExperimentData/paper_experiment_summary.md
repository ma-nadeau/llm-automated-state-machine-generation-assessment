# Paper Experiment Summary

## RQ1: Claude Generation Quality From Human Assessment

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

| Grader | Model element | Items | Exact agreement | Macro P | Macro R | Macro F1 |
| --- | --- | --- | --- | --- | --- | --- |
| Claude4.5Sonnet | Composite State | 31 | 0.839 | 0.732 | 0.883 | 0.779 |
| Claude4.5Sonnet | State | 131 | 0.826 | 0.548 | 0.564 | 0.540 |
| Claude4.5Sonnet | Transition | 189 | 0.831 | 0.523 | 0.621 | 0.554 |
| Claude4.5Sonnet | Action | 112 | 0.634 | 0.556 | 0.544 | 0.506 |
| Claude4.5Sonnet | Region | 24 | 0.958 | 0.958 | 0.962 | 0.958 |
| Claude4.5Sonnet | History State | 18 | 0.737 | 0.571 | 0.500 | 0.750 |
| Claude4.5Sonnet | Guard | 66 | 0.773 | 0.685 | 0.750 | 0.695 |
| Claude4.5Sonnet | Overall Score | 571 | 0.787 | 0.583 | 0.638 | 0.599 |
| GPT-5.5 | Composite State | 31 | 0.903 | 0.750 | 0.933 | 0.765 |
| GPT-5.5 | State | 131 | 0.893 | 0.706 | 0.737 | 0.717 |
| GPT-5.5 | Transition | 189 | 0.841 | 0.625 | 0.684 | 0.641 |
| GPT-5.5 | Action | 112 | 0.670 | 0.652 | 0.668 | 0.540 |
| GPT-5.5 | Region | 24 | 0.958 | 0.667 | 0.955 | 0.976 |
| GPT-5.5 | History State | 18 | 0.789 | 0.556 | 0.542 | 0.812 |
| GPT-5.5 | Guard | 66 | 0.803 | 0.680 | 0.624 | 0.615 |
| GPT-5.5 | Overall Score | 571 | 0.822 | 0.644 | 0.679 | 0.646 |
| Gemini3.1ProPreview | Composite State | 31 | 0.903 | 0.773 | 0.933 | 0.824 |
| Gemini3.1ProPreview | State | 131 | 0.908 | 0.743 | 0.776 | 0.749 |
| Gemini3.1ProPreview | Transition | 189 | 0.884 | 0.636 | 0.727 | 0.666 |
| Gemini3.1ProPreview | Action | 112 | 0.688 | 0.520 | 0.486 | 0.744 |
| Gemini3.1ProPreview | Region | 24 | 0.958 | 0.958 | 0.962 | 0.958 |
| Gemini3.1ProPreview | History State | 18 | 0.789 | 0.857 | 0.542 | 0.801 |
| Gemini3.1ProPreview | Guard | 66 | 0.833 | 0.713 | 0.703 | 0.690 |
| Gemini3.1ProPreview | Overall Score | 571 | 0.846 | 0.644 | 0.693 | 0.662 |

## RQ2: Overall Confusion Matrices

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

## RQ3: Available Grading Trends For GPT/Gemini Generations

Note: the current repository contains GPT-5.5- and Gemini-generated state machines graded by Claude 4.5 Sonnet only. Additional GPT/Gemini grader runs are needed to compare all three grading trends for these generators.

| Generator | Grader | Model element | Items | Score 0 | Score 0.5 | Score 1 |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-5.5 | Claude4.5Sonnet | Action | 111 | 0.144 | 0.027 | 0.829 |
| GPT-5.5 | Claude4.5Sonnet | Composite State | 31 | 0.355 | 0.000 | 0.645 |
| GPT-5.5 | Claude4.5Sonnet | Guard | 66 | 0.182 | 0.015 | 0.803 |
| GPT-5.5 | Claude4.5Sonnet | History State | 18 | 0.667 | 0.000 | 0.333 |
| GPT-5.5 | Claude4.5Sonnet | Overall Score | 570 | 0.167 | 0.030 | 0.804 |
| GPT-5.5 | Claude4.5Sonnet | Region | 23 | 0.391 | 0.087 | 0.522 |
| GPT-5.5 | Claude4.5Sonnet | State | 131 | 0.130 | 0.008 | 0.863 |
| GPT-5.5 | Claude4.5Sonnet | Transition | 190 | 0.095 | 0.053 | 0.853 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Action | 111 | 0.477 | 0.072 | 0.450 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Composite State | 31 | 0.355 | 0.032 | 0.613 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Guard | 66 | 0.318 | 0.121 | 0.561 |
| Gemini3.1ProPreview | Claude4.5Sonnet | History State | 18 | 0.722 | 0.000 | 0.278 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Overall Score | 571 | 0.273 | 0.068 | 0.658 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Region | 24 | 0.458 | 0.042 | 0.500 |
| Gemini3.1ProPreview | Claude4.5Sonnet | State | 131 | 0.153 | 0.046 | 0.802 |
| Gemini3.1ProPreview | Claude4.5Sonnet | Transition | 190 | 0.142 | 0.079 | 0.779 |
