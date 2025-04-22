# Projet Geotier

[![Python](https://img.shields.io/badge/python-3.10-blue)](#)
[![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)](#)

## Aperçu

**Projet Geotier** est un service containerisé qui collecte, normalise et stocke des données géolocalisées pour la ville de Paris :
- **Écoles** (API Éducation nationale)
- **Complexes sportifs** (API Data.gouv.fr)
- **Stations de métro** (Overpass API / OpenStreetMap)
- **Hôpitaux** (fichier JSON Data.gouv.fr)

Les données sont converties en DataFrame, enrichies (source, date d'extraction) puis insérées dans une base PostgreSQL.

## Architecture

```plaintext
┌───────────┐    API    ┌───────────┐    DF    ┌───────┐
│ call_api  │ ───────▶ │ correction│ ───────▶ │ Data  │
│ (Collecte)│         │ (Traitement)│         │ Work  │
└───────────┘          └───────────┘         │ (Conversion,
                                              │  lignage)│
                                              └───────┘
                                                  │
                                                  ▼
                                              ┌────────┐
                                              │  Bdd   │
                                              │(Postgre│
                                              │SQL insert)
                                              └────────┘
```

## Prérequis

- Docker (optionnel pour la containerisation)
- Python 3.10+
- Base de données PostgreSQL (accessible via variables d'environnement)

## Configuration

À la racine du projet, créez un fichier `.env` :

```dotenv
# URLs des APIs
ECOLE_API=https://data.education.gouv.fr/api/...
SPORT_COMPLEXE_API=https://data.education.gouv.fr/api/...
HOPITAUX_API=<chemin_vers_fichier_JSON>
RATP_API=http://overpass-api.de/api/interpreter

# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=geotier_db
DB_USER=utilisateur
DB_PASSWORD=mot_de_passe
```

## Installation

### Avec Docker

```bash
docker build -t projet_geotier .
docker run --env-file .env projet_geotier
```

### En local

```bash
pip install --upgrade pip
pip install -r requirements.txt
python app/main.py
```

## Utilisation

Le script principal `app/main.py` exécute automatiquement toutes les étapes :
1. Collecte des données (call_api)
2. Traitement et formatage (processing)
3. Conversion en DataFrame et enrichissement (convert_df)
4. Insertion dans PostgreSQL (bdd)

## Développement

Pour lancer individuellement chaque module :

```bash
# Collecte
python -m app.call_api
# Traitement
python -m app.processing
# Conversion
python -m app.convert_df
# Exécution complète
python app/main.py
```

## Déploiement

- Construction et push du conteneur Docker sur un registry privé ou Docker Hub.

```bash
docker build -t monregistry/projet_geotier:latest .
docker push monregistry/projet_geotier:latest
```

## Auteurs

- Idir GUETTAB




