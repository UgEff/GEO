import os
import sys
import json
from dotenv import load_dotenv
from datetime import datetime
import psycopg2
from call_api import Call, File_Reader
from processing import Correction_Structure
from convert_df import DataWork
from bdd import Bdd

load_dotenv()

if __name__ == "__main__":
    today=datetime.today().strftime("%A")
    # Exécution autorisée UNIQUEMENT le lundi (0 = lundi)
    #if today != "Monday":
        #print(f"Aujourd'hui nous somme {today}")
        #print("Execution du programme exclusivement les lundi")
        #sys.exit(0)

    # ECOLE --------------------------------------------------------------------------------
    # CALL API
    api_school = Call(os.getenv("ECOLE_API"))
    result_school = api_school.api_school()
    #PROCESSING
    correction_structure = Correction_Structure()
    result_school_processed = correction_structure.corriger_structure_ecole(result_school)
    #CONVERT TO DF
    data_worker = DataWork()
    df = data_worker.convert_to_df(result_school_processed)
    
    if df is not None:
        # Ajout des informations de lignage
        df_with_lineage = data_worker.add_lineage(df, 'ecole')
        # Sauvegarder le DataFrame en xlsx
        #df_with_lineage.to_excel('ecoles_data.xlsx', index=False)
    
    # INSERT INTO BDD
    bdd = Bdd()
    bdd.insert_ecole(df_with_lineage)
    bdd.close_conn()

    # COMPLEXE SPORTIF ----------------------------------------------------------------------
    # CALL API
    api_sport_complex = Call(os.getenv("SPORT_COMPLEXE_API"))
    result_sport_complex = api_sport_complex.api_sport_complex()
    
    #PROCESSING
    correction = Correction_Structure()
    complexes_formated = correction.corriger_structure_sport(result_sport_complex)

    # CONVERT TO DF
    data_worker = DataWork()
    df = data_worker.convert_to_df(complexes_formated)
    
    if df is not None:
        # Ajout des informations de lignage 
        df_with_lineage = data_worker.add_lineage(df, 'sport')

        # Sauvegarder le DataFrame en xlsx
        #df_with_lineage.to_excel('complexes_sportifs_data.xlsx', index=False)     

    # INSERT INTO BDD
    bdd = Bdd()
    bdd.insert_sport(df_with_lineage)
    bdd.close_conn()

    # HOPITAL -------------------------------------------------------------------------------
    # CALL API - FILL READER
    file_reader = File_Reader()
    result_hopital = file_reader.select_hospitals("json/hospitals_paris.json")

    # PROCESSING
    correction = Correction_Structure()
    result_hopital_control = correction.corriger_structure_hopital(result_hopital)

    # CONVERT TO DF
    datawork=DataWork()
    result_hopital_df=datawork.convert_to_df(result_hopital_control)
    if result_hopital_df is not None:
        df_with_lineage = datawork.add_lineage(result_hopital_df,'hopital')
        #df_with_lineage.to_excel('hopital.xlsx',index=False)

    # INSERT INTO BDD
    bdd = Bdd()
    bdd.insert_hopital(df_with_lineage)
    bdd.close_conn()


    # METRO ---------------------------------------------------------------------------------
    # CALL API
    api_metro = Call("http://overpass-api.de/api/interpreter")
    correction_structure = Correction_Structure()
    data_worker = DataWork()

    # PROCESSING
    result_metro = api_metro.api_lines()
    result_metro_correction = correction_structure.corriger_structure_metro(result_metro)
    
    # CONVERT TO DF
    df_metro = data_worker.convert_to_df(result_metro_correction)
    if df_metro is not None:
        df_with_lineage = data_worker.add_lineage(df_metro, 'metro')
        # Sauvegarder le DataFrame en xlsx avec l'extension
        #df_with_lineage.to_excel('test_metro_1.xlsx', index=False) 

    # INSERT INTO BDD
    bdd = Bdd()
    bdd.insert_metro(df_with_lineage)
    bdd.close_conn()

