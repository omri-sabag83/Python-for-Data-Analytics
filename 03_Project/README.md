# Overview

Welcome to my analysis of the data job market, focusing on data analyst roles. This project was created out of a desire to navigate and understand the job market more effectively. It delves into the top-paying and in-demand skills to help find optimal job opportunities for data analysts.

The data sourced from [Luke Barousse's Python Course](https://lukebarousse.com/python) which provides a foundation for my analysis, containing detailed information on job titles, salaries, locations, and essential skills. Through a series of Python scripts, I explore key questions such as the most demanded skills, salary trends, and the intersection of demand and salary in data analytics.

> **Note:** this write-up describes the analysis as configured by default — `SELECTED_COUNTRY = "United Kingdom"` and `BENCHMARK_COUNTRY = "United States"` in [`config.py`](config.py). Point `config.py` at another market and the notebooks re-run against it, but this narrative won't follow automatically.

# The Questions

Below are the questions I want to answer in my project:

1. What are the skills most in demand for the top 4 most popular data roles?
2. How are in-demand skills trending for Data Analysts?
3. How well do jobs and skills pay for Data Analysts?
4. What are the optimal skills for data analysts to learn? (High Demand AND High Paying) 

# Tools I Used

For my deep dive into the data analyst job market, I harnessed the power of several key tools:

- **Python:** The backbone of my analysis, allowing me to analyze the data and find critical insights. I also used the following Python libraries:
    - **Pandas Library:** This was used to analyze the data. 
    - **Matplotlib Library:** I visualized the data.
    - **Seaborn Library:** Helped me create more advanced visuals. 
- **Jupyter Notebooks:** The tool I used to run my Python scripts which let me easily include my notes and analysis.
- **Visual Studio Code:** My go-to for executing my Python scripts.
- **Git & GitHub:** Essential for version control and sharing my Python code and analysis, ensuring collaboration and project tracking.

# Setup & Reproduce

To run this analysis yourself you need **Python 3.11** (the version it was tested with) and **Git**.

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd <repo-folder>

# 2. Create and activate an isolated virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install the pinned dependencies (requirements.txt is at the repo root)
pip install -r requirements.txt

# 4. Move into this project and launch Jupyter
cd 03_Project
jupyter lab
```

Then run the notebooks in order, `1_EDA_Intro` through `5_Optimal_Skills`. (Alternatively, open the folder in VS Code and run the notebooks with the Jupyter extension, selecting `.venv` as the kernel.)

To execute all five end to end from the command line — re-running every notebook and refreshing its saved output in place — run `make run` from this folder (`make clean` strips the outputs again). It just wraps `jupyter nbconvert --execute`, so plain `jupyter nbconvert --to notebook --execute --inplace *.ipynb` works too if you don't have `make`.

The first notebook you run calls `load_data()` from [`load_data.py`](load_data.py). On the first call it downloads the [`lukebarousse/data_jobs`](https://huggingface.co/datasets/lukebarousse/data_jobs) dataset from Hugging Face, cleans it, and caches the result to `data/data_jobs.parquet`. Every later call reads that local cache, so the download only happens once.

# Data Preparation and Cleanup

This section outlines the steps taken to prepare the data for analysis, ensuring accuracy and usability.

## Import & Clean Up Data

Each notebook starts by importing the libraries and loading the data. The download and cleaning steps live in a single helper, [`load_data.py`](load_data.py), so every notebook begins from the same cleaned DataFrame:

```python
# Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from load_data import load_data

# Load the cleaned dataset (downloads once, then reads a local cache)
df = load_data()
```

Inside `load_data()` the cleanup converts `job_posted_date` to a real datetime and parses the `job_skills` text (e.g. `"['sql', 'python']"`) into actual Python lists.

## Filter to One Country

The market to analyse is set once in [`config.py`](config.py) (default: United Kingdom) and every notebook imports it, so the whole analysis retargets from a single place:

```python
from config import SELECTED_COUNTRY

df_country = df[df['job_country'] == SELECTED_COUNTRY]
```

# The Analysis

Each Jupyter notebook for this project aimed at investigating specific aspects of the data job market. Here’s how I approached each question:

## 1. What are the most demanded skills for the top 4 most popular data roles?

To find the most demanded skills for the top 4 most popular data roles, I filtered to the 4 most common job titles and took the top 5 skills for each. This highlights which skills to pay attention to depending on the role I'm targeting. 

View my notebook with detailed steps here: [2_Skill_Demand](2_Skill_Demand.ipynb).

### Visualize Data

```python
fig, ax = plt.subplots(len(job_titles), 1)


for i, job_title in enumerate(job_titles):
    df_plot = df_skills_count[df_skills_count['job_title_short'] == job_title].head(top_n_skills)[::-1]
    sns.barplot(data=df_plot, x='skill_percent', y='job_skills', ax=ax[i], hue='skill_count', palette='dark:b_r')

plt.show()
```

### Results

![Likelihood of Skills Requested in UK Job Postings](images/skill_likelihood_united_kingdom.png)

*Bar graphs showing how often each of the top 5 skills appears in postings for the 4 most common roles in the UK data job market.*

### Insights:

- The four most common UK data roles are Data Engineer, Data Analyst, Data Scientist and Senior Data Engineer. SQL leads for Data Engineers (~60%) and Data Analysts (~43%); Python leads for Data Scientists (~69%) and Senior Data Engineers (~65%).
- The engineering roles lean on cloud/infrastructure skills — Azure ~40–41%, AWS ~33–42%, Spark ~18–23% — while Data Analysts skew toward BI and office tools: Excel ~41%, Power BI ~27%, Tableau ~16%.
- SQL and Python are the common thread across all 4 roles; for Data Analysts, Python sits only fourth (~20%), behind SQL, Excel and Power BI.

## 2. How are in-demand skills trending for Data Analysts?

To find how skills are trending in 2023 for Data Analysts, I filtered data analyst positions and grouped the skills by the month of the job postings. This got me the top skills of data analysts by month, showing how popular skills were throughout 2023.

View my notebook with detailed steps here: [3_Skills_Trend](3_Skills_Trend.ipynb).

### Visualize Data

```python

from matplotlib.ticker import PercentFormatter

df_plot = df_country_percent.iloc[:, :top_n_skills]
sns.lineplot(data=df_plot, dashes=False, legend='full', palette='tab10')

plt.gca().yaxis.set_major_formatter(PercentFormatter(decimals=0))

plt.show()

```

### Results

![Trending Top Skills for Data Analysts in the UK](images/trending_skills_da_united_kingdom.png)  
*Line chart of the trending top skills for data analysts in the UK across 2023.*

### Insights:
- SQL and Excel run neck-and-neck all year, both roughly in a ~38–47% band and trading the top spot from month to month (Excel actually leads in February at ~46%).
- Power BI holds a steady third place, ~24–33% of Data Analyst postings, with a mid-year bump in July.
- Python is a clear fourth, ~16–26%, drifting upward over the second half of the year — from ~16% in spring to ~23–26% by October–December.
- The lines are built from the normalised `job_title_short` category — about 10,500 UK Data Analyst postings across 2023.

## 3. How well do jobs and skills pay for Data Analysts?

To identify the highest-paying roles and skills, I only got jobs in the UK and looked at their median salary. But first I looked at the salary distributions of common data jobs like Data Scientist, Data Engineer, and Data Analyst, to get an idea of which jobs are paid the most. 

View my notebook with detailed steps here: [4_Salary_Analysis](4_Salary_Analysis.ipynb).

#### Visualize Data 

```python
sns.boxplot(data=df_country_top, x='salary_year_avg', y='job_title_short', order=job_order)

ticks_x = plt.FuncFormatter(lambda y, pos: f'${int(y/1000)}K')
plt.gca().xaxis.set_major_formatter(ticks_x)
plt.show()

```

#### Results

![Salary Distributions of Data Jobs in the UK](images/salary_distribution_data_jobs_united_kingdom.png)  
*Box plot visualizing the salary distributions for the Data Analyst/Scientist/Engineer and their respective Senior job titles.*

#### Insights

- Median pay tracks seniority: Senior Data Scientist (~$157K) and Senior Data Engineer (~$148K) are highest, then Senior Data Analyst (~$111K) and Data Engineer (~$110K), Data Scientist (~$105K), with Data Analyst lowest (~$88K).

- Sample sizes are healthier than a thin market but still modest at the senior end — `n` ranges from 8 (Senior Data Analyst) to 75 (Data Scientist), shown on the chart; the crimson diamonds mark the United States median for the same role as a reference point.

- Against that US reference, the UK senior roles land within ~2% of the US ($157K vs $155K, $148K vs $150K, $111K vs $110K). The mid-level roles sit **below** the US: Data Engineer $110K vs $125K (~−12%), Data Scientist $105K vs $130K (~−19%), Data Analyst $87.8K vs $90K (~−3%).

### Highest Paid & Most Demanded Skills for Data Analysts

Next, I narrowed my analysis and focused only on data analyst roles. I looked at the highest-paid skills and the most in-demand skills. I used two bar charts to showcase these.

#### Visualize Data

```python

fig, ax = plt.subplots(2, 1)

# Highest-paid skills for Data Analysts
sns.barplot(data=df_country_da_top_pay, x='median', y=df_country_da_top_pay.index, hue='median', ax=ax[0], palette='dark:b_r')

# Most in-demand skills for Data Analysts
sns.barplot(data=df_country_da_top_skills, x='median', y=df_country_da_top_skills.index, hue='median', ax=ax[1], palette='light:b')

plt.show()

```

#### Results
Here's the breakdown of the highest-paid & most in-demand skills for data analysts in the UK:

![The Highest Paid & Most In-Demand Skills for Data Analysts in the UK](images/highest_paid_in_demand_skills_united_kingdom.png)
*Two separate bar graphs visualizing the highest paid skills and most in-demand skills for data analysts in the UK. Each bar is annotated with `n` (postings behind the median); a crimson diamond marks the United States median for that skill.*

#### Insights:

- 12 of the 62 skills in UK Data Analyst postings clear the reliability floor (≥ 5 salaried postings); the other 50 are dropped rather than ranked on one or two data points.

- With 12 skills left, the "highest paid" and "most in-demand" lists genuinely differ: the best-paid are `tableau` ($100.5K), `sql` ($98.5K), `looker` ($96K) and `azure` ($92.5K), while the most in-demand are `sql` (~46% of postings), `excel` (~40%), `python` (~35%) and `tableau` (~18%).

- Against the United States median, only `tableau` and `sql` pay more in the UK (both ~+8%). Everything else pays less — `python` ~−9%, `excel` ~−11%, `r` ~−17% — and the office tools `word` (~−29%) and `outlook` (~−33%) are well below.

## 4. What are the most optimal skills to learn for Data Analysts?

To identify the most optimal skills to learn ( the ones that are the highest paid and highest in demand) I calculated the percent of skill demand and the median salary of these skills. To easily identify which are the most optimal skills to learn. 

View my notebook with detailed steps here: [5_Optimal_Skills](5_Optimal_Skills.ipynb).

#### Visualize Data

```python
# sel / bench: one row per skill (skill_percent, median_salary) for
# SELECTED_COUNTRY and BENCHMARK_COUNTRY respectively

plt.scatter(sel['skill_percent'], sel['median_salary'], label=SELECTED_COUNTRY)
plt.scatter(bench['skill_percent'], bench['median_salary'],
            facecolors='none', edgecolors='gray', label=BENCHMARK_COUNTRY)

# join each skill's two points so the demand/pay shift is visible
for s in sel.index:
    plt.plot([sel.loc[s, 'skill_percent'], bench.loc[s, 'skill_percent']],
             [sel.loc[s, 'median_salary'], bench.loc[s, 'median_salary']], color='gray', lw=0.8)

plt.legend()
plt.show()
```

#### Results

![Most Optimal Skills for Data Analysts in the UK](images/optimal_skills_da_united_kingdom.png)    
*A scatter plot visualizing the most optimal skills (high paying & high demand) for data analysts in the UK. Hollow points joined by a line show the same skills in the United States.*

#### Insights:

- `sql` is the stand-out optimal skill: the most in demand (~46% of postings) and near the top of the pay range (~$98.5K). `tableau` is the best-paid reliable skill (~$100.5K) but only ~18% of postings.

- `excel` and `python` are common (~40% and ~35% of postings) but mid-pack on pay (~$75.5K and ~$89K).

- Unlike a market that rewards these skills above the US, most UK points sit **below and to the left** of their United States counterparts. `sql` and `tableau` are the only two that clear their US pay marks (~+8% each); `python`, `excel`, `r` and the rest trail the US on pay, and several also on demand share.

### Visualizing Different Technologies

Let's visualize the different technologies as well in the graph. We'll add color labels based on the technology (e.g., {Programming: Python})

#### Visualize Data

```python
from matplotlib.ticker import PercentFormatter

# Create a scatter plot
scatter = sns.scatterplot(
    data=df_country_da_skills_tech_high_demand,
    x='skill_percent',
    y='median_salary',
    hue='technology',  # Color by technology
    palette='bright',  # Use a bright palette for distinct colors
    legend='full'  # Ensure the legend is shown
)
plt.show()

```

#### Results

![Most Optimal Skills for Data Analysts in the UK with Coloring by Technology](images/optimal_skills_da_colored_united_kingdom.png)  
*A scatter plot visualizing the most optimal skills (high paying & high demand) for data analysts in the UK with color labels for technology.*

#### Insights:

- Three technology groups clear the reliability floor: `programming` (`sql`, `python`, `r`, `go`, `sas`), `analyst_tools` (`excel`, `tableau`, `power bi`, `looker`, `outlook`, `word`, `sas`) and `cloud` (`azure`).

- The best demand/pay corner is held by `sql` (programming) and `tableau` (analyst_tools); the remaining analyst tools (`excel`, `power bi`, `looker`) and programming skills (`python`, `r`, `go`) cluster lower on pay.

- Cloud appears as a single point — `azure`, ~8% of postings and ~$92K — so cloud and database specialisation is still a small slice of the UK Data Analyst market.

# What I Learned

Throughout this project, I deepened my understanding of the data analyst job market and enhanced my technical skills in Python, especially in data manipulation and visualization. Here are a few specific things I learned:

- **Advanced Python Usage**: Utilizing libraries such as Pandas for data manipulation, Seaborn and Matplotlib for data visualization, and other libraries helped me perform complex data analysis tasks more efficiently.
- **Data Cleaning Importance**: I learned that thorough data cleaning and preparation are crucial before any analysis can be conducted, ensuring the accuracy of insights derived from the data.
- **Strategic Skill Analysis**: The project emphasized the importance of aligning one's skills with market demand. Understanding the relationship between skill demand, salary, and job availability allows for more strategic career planning in the tech industry.


# Insights

This project provided several general insights into the data job market for analysts:

- **Skill Demand and Salary Correlation**: There is a clear link between how often a skill is asked for and what it pays. For UK Data Analysts, SQL sits at the top of both axes, and SQL and Tableau are the only reliable skills that pay above their United States equivalent; other core skills (Python, Excel, R) are in demand but pay below the US benchmark.
- **Market Trends**: There are changing trends in skill demand, highlighting the dynamic nature of the data job market. Keeping up with these trends is essential for career growth in data analytics.
- **Economic Value of Skills**: Understanding which skills are both in-demand and well-compensated can guide data analysts in prioritizing learning to maximize their economic returns.


# Challenges I Faced

This project was not without its challenges, but it provided good learning opportunities:

- **Data Inconsistencies**: Handling missing or inconsistent data entries requires careful consideration and thorough data-cleaning techniques to ensure the integrity of the analysis.
- **Complex Data Visualization**: Designing effective visual representations of complex datasets was challenging but critical for conveying insights clearly and compellingly.
- **Balancing Breadth and Depth**: Deciding how deeply to dive into each analysis while maintaining a broad overview of the data landscape required constant balancing to ensure comprehensive coverage without getting lost in details.


# Conclusion

This exploration into the data analyst job market has been incredibly informative, highlighting the critical skills and trends that shape this evolving field. The insights I got enhance my understanding and provide actionable guidance for anyone looking to advance their career in data analytics. As the market continues to change, ongoing analysis will be essential to stay ahead in data analytics. This project is a good foundation for future explorations and underscores the importance of continuous learning and adaptation in the data field.


