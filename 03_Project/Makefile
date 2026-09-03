# Run the whole analysis end to end.
#
#   make run     execute notebooks 1-5 in order, in place, so the committed
#                .ipynb files hold freshly generated output
#   make clean   strip all notebook output again
#
# Needs the project dependencies installed (pip install -r ../requirements.txt).
# `make run` just wraps `jupyter nbconvert --execute`; the raw command in each
# target works without make if needed.

NOTEBOOKS := 1_EDA_Intro.ipynb 2_Skill_Demand.ipynb 3_Skills_Trend.ipynb 4_Salary_Analysis.ipynb 5_Optimal_Skills.ipynb

.PHONY: run clean

run:
	jupyter nbconvert --to notebook --execute --inplace \
		--ExecutePreprocessor.timeout=600 $(NOTEBOOKS)

clean:
	jupyter nbconvert --to notebook --clear-output --inplace $(NOTEBOOKS)
