# Projet de Cartographie des Services Parisiens

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
  - Source : fichier local
  - Données : hôpitaux parisiens

## Fonctionnalités Implémentées

### Collecte des Données (`call_api.py`)
- ✅ Classe `Call`
  - Récupération données écoles
  - Récupération données sportives
  - Récupération stations métro
  - Lecture données hôpitaux

- ✅ Classe `File_Reader`
  - Traitement fichiers JSON
  - Géocodage des adresses

### Traitement des Données (`processing.py`)
- ✅ Classe `Correction_Structure`
  - Formatage données métro
  - Formatage données écoles
  - Formatage données sportives
  - Formatage données hôpitaux

## Configuration Requise
- Python 3.x
- Fichier `.env` avec URLs des API
- Dépendances : requests, json, geopy, python-dotenv

## Format des Données
Structure standardisée pour chaque établissement :
```json
{
    "nom_etablissement": "...",
    "adresse": "...",
    "code_postal": "75...",
    "latitude": 48.8...,
    "longitude": 2.3...,
    "VILLE": "PARIS",
    "DEPARTEMENT": "PARIS",
    "PAYS": "FRANCE"
}
```

## Utilisation
1. Configuration `.env`
2. Exécution collecte : `python call_api.py`
3. Exécution traitement : `python processing.py`

## Prochaines Étapes
- [ ] Visualisation cartographique
- [ ] Filtres de recherche
- [ ] Enrichissement métadonnées
- [ ] Optimisation performances
- [ ] Tests unitaires

## Auteur
Idir GUETTAB

