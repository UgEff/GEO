import os
import time
from call_api  import *
from processing import *
from convert_df import *


if __name__ == "__main__":


# ecole
# Exemple d'utilisation
    api_school = Call(os.getenv("ECOLE_API"))
    result_school = api_school.api_school()
    
    correction_structure = Correction_Structure()
    result_school_processed = correction_structure.corriger_structure_ecole(result_school)
    
    # Conversion en DataFrame et ajout du lignage
    data_worker = DataWork()
    df = data_worker.convert_to_df(result_school_processed)
    
    if df is not None:
        # Ajout des informations de lignage
        df_with_lineage = data_worker.add_lineage(df, 'ecole')
        
        print("Aperçu du DataFrame avec lignage :")
        print(df_with_lineage.head())
        
        # Afficher les colonnes pour vérifier les nouveaux champs
        print("\nColonnes du DataFrame :")
        print(df_with_lineage.columns.tolist())

        # Sauvegarder le DataFrame en xlsx
        df_with_lineage.to_excel('ecoles_data.xlsx', index=False)

# complexe sportif
   # Création des instances pour les complexes sportifs
    api_sport_complex = Call(os.getenv("SPORT_COMPLEXE_API"))
    result_sport_complex = api_sport_complex.api_sport_complex()
    
    # Création de l'instance de correction
    correction = Correction_Structure()
    
    # Correction et formatage des données des complexes sportifs
    complexes_formated = correction.corriger_structure_sport(result_sport_complex)

    # Conversion en DataFrame
    data_worker = DataWork()
    df = data_worker.convert_to_df(complexes_formated)
    
    if df is not None:
        # Ajout des informations de lignage 
        df_with_lineage = data_worker.add_lineage(df, 'sport')
        
        print("Aperçu du DataFrame avec lignage :")
        print(df_with_lineage.head())
        
        # Afficher les colonnes pour vérifier les nouveaux champs   
        print("\nColonnes du DataFrame :")
        print(df_with_lineage.columns.tolist())

        # Sauvegarder le DataFrame en xlsx
        df_with_lineage.to_excel('complexes_sportifs_data.xlsx', index=False)     

    

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
