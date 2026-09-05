
import os
from dotenv import load_dotenv

load_dotenv()  # .env file er content load kore environment e set kore dey

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_API_URL = "https://api.github.com/search/repositories"

SEARCH_QUERY = os.getenv("SEARCH_QUERY", "stars:>1000")
LANGUAGE_FILTER = os.getenv("LANGUAGE_FILTER", "")
FETCH_LIMIT = int(os.getenv("FETCH_LIMIT", "100"))

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "github_etl"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}
