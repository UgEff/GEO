# Projet Geotier

## Sources de Données

### API Publiques
- **Éducation**
  - ✅ API des établissements scolaires
  - Source : data.education.gouv.fr
  - Données : écoles, collèges, lycées parisiens

- **Sport**
  - ✅ API des équipements sportifs
  - Source : data.education.gouv.fr
  - Données : complexes sportifs, gymnases, piscines

### API OpenStreetMap
- **Transport**
  - ✅ Overpass API
  - Source : openstreetmap.org
  - Données : stations de métro parisiennes

### Fichiers Locaux
- **Santé**
  - ✅ Fichier JSON des établissements de santé
  - Source : fichier local data.gouv.fr
  - Données : hôpitaux parisiens

## Structure du Projet

### 1. Collecte des Données (`call_api.py`)
- ✅ Classe `Call`
  - `api_school()` : Récupération données écoles
  - `api_sport_complex()` : Récupération données sportives
  - `api_lines()` : Récupération stations métro
  - `api_hospitals()` : Lecture données hôpitaux

- ✅ Classe `File_Reader`
  - `select_hospitals()` : Traitement fichiers JSON
  - Géocodage des adresses

### 2. Traitement des Données (`processing.py`)
- ✅ Classe `Correction_Structure`
  - `corriger_structure_metro()` : Formatage données métro
  - `corriger_structure_ecole()` : Formatage données écoles
  - `corriger_structure_sport()` : Formatage données sportives
  - `corriger_structure_hopital()` : Formatage données hôpitaux

### 3. Conversion et Enrichissement (`3_convert_df.py`)
- ✅ Classe `DataWork`
  - `convert_to_df()` : Conversion en DataFrame
  - `add_lineage()` : Ajout informations de traçabilité
    - Source des données
    - Date d'extraction

## Format des Données Standardisé
Structure commune pour chaque établissement :
```json
{
    "nom_etablissement": "...",
    "adresse": "...",
    "code_postal": "75...",
    "latitude": 48.8...,
    "longitude": 2.3...,
    "VILLE": "PARIS",
    "DEPARTEMENT": "PARIS",
    "PAYS": "FRANCE",
    "source": "...",
    "date_extraction": "YYYY-MM-DD HH:MM:SS"
}
```

## Configuration Requise
- Python 3.x
- Fichier `.env` avec URLs des API :
  - ECOLE_API
  - SPORT_COMPLEXE_API
  - HOPITAUX_API
  - RATP_API

## Dépendances
- requests
- pandas
- json
- geopy
- python-dotenv

## Installation et Utilisation
1. Cloner le repository
2. Installer les dépendances : `pip install -r requirements.txt`
3. Configurer le fichier `.env` avec les URLs des API
4. Exécution :
   ```bash
   python call_api.py      # Collecte des données
   python processing.py    # Traitement des données
   python 3_convert_df.py  # Conversion en DataFrame et enrichissement
   ```

## Prochaines Étapes
- [ ] Visualisation cartographique
- [ ] Connexion a BDD
- [ ] Optimisation performances


## Auteur
Idir GUETTAB



