"""
main.py
-------
Puro ETL pipeline ekshathe run kora hocche ei file theke.
Run command: python main.py
"""

import logging

from extract import extract_repositories, parse_repositories
from transform import transform_data
from load import create_table, load_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def run_pipeline():
    logger.info("===== ETL PIPELINE START =====")

    # ---------- EXTRACT ----------
    raw_items = extract_repositories()
    logger.info(f"Extract complete: {len(raw_items)} raw repository ana hoyeche.")
    parsed_items = parse_repositories(raw_items)

    # ---------- TRANSFORM ----------
    df = transform_data(parsed_items)

    # ---------- LOAD ----------
    create_table()
    load_data(df)

    logger.info("===== ETL PIPELINE COMPLETE =====")

    if not df.empty:
        print("\nTop 5 fastest-growing repositories:")
        print(df[["rank", "full_name", "stars", "growth_rate", "language"]].head(5).to_string(index=False))


if __name__ == "__main__":
    run_pipeline()
