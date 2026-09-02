"""load_data.py — one place to load and clean the data_jobs dataset.

Every notebook in this project starts from the same DataFrame. Rather than
repeating the download-and-clean code at the top of each notebook, they all
import and call ``load_data()`` from here.

First call:  downloads the dataset from Hugging Face (a few hundred MB),
             applies the cleaning steps, and saves the result to a local
             Parquet file at ``03_Project/data/data_jobs.parquet``.
Later calls: read that Parquet file instead — fast, and works offline.

Usage inside a notebook (from the 03_Project folder):

    from load_data import load_data
    df = load_data()
"""

from pathlib import Path

import pandas as pd

# Resolve paths relative to THIS file, so it does not matter which folder the
# notebook is run from.
_PROJECT_DIR = Path(__file__).resolve().parent
_CACHE_PATH = _PROJECT_DIR / "data" / "data_jobs.parquet"

_DATASET_NAME = "lukebarousse/data_jobs"


def _download_and_clean() -> pd.DataFrame:
    """Download the raw dataset and apply the shared cleaning steps."""
    import ast

    from datasets import load_dataset

    print(f"Downloading '{_DATASET_NAME}' from Hugging Face (first run only)...")
    df = load_dataset(_DATASET_NAME)["train"].to_pandas()

    # 'job_posted_date' arrives as text -> convert to a real datetime.
    df["job_posted_date"] = pd.to_datetime(df["job_posted_date"])

    # 'job_skills' arrives as text that *looks* like a list, e.g. "['sql', 'python']".
    # ast.literal_eval turns that text into an actual Python list, leaving NaNs as-is.
    df["job_skills"] = df["job_skills"].apply(
        lambda skills: ast.literal_eval(skills) if pd.notna(skills) else skills
    )

    return df


def load_data(refresh: bool = False) -> pd.DataFrame:
    """Return the cleaned ``data_jobs`` DataFrame.

    Parameters
    ----------
    refresh : bool, default False
        If True, ignore any cached file, re-download, and rewrite the cache.
        Use this if the source dataset changes or the cache looks wrong.

    Notes
    -----
    After a round-trip through Parquet, each ``job_skills`` value comes back as a
    NumPy array (not a Python list) and missing values come back as ``None``.
    Both still work with ``df.explode('job_skills')`` and ``pd.notna(...)``.
    """
    if _CACHE_PATH.exists() and not refresh:
        return pd.read_parquet(_CACHE_PATH)

    df = _download_and_clean()

    _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(_CACHE_PATH, index=False)
    print(f"Cached cleaned data to {_CACHE_PATH}")

    return df
