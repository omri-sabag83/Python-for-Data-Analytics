"""config.py - analysis parameters shared by every notebook in this project
(except 1_EDA_Intro, which is standalone exploration).

Edit a value here once; re-run notebooks 2-5 and they all pick it up. The
defaults below run the project as-is - nothing here needs changing to get output.
"""

# Job market the analysis focuses on. Must match a value in the dataset's
# 'job_country' column (e.g. "Israel", "United States", "United Kingdom", "India").
SELECTED_COUNTRY = "Israel"

# A larger, more mature market shown alongside SELECTED_COUNTRY for context
# (the benchmark diamonds / connector points on the salary charts in notebooks 4-5).
# Set it equal to SELECTED_COUNTRY to switch the benchmark overlays off.
BENCHMARK_COUNTRY = "United States"

# Reliability floor for salary figures: a median taken over only a handful of
# postings is noise, not signal. Skills with fewer than this many postings are
# dropped before any salary ranking (notebooks 4 and 5). Raise it for stricter
# results; lower it to keep more skills on a thin market.
MIN_SKILL_COUNT = 5
