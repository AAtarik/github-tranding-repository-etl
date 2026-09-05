"""
transform.py
------------
ETL er "T" (Transform) part. Raw data theke business logic apply kore
Growth Rate, Top Language, ebong Ranking ber kora hocche.
"""

import logging
from datetime import datetime, timezone
import pandas as pd

logger = logging.getLogger(__name__)


def calculate_growth_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Growth Rate (বৃদ্ধির হার):
    Repo create howar din theke ajke porjonto proti-din-e gore koto star peyeche
    tar hisab. Formula: stars / days_since_created

    Eta ekta proxy metric - GitHub API single call e historical star data dey na,
    tai "koto din e koto star" - eita diye bujha hocche repo ta koto fast growing.
    """
    df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
    now = datetime.now(timezone.utc)

    days = (now - df["created_at"]).dt.days
    # notun repo (0 din) hole divide-by-zero na hoy tar jonno minimum 1 din dhora hocche
    df["days_since_created"] = days.apply(lambda d: d if d > 0 else 1)

    df["growth_rate"] = (df["stars"] / df["days_since_created"]).round(2)
    return df


def add_ranking(df: pd.DataFrame) -> pd.DataFrame:
    """
    Growth Rate onujayi descending order e rank bosano hocche.
    Rank 1 = shobcheye fast-growing repository
    """
    df = df.sort_values(by="growth_rate", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1
    return df


def get_top_language(df: pd.DataFrame) -> str:
    """
    Puro dataset e shobcheye beshi ki language use hoyeche - eta ber kora hocche.
    """
    languages = df["language"].dropna()
    if languages.empty:
        return "Unknown"
    return languages.value_counts().idxmax()


def transform_data(parsed_items: list) -> pd.DataFrame:
    """
    Main transform function - shob transformation ek shathe apply kore
    final DataFrame return kore, jeta load.py e use hobe.
    """
    df = pd.DataFrame(parsed_items)

    if df.empty:
        logger.warning("Transform korar moto kono data nei.")
        return df

    df = calculate_growth_rate(df)
    df = add_ranking(df)

    top_language = get_top_language(df)
    df["top_language_overall"] = top_language

    logger.info(f"Transform complete. Overall top language: {top_language}")
    return df
