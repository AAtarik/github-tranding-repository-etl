# GitHub Trending Repository ETL

GitHub API theke trending/popular repository extract kore, growth rate & ranking calculate kore, PostgreSQL e load kora hoy.

## Project Structure

```
github_etl/
├── .env.example       # env variable er template (copy kore .env banabe)
├── requirements.txt   # dorkari python library list
├── config.py          # shob configuration ekjaygay
├── extract.py         # Extract step - GitHub API theke data ana
├── transform.py       # Transform step - growth rate, top language, rank
├── load.py            # Load step - PostgreSQL e data pathano
├── main.py            # puro pipeline run korar entry point
└── README.md          # ei file
```

Ei shob file already toiri kore deya hoyeche - VS Code e project folder e rakho.

## Setup Steps (VS Code e)

### 1. Virtual environment banao
```bash
python -m venv venv
```

Activate koro:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Library install koro
```bash
pip install -r requirements.txt
```
Eta `requirements.txt` file e likha `requests`, `pandas`, `psycopg2-binary`, `python-dotenv` - shobgula ekshathe install kore dibe.

### 3. PostgreSQL Database toiri koro
PostgreSQL install thakte hobe (na thakle: https://www.postgresql.org/download/)

```bash
psql -U postgres
```
Tারপর psql shell e:
```sql
CREATE DATABASE github_etl;
```
Table (`github_trending_repos`) manually banate hobe na - `main.py` run korle `load.py` automatically create kore dibe.

### 4. `.env` file banao
`.env.example` file ta copy kore `.env` name e save koro:
```bash
cp .env.example .env
```
Tারপর `.env` file khule nijer values bosao:
- `DB_PASSWORD` → tomar PostgreSQL password
- `GITHUB_TOKEN` → (optional but recommended) GitHub e giye Settings → Developer Settings → Personal Access Tokens theke ekta token banao. Token dile rate limit onek beshi pabe (5000 request/hour, na dile 60/hour)
- `SEARCH_QUERY` → kon repo chao seta filter (default: `stars:>1000`)
- `LANGUAGE_FILTER` → specific language chaile (e.g. `Python`), na chaile empty rakho

### 5. Pipeline run koro
```bash
python main.py
```

Eta run hole:
1. GitHub theke repo data extract hobe
2. Growth rate, ranking, top language calculate hobe
3. PostgreSQL e `github_trending_repos` table e data upsert (insert/update) hobe
4. Terminal e top 5 fastest-growing repo print hobe

## File-wise ki hocche o kno (explanation)

| File | Ki kore | Kno lagbe |
|------|---------|-----------|
| `config.py` | `.env` theke shob setting load kore | Ekjaygay shob config rakhle onno file e change korte hoy na |
| `extract.py` | GitHub Search API ke call kore repo list ana hoy, pagination handle kore | Ei API `stars`, `forks`, `language`, `owner` shob dey ek response e |
| `transform.py` | `growth_rate = stars / days_since_created` calculate kore, tarpor rank bosay, ebong shobcheye common language ber kore | GitHub API directly "growth rate" dey na - tai created_at theke calculate korte hoy |
| `load.py` | PostgreSQL e connect kore, table create kore (na thakle), `ON CONFLICT` diye upsert kore | Same repo abar run korle duplicate row na hoye update hoy |
| `main.py` | Extract → Transform → Load - tinta step ke order e call kore | Pura pipeline ekta command diye run korar jonno |

## Growth Rate ki bhabe kaj kore

GitHub API single call e ekta repo koto din agee koto star chilo - eita dey na. Tai proxy hishebe:

```
growth_rate = total_stars / (days since repository created)
```

Mane repo ta create howar por theke protidin gore koto star peyeche - eita diye bujha jay kotota "fast" popularity peyeche. Beshi growth_rate mane newer repo o beshi star peyeche - mane fast trending.

**Note:** Ei method ta ek-time snapshot diye kaj kore. Age ei script ta prottidin (cron/scheduler diye) run korle, actual "week-over-week star growth" o track kora jabe - shetar jonno `loaded_at` column already table e rakha ache, jate history compare kora jay pore.

## Common Issues

- **`psycopg2.OperationalError: connection refused`** → PostgreSQL service run hocche kina check koro, `.env` e host/port thik ache kina dekho
- **`403 rate limit exceeded`** → `.env` e `GITHUB_TOKEN` add koro
- **Empty data** → `SEARCH_QUERY` khub restrictive hote pare, `stars:>1000` kore try koro
