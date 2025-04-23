# Geotier Project 🌍

[![Python](https://img.shields.io/badge/python-3.10-blue)](#)
[![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)](https://hub.docker.com/r/monregistry/projet_geotier)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)

## Overview 📖

**Geotier** is a mapping service currently under development, focusing on various aspects of the city of Paris using multiple data sources:

- **Schools** (National Education API) 🏫
- **Sports complexes** (Data.gouv.fr API) ⚽
- **Metro stations** (Overpass API / OpenStreetMap) 🚇
- **Hospitals** (Data.gouv.fr JSON file) 🏥

The collected data is converted into DataFrames, enriched (with source and extraction date), and then inserted into a PostgreSQL database.

We have different data sources, including flat files and APIs. The input flat files are stored in the `json` directory, and we use the `File_Reader` class to process them. Simply duplicate the method from this class to adapt it to the file format.

## Architecture 🏗️

```plaintext
┌───────────┐    API    ┌───────────┐    DF    ┌───────┐
│ call_api  │ ───────▶ │ correction│ ───────▶ │ Data  │
│ (Collect) │         │ (Processing)│         │ Work  │
└───────────┘          └───────────┘         │ (Conversion,
                                              │  Lineage)│
                                              └───────┘
                                                  │ BDD
                                                  ▼
                                              ┌────────┐
                                              │  Bdd   │
                                              │(Postgre│
                                              │SQL insert)
                                              └────────┘
```

## Components 🛠️

The project consists of **4** main modules:

- **call_api.py**: Responsible for collecting data from various sources.
- **processing.py**: Formats the data into JSON, checks latitudes and longitudes using the `geopy` library, and stores a copy of the data in JSON format in the `json_prd` directory.
- **convert_df.py**: Converts the data into DataFrames and manages data lineage.
- **bdd.py**: Manages the connection to the database and populates it.
- **main.py**: Coordinates the execution of the different modules.

## Prerequisites ⚙️

- Docker (optional for containerization)
- Python 3.10+
- PostgreSQL database (accessible via environment variables)

## Configuration ⚙️

At the root of the project, create a `.env` file:

**For each new API, add a class in `call_api.py`. Simply duplicate the previous ones and make the necessary modifications according to the API.**

```dotenv
# URLs of the APIs
ECOLE_API=https://data.education.gouv.fr/api/...
SPORT_COMPLEXE_API=https://data.education.gouv.fr/api/...
HOPITAUX_API=<path_to_JSON_file>
RATP_API=http://overpass-api.de/api/interpreter

# PostgreSQL
DB_HOST=<database_address>
DB_PORT=<connection_port>
DB_NAME=<database_name>
DB_USER=<username>
DB_PASSWORD=<database_password>
```

## Installation 🛠️

### With Docker 🐳

```bash
docker build -t projet_geotier .
docker run --env-file .env projet_geotier
```

### Locally 💻

```bash
pip install --upgrade pip
pip install -r requirements.txt
python app/main.py
```

## Usage 🚀

The main script `app/main.py` automatically executes all steps:
1. Data collection (call_api)
2. Processing and formatting (processing)
3. Conversion to DataFrame and enrichment (convert_df)
4. Insertion into PostgreSQL (bdd)

## Development 🧑‍💻

To run each module individually:

```bash
# Collection
python -m app.call_api
# Processing
python -m app.processing
# Conversion
python -m app.convert_df
# Full execution
python app/main.py
```

## Deployment 🚀

- Build and push the Docker container to a private registry or Docker Hub.

```bash
docker build -t monregistry/projet_geotier:latest .
docker push monregistry/projet_geotier:latest
```

## Authors ✍️

- Idir GUETTAB




