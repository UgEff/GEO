import os
import time
from call_api  import *
from processing import *
from convert_df import *


if __name__ == "__main__":


# ecole
    api_school = Call(os.getenv("ECOLE_API"))
    result_school = api_school.api_school()
    print(result_school)

    with open("school_control_0.json", "w", encoding="utf-8") as f:
        json.dump(result_school, f, indent=4, ensure_ascii=False)
    
    correction_structure = Correction_Structure()
    result_school_control = correction_structure.corriger_structure_ecole(result_school)
    print(result_school_control)

    with open("school_control_1.json", "w", encoding="utf-8") as f:
        json.dump(result_school_control, f, indent=4, ensure_ascii=False)

# complexe sportif
        
# Création des instances pour les complexes sportifs
    api_sport_complex = Call(os.getenv("SPORT_COMPLEXE_API"))
    result_sport_complex = api_sport_complex.api_sport_complex()
    
    # Création de l'instance de correction
    correction = Correction_Structure()
    
    # Correction et formatage des données des complexes sportifs
    complexes_formated = correction.corriger_structure_sport(result_sport_complex)
    

# hopital
    file_reader = File_Reader()
    result_hopital = file_reader.select_hospitals("json/hospitals_paris.json")
    print(result_hopital)

    with open("hopital_control_0.json", "w", encoding="utf-8") as f:
        json.dump(result_hopital, f, indent=4, ensure_ascii=False)

    # correction
    correction = Correction_Structure()
    result_hopital_control = correction.corriger_structure_hopital(result_hopital)
    print(result_hopital_control)

    with open("hopital_control_1.json", "w", encoding="utf-8") as f:
        json.dump(result_hopital_control, f, indent=4, ensure_ascii=False)

    # metro
    api_metro = Call("http://overpass-api.de/api/interpreter")
    result_metro = api_metro.api_lines()
    print(result_metro)
