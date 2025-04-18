import os
from call_api import Call
from processing import Correction_Structure
import pandas as pd
import json
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()


class DataWork:
    def __init__(self):
        pass
    

    def converte_to_df(self):
        data = self.read_json()
        df = pd.DataFrame(data)
        return df
    


if __name__ == "__main__":
    api_school = Call(os.getenv("ECOLE_API"))
    result_school = api_school.api_school()
    print(result_school)

    with open("school_control_0.json", "w", encoding="utf-8") as f:
        json.dump(result_school, f, indent=4, ensure_ascii=False)
    
    correction_structure = Correction_Structure()
    result_school_control = correction_structure.corriger_structure_ecole(result_school)
    print(result_school_control)
