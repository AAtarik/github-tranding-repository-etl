"""
GitHub API doc: https://docs.github.com/en/rest/search/search#search-repositories
"""

import logging
import requests

from config import GITHUB_API_URL, GITHUB_TOKEN, SEARCH_QUERY, LANGUAGE_FILTER, FETCH_LIMIT

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def build_query() -> str:
    """Search query string banano hocche - SEARCH_QUERY + optional language filter"""
    query = SEARCH_QUERY
    if LANGUAGE_FILTER:
        query += f" language:{LANGUAGE_FILTER}"
    return query


def extract_repositories() -> list:
    """
    GitHub API theke repository list fetch kore.
    Pagination handle kora hoyeche jate FETCH_LIMIT porjonto data ana jay.
    Return: raw JSON items er list (list of dict)
    """
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    all_items = []
    per_page = 100
    pages_needed = (FETCH_LIMIT // per_page) + 1

    for page in range(1, pages_needed + 1):
        params = {
            "q": build_query(),
            "sort": "stars",
            "order": "desc",
            "per_page": per_page,
            "page": page,
        }

        logger.info(f"GitHub API theke page {page} fetch kora hocche...")
        response = requests.get(GITHUB_API_URL, headers=headers, params=params, timeout=30)

        if response.status_code != 200:
            logger.error(f"GitHub API error: {response.status_code} - {response.text}")
            break

        data = response.json()
        items = data.get("items", [])

        if not items:
            break

        all_items.extend(items)

        if len(all_items) >= FETCH_LIMIT:
            break

    return all_items[:FETCH_LIMIT]


def parse_repositories(raw_items: list) -> list:
    """
    Raw GitHub JSON theke dorkari field gula ber kore clean dict list banano hocche.
    """
    parsed = []
    for item in raw_items:
        parsed.append({
            "repo_id": item.get("id"),
            "name": item.get("name"),
            "full_name": item.get("full_name"),
            "owner": item.get("owner", {}).get("login") if item.get("owner") else None,
            "stars": item.get("stargazers_count", 0),
            "forks": item.get("forks_count", 0),
            "language": item.get("language"),
            "created_at": item.get("created_at"),
            "updated_at": item.get("updated_at"),
            "url": item.get("html_url"),
        })
    return parsed


if __name__ == "__main__":
    # Ei file ta direct run korle test hishebe kaj korbe
    raw = extract_repositories()
    parsed = parse_repositories(raw)
    print(f"Total {len(parsed)} repositories extract hoyeche.")
    if parsed:
        print(parsed[0])
