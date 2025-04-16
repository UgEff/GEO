#-------------------------------------------------------------------------
#------------------------CLASSE CORRECTION STRUCTURE----------------------
#           classe qui permet de revoir la mise en forme des jsons 

class Correction_Structure:
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

    def select_sport_complex(self):
        import json

        # Charger le fichier JSON
        with open(self.file_path_input, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extraire les données nécessaires
        complex_sportif = data["results"]
        results = []

        for index, complex in enumerate(complex_sportif):
            result = {
                "inst_nom": complex["inst_nom"],
                "inst_adresse": complex["inst_adresse"],
                "inst_cp": complex["inst_cp"],
                "equip_type_name": complex["equip_type_name"],
                "equip_type_famille": complex["equip_type_famille"],
                "PAYS": "FRANCE",
                "VILLE": "PARIS",
                "DEPARTEMENT": "PARIS",
            }
            # Ajouter les coordonnées
            if complex["coordonnees"] is not None:
                result["latitude"] = complex["coordonnees"].get("lat")
            else:
                result["latitude"] = None
            if complex["coordonnees"] is not None:
                result["longitude"] = complex["coordonnees"].get("lon")
            else:
                result["longitude"] = None

            results.append(result)

            print(f"Traitement du complexe {index + 1}/{len(complex_sportif)}")
            
        
        # Sauvegarder les résultats dans un fichier JSON
        with open(self.file_path_output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

    def select_school(self):
        import json

        # Charger le fichier JSON
        with open(self.file_path_input, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extraire les données nécessaires
        etablissements = data["results"]
        results = []

        for index, etablissement in enumerate(etablissements):
            result = {
                "nom_etablissement": etablissement["nom_etablissement"],
                "type_etablissement": etablissement["type_etablissement"],
                "statut_public_prive": etablissement["statut_public_prive"],
                "adresse_1": etablissement["adresse_1"],
                "code_postal": etablissement["code_postal"],
                "VILEE": etablissement["nom_commune"],
                "DEPARTEMENT":"PARIS",
                "PAYS":"FRANCE",
            }

            if etablissement["position"] is not None:
                result["longitude"] = etablissement["position"].get("lat")
            else:
                result["longitude"] = None
            if etablissement["position"] is not None:
                result["latitude"] = etablissement["position"].get("lon")
            else:
                result["latitude"] = None

            results.append(result)

            print(f"Traitement de l'établissement {index + 1}/{len(etablissements)}")

        # Sauvegarder les résultats dans un fichier JSON    
        with open(self.file_path_output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

    def select_hospitals(self):
        # Initialiser le géocodeur
        geolocator = Nominatim(user_agent="hospital_locator")

        # Charger le fichier JSON
        with open(self.file_path_input, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extraire les données nécessaires
        etablissements = data.get("results", [])
        results = []

        if not etablissements:
            print("Aucun établissement trouvé dans le fichier JSON.")
            return  # Sortir de la méthode si aucun établissement n'est trouvé

        for index, etablissement in enumerate(etablissements):
            fields = etablissement.get("fields", {})
            adresse_complete = fields.get("adresse_complete", "")
            
            # Utiliser geopy pour obtenir la latitude et la longitude
            try:
                location = geolocator.geocode(adresse_complete, timeout=10)  # Augmenter le délai d'attente
                if location:
                    longitude = location.longitude
                    latitude = location.latitude
                else:
                    longitude = None
                    latitude = None
            except Exception as e:
                print(f"Erreur lors du géocodage de l'adresse '{adresse_complete}': {e}")
                longitude = None
                latitude = None

            result = {
                "type_etablissement": fields.get("categorie_de_l_etablissement", "Inconnu"),
                "nom_etablissement": fields.get("raison_sociale_entite_juridique", "Inconnu"),
                "PAYS": "FRANCE",
                "VILLE": fields.get("cp_ville", "").split()[1] if len(fields.get("cp_ville", "").split()) > 1 else "Inconnue",
                "DEPARTEMENT": fields.get("dept", "Inconnu"),
                "adresse_1": adresse_complete,
                "code_postal": fields.get("cp_ville", "").split()[0],  # Extraire le code postal
                "longitude": longitude,
                "latitude": latitude,
            }

            if result["DEPARTEMENT"] == "PARIS":
                results.append(result)

            print(f"Traitement de l'établissement {index + 1}/{len(etablissements)}")
            
            # Ajouter un délai entre les requêtes pour éviter d'être bloqué
            time.sleep(1)  # Délai d'une seconde

        # Sauvegarder les résultats dans un fichier JSON    
        with open(self.file_path_output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)