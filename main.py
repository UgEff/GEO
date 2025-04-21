import json
import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from call_api import Call, File_Reader
from processing import Correction_Structure
from convert_df import DataWork

load_dotenv()

if __name__ == "__main__":
    today=datetime.today().strftime("%A")
    # Exécution autorisée UNIQUEMENT le lundi (0 = lundi)
    if today != "Monday":
        print(f"Aujourd'hui nous somme {today}")
        print("Execution du programme exclusivement les lundi")
        sys.exit(0)

        #Connexion a Postgre

        #Verification de l'existance des tables

        # 

