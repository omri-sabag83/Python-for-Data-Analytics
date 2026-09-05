# 03_Project

Job-market analysis portfolio piece (Luke Barousse `data_jobs` dataset). Five
sequential notebooks: `1_EDA_Intro.ipynb` is a standalone exploration sandbox;
`2_Skill_Demand.ipynb` → `5_Optimal_Skills.ipynb` are driven by `config.py`.

## config.py vs inline params

`config.py` holds only parameters shared across multiple notebooks
(`SELECTED_COUNTRY`, `BENCHMARK_COUNTRY`, `MIN_SKILL_COUNT`). Per-section
display knobs (e.g. `skill_limit`, `top_n_skills`, `top_n_roles`) stay inline
in the notebook cell that uses them — do not promote them to `config.py`.

## Notebook 1 is out of scope for polish

`1_EDA_Intro.ipynb` is a personal sandbox, not part of the deliverable. Don't
wire it to `config.py`, and don't add markdown/comments to "document" it
unless asked.

## Execution environment

Always use the existing conda env `luke_barousse_course` (Python 3.11.13,
matches `requirements.txt`) — never base anaconda, which is missing
`datasets`/`adjustText`. Do not install or upgrade any packages; the env
already has everything needed. Execute notebooks via:

```
conda run -n luke_barousse_course jupyter nbconvert --to notebook --execute --inplace <notebook>
```

or `make run` (all notebooks) / `make clean` (strip output), which wrap the
same command. Chart image filenames in `images/` are derived from
`SELECTED_COUNTRY` (`country_slug`), so `make run` regenerates them
automatically after a country retarget.

## Docs

`README.md` lives in `03_Project/`, not the repo root — that's deliberate,
not an oversight.

## Git workflow

Solo repo, direct-to-`main`, no branches/PRs, no `gh` CLI. Only stage/commit/
push when explicitly asked in that turn; show the diff/`git status` for
review first.
