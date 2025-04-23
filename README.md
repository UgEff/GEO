# Projet Geotier

[![Python](https://img.shields.io/badge/python-3.10-blue)](#)
[![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)](https://hub.docker.com/r/monregistry/projet_geotier)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)

## Aperçu

**Geotier** est un service de cartographie en cours de développement, axé sur divers aspects de la ville de Paris en utilisant plusieurs sources de données :

- **Écoles** (API Éducation nationale)
- **Complexes sportifs** (API Data.gouv.fr)
- **Stations de métro** (Overpass API / OpenStreetMap)
- **Hôpitaux** (fichier JSON Data.gouv.fr)

Les données collectées sont converties en DataFrame, enrichies (avec la source et la date d'extraction), puis insérées dans une base de données PostgreSQL.

Nous avons différentes sources de données, y compris des fichiers plats et des API. Les fichiers plats en entrée sont stockés dans le répertoire `json`, et nous utilisons la classe `File_Reader` pour les traiter. Il suffit de dupliquer la méthode de cette classe afin de l'adapter au format du fichier.

## Architecture

```plaintext
┌───────────┐    API    ┌───────────┐    DF    ┌───────┐
│ call_api  │ ───────▶ │ correction│ ───────▶ │ Data  │
│ (Collecte)│         │ (Traitement)│         │ Work  │
└───────────┘          └───────────┘         │ (Conversion,
                                              │  lignage)│
                                              └───────┘
                                                  │ BDD
                                                  ▼
                                              ┌────────┐
                                              │  Bdd   │
                                              │(Postgre│
                                              │SQL insert)
                                              └────────┘
```

## Composants

Le projet est composé de **4** modules principaux :

- **call_api.py** : Responsable de la collecte des données à partir de diverses sources.
- **processing.py** : Formate les données au format JSON, vérifie les latitudes et longitudes à l'aide de la bibliothèque `geopy`, et stocke un exemplaire des données en JSON dans le répertoire `json_prd`.
- **convert_df.py** : Convertit les données en DataFrame et gère le lignage des données.
- **bdd.py** : Gère la connexion à la base de données et l'alimentation de celle-ci.
- **main.py** : Coordonne l'exécution des différents modules.

## Prérequis

- Docker (optionnel pour la containerisation)
- Python 3.10+
- Base de données PostgreSQL (accessible via des variables d'environnement)

## Configuration

À la racine du projet, créez un fichier `.env` :

**Pour chaque nouvelle API, ajoutez une classe dans `call_api.py`. Il suffit de dupliquer les précédentes et d'apporter les modifications nécessaires en fonction de l'API.**

```dotenv
# URLs des APIs
ECOLE_API=https://data.education.gouv.fr/api/...
SPORT_COMPLEXE_API=https://data.education.gouv.fr/api/...
HOPITAUX_API=<chemin_vers_fichier_JSON>
RATP_API=http://overpass-api.de/api/interpreter

# PostgreSQL
DB_HOST=<adresse_de_la_base_de_données>
DB_PORT=<port_de_connexion>
DB_NAME=<nom_de_la_bdd>
DB_USER=<nom_d_utilisateur>
DB_PASSWORD=<mot_de_passe_de_la_bdd>
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

- Construction et push du conteneur Docker sur un registre privé ou Docker Hub.

```bash
docker build -t monregistry/projet_geotier:latest .
docker push monregistry/projet_geotier:latest
```

## Auteurs

- Idir GUETTAB




