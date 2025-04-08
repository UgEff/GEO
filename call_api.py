import requests
import json
import time
import os

#-------------------------------------------------------------------------
#------------------------CLASSE APPEL API-------------------------------
#     classe qui permet d'appeler les API et de récupérer les données

class Call:
    def __init__(self,url) :
        self.url = url

    
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
        with open('school.json', 'w') as f:
            json.dump({"total_count": len(total_results), "results": total_results}, f)

        print(f"Total d'écoles récupérées : {len(total_results)}")

    def api_sport_complex(self):
        # URL de l'API pour les complexes sportifs
        #url = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-data-es-base-de-donnees/records"

        # Paramètres de la requête
        params = {
            "select": (
                "inst_numero,inst_nom,inst_adresse,inst_cp,inst_com_code,inst_com_nom,new_code,new_name,"
                "inst_actif,inst_etat,inst_date_creation,inst_date_etat,equip_type_code,equip_type_name,"
                "equip_type_famille,coordonnees"
            ),
            "where": "dep_code='75'",  # Correction ici
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

        # Enregistrer tous les résultats dans un fichier
        with open('sportcomplex.json', 'w') as f:
            json.dump({"total_count": len(total_results), "results": total_results}, f)

        print(f"Total d'complexe sportif récupérées : {len(total_results)}")

    def api_lines(self, transport_type=None):
        params = {
            "select": "station,trafic,reseau,ville",
            "limit": 100,
            "offset": 0
        }
        
        try:
            total_results = []
            offset = 0
            total_count = 1000  # Valeur arbitraire, à ajuster selon le nombre réel de stations
            
            while offset < total_count:
                params['offset'] = offset
                response = requests.get(self.url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('results', [])
                    if not results:  # Si plus de résultats, on sort de la boucle
                        break
                        
                    total_results.extend(results)
                    print(f"Récupéré {len(results)} stations avec offset {offset}")
                    offset += 100
                else:
                    print(f"Erreur: {response.status_code} - {response.text}")
                    break
                    
            # Sauvegarder les résultats dans un fichier JSON
            with open('stations.json', 'w', encoding='utf-8') as f:
                json.dump({
                    "total_count": len(total_results),
                    "results": total_results
                }, f, ensure_ascii=False, indent=2)
            
            print(f"Total de stations récupérées : {len(total_results)}")
                
        except Exception as e:
            print(f"Erreur lors de la récupération des stations : {str(e)}")

    def api_hospitals(self):
        # Charger le fichier JSON
        with open("les_etablissements_hospitaliers_franciliens.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extraire uniquement les établissements à Paris
        paris_only = [
            record for record in data
            if "fields" in record and "cp_ville" in record["fields"] and "PARIS" in record["fields"]["cp_ville"]
        ]

        # Sauvegarder les résultats dans un fichier JSON
        with open('hospitals_paris.json', 'w', encoding='utf-8') as f:
            json.dump({
                "total_count": len(paris_only),
                "results": paris_only
            }, f, ensure_ascii=False, indent=2)

        print(f"Total d'hôpitaux à Paris récupérés : {len(paris_only)}")

    def longlat_station(self):
        import json
        from geopy.geocoders import Nominatim
        from time import sleep

        # Charger les données JSON
        with open("stations_prd.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        stations = data["results"]
        geolocator = Nominatim(user_agent="station_locator")
        results = []

        for index, station in enumerate(stations):
            address = f"{station['station']}, {station['ville']}, Île-de-France, France"
            try:
                location = geolocator.geocode(address, timeout=10)
                if location:
                    station["latitude"] = location.latitude
                    station["longitude"] = location.longitude
                else:
                    station["latitude"] = None
                    station["longitude"] = None
            except Exception as e:
                print(f"Erreur pour {address}: {e}")
                station["latitude"] = None
                station["longitude"] = None
            
            results.append(station)
            print(f"Traitement de la station {index + 1}/{len(stations)}")  # Message de débogage
            sleep(0.5)  # Réduire le temps d'attente

        # Sauvegarder le résultat
        with open("stations_geo.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

#-------------------------------------------------------------------------
#------------------------CLASSE LECTURE FICHIER JSON----------------------
#  classe qui permet de lire les fichiers JSON et d'extraire que les données nécessaires


class File_Reader:
    def __init__(self, file_path):
        self.file_path = file_path

    def api_hospitals(self):
        # Charger le fichier JSON
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extraire uniquement les établissements à Paris
        paris_only = [
            record for record in data
            if "fields" in record and "cp_ville" in record["fields"] and "PARIS" in record["fields"]["cp_ville"]
        ]

        # Sauvegarder les résultats dans un fichier JSON
        with open('hospitals_paris.json', 'w', encoding='utf-8') as f:
            json.dump({
                "total_count": len(paris_only),
                "results": paris_only
            }, f, ensure_ascii=False, indent=2)

        print(f"Total d'hôpitaux à Paris récupérés : {len(paris_only)}")


#-------------------------------------------------------------------------
#------------------------CLASSE CORRECTION STRUCTURE----------------------
#           classe qui permet de revoir la mise en forme des jsons 

class correction_structure:
    def __init__(self, file_path_input, file_path_output):
        self.file_path_input = file_path_input
        self.file_path_output = file_path_output

    def corriger_structure(self):
        import json
        import os

        # Vérifier si les chemins de fichiers sont valides
        if not os.path.exists(self.file_path_input):
            raise FileNotFoundError(f"Le fichier {self.file_path_input} n'existe pas.")

        try:
            with open(self.file_path_input, "r", encoding="utf-8") as f:
                data = json.load(f)

            with open(self.file_path_output, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        except json.JSONDecodeError:
            print("Erreur de décodage JSON : le fichier peut être mal formatté.")
        except Exception as e:
            print(f"Une erreur est survenue : {e}")

    def longlat_station(self):
        import json
        from geopy.geocoders import Nominatim
        from time import sleep

        # Charger les données JSON
        with open(self.file_path_input, "r", encoding="utf-8") as f:
            data = json.load(f)

        stations = data["results"]
        geolocator = Nominatim(user_agent="station_locator")
        results = []

        for index, station in enumerate(stations):
            address = f"{station['station']}, {station['ville']}, Île-de-France, France"
            try:
                location = geolocator.geocode(address, timeout=10)
                if location:
                    station["latitude"] = location.latitude
                    station["longitude"] = location.longitude
                else:
                    station["latitude"] = None
                    station["longitude"] = None
            except Exception as e:
                print(f"Erreur pour {address}: {e}")
                station["latitude"] = None
                station["longitude"] = None
            
            results.append(station)
            print(f"Traitement de la station {index + 1}/{len(stations)}")  # Message de débogage
            sleep(0.5)  # Réduire le temps d'attente

        # Sauvegarder le résultat
        with open(self.file_path_output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)


if __name__=="__main__":
    #url_transport = "https://data.ratp.fr/api/explore/v2.1/catalog/datasets/trafic-annuel-entrant-par-station-du-reseau-ferre-2021/records"
    
    #api = Call()
    
    # Récupérer les stations
    #api.api_lines()
    
    # Chemin vers le fichier JSON contenant les établissements hospitaliers
    #file_path = "les_etablissements_hospitaliers_franciliens.json"
    
    # Créer une instance de la classe HospitalData
    #hospital_data = File_Reader(file_path)
    
    # Récupérer les hôpitaux à Paris
    #hospital_data.api_hospitals()

    # corriger la structure du fichier JSON
    #correction_structure(file_path_input="school.json", file_path_output="school_prd.json").corriger_structure()
    #correction_structure(file_path_input="hospitals_paris.json", file_path_output="hospitals_paris_prd.json").corriger_structure()
    #correction_structure(file_path_input="sportcomplex.json", file_path_output="sportcomplex_prd.json").corriger_structure()
    #correction_structure(file_path_input="stations.json", file_path_output="stations_prd.json").corriger_structure()
    #correction_structure(file_path_input="stations_prd.json", file_path_output="stations_geo.json").longlat_station()