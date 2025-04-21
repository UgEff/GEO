import os
from call_api import *
from processing import *
import pandas as pd
import json
from dotenv import load_dotenv

load_dotenv()


class DataWork:
    def __init__(self):
        # Définition des sources
        self.sources = {
            'ecole': 'API Education Nationale',
            'sport': 'API Equipements Sportifs',
            'metro': 'API OpenStreetMap',
            'hopital': 'Fichier Local Data gouv'
        }
    
    def convert_to_df(self, data):
        try:
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Erreur lors de la conversion en DataFrame : {str(e)}")
            return None

    def add_lineage(self, df, type_donnee, date_extraction=None):
        try:
            # Ajout de la source
            df['source'] = self.sources.get(type_donnee, 'Source inconnue')
            
            # Ajout de la date d'extraction
            if date_extraction:
                df['date_extraction'] = date_extraction
            else:
                from datetime import datetime
                df['date_extraction'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            return df
            
        except Exception as e:
            print(f"Erreur lors de l'ajout des champs de lignage : {str(e)}")
            return df
