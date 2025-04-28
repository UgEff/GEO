import json
import os
import time

import requests
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()
#print les variables d'environnement
print(f'ECOLE_API: {os.getenv("ECOLE_API")}')
print(f'SPORT_COMPLEXE_API: {os.getenv("SPORT_COMPLEXE_API")}')
print(f'HOPITAUX_API: {os.getenv("HOPITAUX_API")}')
print(f'RATP_API: {os.getenv("RATP_API")}')

#-------------------------------------------------------------------------
#------------------------CLASSE APPEL API-------------------------------
#     classe qui permet d'appeler les API et de récupérer les données

class Call:
    def __init__(self, url):
        self.url = url

    # methode API ECOLE
    def api_school(self):
        # Paramètres de la requête
        params = {
            "select": (
                "identifiant_de_l_etablissement,nom_etablissement,type_etablissement,"
                "statut_public_prive,adresse_1,adresse_2,adresse_3,code_postal,code_commune,"
                "nom_commune,code_departement,code_academie,code_region,ecole_maternelle,"
                "ecole_elementaire,voie_generale,voie_technologique,voie_professionnelle,"
                "restauration,hebergement,ulis,apprentissage,segpa,section_arts,section_cinema,"
                "section_theatre,section_sport,section_internationale,section_europeenne,"
                "lycee_agricole,lycee_militaire,lycee_des_metiers,post_bac,appartenance_education_prioritaire,greta,position"
            ),
            "where": "code_departement='075'",
            "refine": "libelle_region:Ile-de-France", 
            "limit": 100,
            "offset": 0
        }

        total_results = []  # Liste pour stocker tous les résultats
        total_count = 1490  # Nombre total d'écoles à récupérer
        offset = 0  # Initialiser l'offset

        while offset < total_count:
            params['offset'] = offset  # Mettre à jour l'offset dans les paramètres
            response = requests.get(self.url, params=params)

            if response.status_code == 200:
                try:
                    data_return = response.json()
                    total_results.extend(data_return['results'])  # Ajouter les résultats à la liste
                    print(f"LOG: keep {len(data_return['results'])} school with offset {offset}")
                except json.JSONDecodeError as e:
                    print(f"LOG: Erreur lors du décodage JSON : {e}")
                    break
            else:
                print(f"ERROR: {response.status_code} - {response.text}")
                break  # Sortir de la boucle en cas d'erreur

            offset += 100  # Incrémenter l'offset de 100

        # Enregistrer tous les résultats dans un fichier après la boucle
        with open('json_prd/school.json', 'w') as f:
            json.dump({"total_count": len(total_results), "results": total_results}, f)

        print(f"Total d'écoles récupérées : {len(total_results)}")

        return total_results  # Retourner les résultats

    # methode API SPORT COMPLEXE
    def api_sport_complex(self):
        # URL de l'API pour les complexes sportifs
        #url = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-data-es-base-de-donnees/records"

        # Paramètres de la requête
        params = {
            "select": (
                "inst_numero,inst_nom,inst_adresse,inst_cp,new_code,new_name,"
                "equip_type_code,equip_type_name,equip_type_famille,coordonnees"
            ),
            "where": "dep_code='75'",
            "refine": "inst_part_type_filter:Complexe sportif",
            "limit": 100,
            "offset": 0
        }

        total_results = []  # Liste pour stocker tous les résultats
        total_count = 1500  # Nombre total de complexes sportifs à récupérer
        offset = 0  # Initialiser l'offset

        while offset < total_count:
            params['offset'] = offset  # Mettre à jour l'offset dans les paramètres
            response = requests.get(self.url, params=params)

            if response.status_code == 200:
                data = response.json()
                total_results.extend(data['results'])  # Ajouter les résultats à la liste
                print(f"Récupéré {len(data['results'])} complexe sportif à partir de l'offset {offset}.")
            else:
                print(f"Erreur: {response.status_code} - {response.text}")  # Afficher le message d'erreur
                break  # Sortir de la boucle en cas d'erreur

            offset += 100  # Incrémenter l'offset de 100

        # Enregistrer tous les résultats dans un fichier JSON avec un encodage UTF-8
        # Cela permet de s'assurer que les caractères spéciaux sont correctement gérés
        with open('json_prd/sportcomplex.json', 'w', encoding='utf-8') as f:
            json.dump({"total_count": len(total_results), "results": total_results}, f, ensure_ascii=False, indent=2)

        print(f"Total de complexes sportifs récupérés : {len(total_results)}")

        return total_results  # Retourner les résultats

    # methode API LIGNES DE METRO /!\ a verifier 
    def api_lines(self, transport_type=None):
        try:
            # Configuration de la requête Overpass
            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = """
            [out:json][timeout:60];
            area["name"="Paris"]["admin_level"="8"]->.searchArea;
            (
                node["station"="subway"](area.searchArea);
                node["railway"="station"]["subway"="yes"](area.searchArea);
            );
            out body;
            """

            # Envoi de la requête
            print("Récupération des stations de métro...")
            response = requests.get(overpass_url, params={'data': overpass_query})
            response_data = response.json()  # Stoker la réponse de l'API dans une variable
            
            if response.status_code == 200:
                if 'elements' in response_data:
                    # Traitement des données
                    stations = []
                    for element in response_data['elements']:
                        if element['type'] == 'node':
                            station = {
                                'fields': {
                                    'name': element['tags'].get('name', 'Sans nom'),
                                    'transportmode': 'metro',
                                    'latitude': element.get('lat'),
                                    'longitude': element.get('lon'),
                                    'line': element['tags'].get('line', ''),
                                    'operator': element['tags'].get('operator', 'RATP')
                                }
                            }
                            stations.append(station)

                    with open('json_prd/metro.json', 'w') as f:
                        json.dump({"total_count": len(stations), "results": stations}, f)

                    print(f"Nombre total de stations trouvées : {len(stations)}")
                    return stations
                else:
                    print("Aucune station trouvée dans la réponse")
                    return []
                    
            else:
                print(f"Erreur lors de la requête : {response.status_code} - {response.text}")
                return []
            
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion : {str(e)}")
            return []
        except KeyError as e:
            print(f"Erreur dans le format des données : {str(e)}")
            return []
        except Exception as e:
            print(f"Erreur inattendue : {str(e)}")


            return []

    # methode API HOPITAUX
    def api_hospitals(self):
        # Charger le fichier JSON
        hospitals_json_path = os.getenv("HOSPITALS_JSON_PATH")
        try:
            with open(hospitals_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Erreur : le fichier '{hospitals_json_path}' est introuvable.")
            return []  # Retourner une liste vide si le fichier n'est pas trouvé

        # Extraire uniquement les établissements à Paris
        paris_only = [
            record for record in data
            if "fields" in record and "cp_ville" in record["fields"] and "PARIS" in record["fields"]["cp_ville"]
        ]

        # Sauvegarder les résultats dans un fichier JSON
        with open('json/hospitals_paris.json', 'w', encoding='utf-8') as f:
            json.dump({
                "total_count": len(paris_only),
                "results": paris_only
            }, f, ensure_ascii=False, indent=2)

        print(f"Total d'hôpitaux à Paris récupérés : {len(paris_only)}")
        return paris_only  # Retourner les résultats


#-------------------------------------------------------------------------
#------------------------ CLASSE LECTURE FICHIER JSON ----------------------
#  classe qui permet de lire les fichiers JSON et d'extraire que les données nécessaires


class File_Reader:
    def __init__(self):
        pass

    def select_hospitals(self, file_path_input):
        # Charger le fichier JSON
        try:
            with open(file_path_input, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Erreur : le fichier '{file_path_input}' est introuvable.")
            return []

        # Filtrer uniquement les établissements de Paris
        etablissements_paris = [
            etablissement for etablissement in data.get("results", [])
            if etablissement.get("fields", {}).get("dept") == "PARIS"
        ]

        if not etablissements_paris:
            print("Aucun établissement parisien trouvé dans le fichier JSON.")
            return []

        # Dictionnaire des abréviations à remplacer
        abreviations = {
            " R ": " RUE ",
            " AV ": " AVENUE ",
            " BD ": " BOULEVARD ",
            " SQ ": " SQUARE ",
            " PL ": " PLACE ",
            " BLD ": " BOULEVARD ",
            " FBG ": " FAUBOURG ",
            " RTE ": " ROUTE ",
            " QU ": " QUAI ",
            " QUA ": " QUAI ",
            " VLA ": " VILLAGE ",
            " IMP ": " IMPASSE "
        }

        results = []
        geolocator = Nominatim(user_agent="hospital_locator")

        for index, etablissement in enumerate(etablissements_paris):
            fields = etablissement.get("fields", {})
            adresse_complete = fields.get("adresse_complete", "")

            # Corriger les abréviations dans l'adresse
            for abrev, complet in abreviations.items():
                adresse_complete = adresse_complete.replace(abrev, complet)

            # Obtenir les coordonnées géographiques
            """""
            try:
                location = geolocator.geocode(adresse_complete, timeout=10)
                longitude = location.longitude if location else None
                latitude = location.latitude if location else None
            except Exception as e:
                print(f"Erreur lors du géocodage de l'adresse '{adresse_complete}': {e}")
                longitude = None
                latitude = None
            """
            result = {
                "type_etablissement": fields.get("categorie_de_l_etablissement", ""),
                "nom_etablissement": fields.get("raison_sociale_entite_juridique", ""),
                "PAYS": "FRANCE",
                "VILLE": fields.get("cp_ville", "").split()[1] if len(fields.get("cp_ville", "").split()) > 1 else "",
                "DEPARTEMENT": fields.get("dept", ""),
                "adresse_1": adresse_complete,
                "code_postal": fields.get("cp_ville", "").split()[0],
                "longitude": fields.get("wgs84", "")[1],
                "latitude": fields.get("wgs84", "")[0],
            }

            results.append(result)
            #time.sleep(0.1)  # Délai entre les requêtes
            # Afficher le résultat et l'avancement
            print(f"Traitement de l'établissement {index + 1}/{len(etablissements_paris)}")

        # Sauvegarder les résultats
        with open('json_prd/hospitals_paris.json', 'w', encoding='utf-8') as f:
            json.dump({"total_count": len(results), "results": results}, f, ensure_ascii=False, indent=2)

        return results


if __name__ == "__main__":
    file_reader = File_Reader()
    file_reader.select_hospitals("json/hospitals_paris.json")
    