"""
load.py
-------
ETL er "L" (Load) part. Transform kora data PostgreSQL e insert/update kora hocche.
"""

import logging
import psycopg2
from psycopg2.extras import execute_values

from config import DB_CONFIG

logger = logging.getLogger(__name__)

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS github_trending_repos (
    repo_id BIGINT PRIMARY KEY,
    name TEXT,
    full_name TEXT,
    owner TEXT,
    stars INTEGER,
    forks INTEGER,
    language TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    url TEXT,
    days_since_created INTEGER,
    growth_rate NUMERIC,
    rank INTEGER,
    top_language_overall TEXT,
    loaded_at TIMESTAMP DEFAULT NOW()
);
"""

# ON CONFLICT diye "upsert" kora hocche - repo_id already thakle update, na thakle notun insert
UPSERT_QUERY = """
INSERT INTO github_trending_repos (
    repo_id, name, full_name, owner, stars, forks, language,
    created_at, updated_at, url, days_since_created, growth_rate,
    rank, top_language_overall
)
VALUES %s
ON CONFLICT (repo_id) DO UPDATE SET
    stars = EXCLUDED.stars,
    forks = EXCLUDED.forks,
    language = EXCLUDED.language,
    updated_at = EXCLUDED.updated_at,
    days_since_created = EXCLUDED.days_since_created,
    growth_rate = EXCLUDED.growth_rate,
    rank = EXCLUDED.rank,
    top_language_overall = EXCLUDED.top_language_overall,
    loaded_at = NOW();
"""


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def create_table():
    """Table na thakle create kore dey. Already thakle kichu hoy na."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_QUERY)
        conn.commit()
        logger.info("Table ready: github_trending_repos")
    finally:
        conn.close()


def load_data(df):
    """DataFrame theke row gula PostgreSQL e batch insert/upsert kore."""
    if df.empty:
        logger.warning("DataFrame empty, load korar kichu nei.")
        return

    columns = [
        "repo_id", "name", "full_name", "owner", "stars", "forks", "language",
        "created_at", "updated_at", "url", "days_since_created", "growth_rate",
        "rank", "top_language_overall"
    ]
    records = df[columns].values.tolist()

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            execute_values(cur, UPSERT_QUERY, records)
        conn.commit()
        logger.info(f"{len(records)} ta row PostgreSQL e load kora hoyeche.")
    finally:
        conn.close()
