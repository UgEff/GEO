# Geotier Middleware for Urban Data

[![Geotier](https://img.shields.io/badge/Geotier-Paris-blue)](#)
[![Python3.10](https://img.shields.io/badge/python-3.10%2B-blue)](#)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)](https://hub.docker.com/r/monregistry/projet_geotier)

---

## Overview 📋

Geotier is a middleware data pipeline focused on centralizing public data for the city of **Paris**. It extracts, formats, enriches, and stores data in a PostgreSQL database to allow simplified access and future analysis.

Data sources include:

- 🏫 **National Education API** for schools
- ⚽ **Data.gouv APIs** for sports infrastructures
- 🚇 **OpenStreetMap Overpass API** for metro stations
- 🏥 **JSON data** for hospitals (offline file)

The collected data is normalized, enriched with metadata (source and extraction date), and saved in a PostgreSQL database.

---

## Architecture 🏗️

```plaintext
┌────────────┐    Collect    ┌────────────┐    Format    ┌────────────┐
│ call_api.py│ ───────────> │ processing │ ───────────> │ convert_df │
└────────────┘               └────────────┘              └────┬───────┘
                                                              ▼
                                                           PostgreSQL
                                                           (bdd.py)
```

---

## Modules 📦

| File           | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `call_api.py`  | Fetches data from external sources via API or local JSON                    |
| `processing.py`| Normalizes the structure of data (standard field names, coordinates, etc.) |
| `convert_df.py`| Converts cleaned data into Pandas DataFrames and adds metadata              |
| `bdd.py`       | Inserts data into the PostgreSQL database and creates the required tables   |
| `main.py`      | Orchestrates all modules; schedules and controls the entire workflow        |

---

## Quickstart 🚀

> ⚠️ This script is designed to run **only on Mondays** to simulate a weekly data refresh.

### 1. Setup your `.env` file 📁

At the root of the project, create a `.env` file with your environment variables:

```env
# API URLs
ECOLE_API=https://data.education.gouv.fr/api/...
SPORT_COMPLEXE_API=https://data.education.gouv.fr/api/...
HOPITAUX_API=./json/hospitals_paris.json
RATP_API=http://overpass-api.de/api/interpreter

# PostgreSQL Connection
DB_HOST=localhost
DB_PORT=5432
DB_NAME=geotier
DB_USER=postgres
DB_PASSWORD=password
```

### 2. Run the pipeline ▶️

```bash
python main.py
```

Or run each module manually if needed:

```bash
python call_api.py
python processing.py
python convert_df.py
python bdd.py
```

### 3. Result 📈

Your database is now populated with structured data for:

- Schools (ecole)
- Sports complexes (sport)
- Hospitals (hopital)
- Metro stations (metro)

---

## Docker Deployment 🐳

Build and run the pipeline in Docker:

```bash
docker build -t projet_geotier .
docker run --env-file .env projet_geotier
```

Push to Docker Hub:

```bash
docker tag projet_geotier monregistry/projet_geotier:latest
docker push monregistry/projet_geotier:latest
```

---

## Dev Notes 📝

### File Outputs
- Intermediate JSONs are saved in `json_prd/`
- All datasets are filtered to focus on Paris only (code postal 75)

### Customization
To add a new API:
- Duplicate a method in `Call` class (in `call_api.py`)
- Implement structure correction in `Correction_Structure`
- Convert via `DataWork` and insert using `Bdd`

---

## Database Modifications & Extensions 🗄️

To **modify the database schema** (e.g. add new columns or tables):

1. Open `bdd.py`
2. Locate the relevant `create_table_<type>()` method
3. Modify the SQL `CREATE TABLE` query accordingly (e.g. add new fields)
4. Restart the script to trigger table creation/update

To **add a new insertion method**:

1. Define a new method `insert_<type>()` inside `bdd.py`
2. It should accept a pandas DataFrame (`data`) and loop over its rows to insert into the appropriate table

To **add new logic for extraction or formatting**:
- Implement your new API logic in `call_api.py`
- Add a corresponding correction method in `processing.py`
- Use `convert_df.py` to convert it
- And finally insert it via `bdd.py`

> 💡 You can copy/paste from the existing structure (e.g., `insert_ecole`) to avoid writing from scratch.

---

## Author ✍️

- **Idir GUETTAB**




