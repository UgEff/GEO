#-------------------------------------------------------------------------
#------------------------CLASSE CORRECTION STRUCTURE----------------------
#           classe qui permet de revoir la mise en forme des jsons 
import os
import json
from call_api import *


class Correction_Structure:
    

    def __init__(self):
        pass

    def corriger_structure_metro(self, result_metro):

        results = []
        
        for station in result_metro:
            if 'fields' in station:
                fields = station['fields']
                result = {
                    "nom_station": fields.get('name', 'Inconnu'),
                    "ligne": fields.get('line', 'Inconnue'),
                    "type_transport": fields.get('transportmode', 'metro'),
                    "operateur": fields.get('operator', 'RATP'),
                    "latitude": fields.get('latitude'),
                    "longitude": fields.get('longitude'),
                    "VILLE": "PARIS",
                    "DEPARTEMENT": "PARIS",
                    "PAYS": "FRANCE"
                }
                results.append(result)
        
        print(f"Nombre de stations de métro traitées : {len(results)}")
        return results

    def corriger_structure_ecole(self, result_school):

        results = []
        
        for ecole in result_school:
            if ecole.get('code_departement') == '075':  # Filtre sur Paris
                # Gestion sécurisée des coordonnées
                position = ecole.get('position', {})
                latitude = None
                longitude = None
                
                if position is not None:
                    latitude = position.get('lat')
                    longitude = position.get('lon')
                
                result = {
                    "nom_etablissement": ecole.get('nom_etablissement'),
                    "type_etablissement": ecole.get('type_etablissement'),
                    "statut_public_prive": ecole.get('statut_public_prive'),
                    "adresse_1": ecole.get('adresse_1'),
                    "code_postal": ecole.get('code_postal'),
                    "VILLE": "PARIS",
                    "DEPARTEMENT": "PARIS",
                    "PAYS": "FRANCE",
                    "latitude": latitude,
                    "longitude": longitude
                }
                results.append(result)
        
        print(f"Nombre d'écoles traitées : {len(results)}")
        return results

    def corriger_structure_sport(self, result_sport):

        results = []
        
        for complexe in result_sport:
            if complexe.get('inst_cp', '').startswith('75'):  # Filtre sur Paris
                # Gestion sécurisée des coordonnées
                coordonnees = complexe.get('coordonnees')
                latitude = None
                longitude = None
                
                if coordonnees is not None:
                    latitude = coordonnees.get('lat')
                    longitude = coordonnees.get('lon')
                
                result = {
                    "nom_etablissement": complexe.get('inst_nom'),
                    "adresse": complexe.get('inst_adresse'),
                    "code_postal": complexe.get('inst_cp'),
                    "type_equipement": complexe.get('equip_type_name'),
                    "famille_equipement": complexe.get('equip_type_famille'),
                    "VILLE": "PARIS",
                    "DEPARTEMENT": "PARIS",
                    "PAYS": "FRANCE",
                    "latitude": latitude,
                    "longitude": longitude
                }
                results.append(result)
        
        print(f"Nombre de complexes sportifs traités : {len(results)}")
        return results
    
    def select_sport_complex(self, result_complex):
        results = []

        for index, complex in enumerate(result_complex):
            result = {
                "inst_nom": complex.get("inst_nom"),
                "inst_adresse": complex.get("inst_adresse"),
                "inst_cp": complex.get("inst_cp"),
                "equip_type_name": complex.get("equip_type_name"),
                "equip_type_famille": complex.get("equip_type_famille"),
                "PAYS": "FRANCE",
                "VILLE": "PARIS",
                "DEPARTEMENT": "PARIS",
            }
            # Ajouter les coordonnées
            coordonnees = complex.get("coordonnees")
            if coordonnees is not None:
                result["latitude"] = coordonnees.get("lat")
                result["longitude"] = coordonnees.get("lon")
            else:
                result["latitude"] = None
                result["longitude"] = None

            results.append(result)

            print(f"Traitement du complexe {index + 1}/{len(result_complex)}")
        
        return results

    def corriger_structure_hopital(self, result_hopital):
        results = []
        
        for hopital in result_hopital:
            result = {
                "nom_etablissement": hopital.get('nom_etablissement'),
                "type_etablissement": hopital.get('type_etablissement'),
                "adresse": hopital.get('adresse_1'),
                "code_postal": hopital.get('code_postal'),
                "VILLE": "PARIS",
                "DEPARTEMENT": "PARIS",
                "PAYS": "FRANCE",
                "latitude": hopital.get('latitude'),
                "longitude": hopital.get('longitude')
            }
            results.append(result)

        for result in results:
            if result.get('adresse'):
                result['adresse'] = result['adresse'].replace(" R ", " RUE ")
            if result.get('adresse'):
                result['adresse'] = result['adresse'].replace(" AV ", " AVENUE ")
            if result.get('adresse'):
                result['adresse'] = result['adresse'].replace(" BD ", " BOULEVARD ")
            if result.get('adresse'):
                result['adresse'] = result['adresse'].replace(" SQ ", " SQUARE ")
            if result.get('adresse'):
                result['adresse'] = result['adresse'].replace(" PL ", " PLACE ")
            if result.get('adresse'):
                result['adresse'] = result['adresse'].replace(" BLD ", " BOULEVARD ")
            if result.get('adresse'):
                result['adresse'] = result['adresse'].replace(" FBG ", " FAUBOURG ")
            if result.get('adresse'):
                result['adresse'] = result['adresse'].replace(" RTE ", " ROUTE ")
        
        print(f"Nombre d'hôpitaux traités : {len(results)}")
        return results
    



