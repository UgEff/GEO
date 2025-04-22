import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class Bdd:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"))
        print("Connexion réussie")
        # Création et mise à jour des tables à chaque connexion
        self.create_table_hopital()
        self.create_table_ecole()
        self.create_table_sport()
        self.create_table_metro()
        
    def get_conn(self):
        print("Connexion réussie")
        return self.conn
    
    def close_conn(self):
        print("Fermeture de la connexion")
        self.conn.close()
        
    def create_table_hopital(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hopital (
                id SERIAL PRIMARY KEY,
                NOM_ETABLISSEMENT VARCHAR(255),
                TYPE_ETABLISSEMENT VARCHAR(255),
                ADRESSE VARCHAR(255),
                CODE_POSTAL INTEGER,
                VILLE VARCHAR(255),
                DEPARTEMENT VARCHAR(255),
                PAYS VARCHAR(255),
                LATITUDE FLOAT,
                LONGITUDE FLOAT,
                SOURCE VARCHAR(255),
                DATE_EXTRACT DATE

            )
        """)
        self.conn.commit()
        cursor.close()  

    def create_table_ecole(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ecole (
                id SERIAL PRIMARY KEY,
                NOM_ETABLISSEMENT VARCHAR(255),
                TYPE_ETABLISSEMENT VARCHAR(255),
                STATUT VARCHAR(255),
                ADRESSE VARCHAR(255),
                CODE_POSTAL INTEGER,
                VILLE VARCHAR(255),
                DEPARTEMENT VARCHAR(255),
                PAYS VARCHAR(255),
                LATITUDE FLOAT,
                LONGITUDE FLOAT,
                SOURCE VARCHAR(255),
                DATE_EXTRACT DATE
            )
        """)
        self.conn.commit()
        cursor.close()

    def create_table_sport(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sport (
                id SERIAL PRIMARY KEY,
                NOM_ETABLISSEMENT VARCHAR(255),
                ADRESSE VARCHAR(255),
                CODE_POSTAL INTEGER,
                TYPE_EQUIPEMENT VARCHAR(255),
                FAMILLE_EQUIPEMENT VARCHAR(255),
                VILLE VARCHAR(255),
                DEPARTEMENT VARCHAR(255),
                PAYS VARCHAR(255),
                LATITUDE FLOAT,
                LONGITUDE FLOAT,
                SOURCE VARCHAR(255),
                DATE_EXTRACT DATE
            )
        """)
        self.conn.commit()
        cursor.close() 

    def create_table_metro(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metro (
                id SERIAL PRIMARY KEY,
                NOM_STATION VARCHAR(255),
                LIGNE VARCHAR(255),
                TYPE VARCHAR(255),
                OPERATEUR VARCHAR(255),
                LATITUDE FLOAT,
                LONGITUDE FLOAT,
                VILLE VARCHAR(255),
                DEPARTEMENT VARCHAR(255),
                PAYS VARCHAR(255),
                SOURCE VARCHAR(255),
                DATE_EXTRACT DATE
            )
        """)
        cursor.execute("""
            ALTER TABLE metro ADD COLUMN IF NOT EXISTS PAYS VARCHAR(255)
        """)
        self.conn.commit()
        cursor.close()

    def insert_hopital(self, data):
        cursor = self.conn.cursor()
        for _, row in data.iterrows():
            cursor.execute("""
                INSERT INTO hopital (nom_etablissement, type_etablissement, adresse, code_postal, ville, departement, pays, latitude, longitude, source, date_extract)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['nom_etablissement'], row['type_etablissement'], row['adresse'], row['code_postal'],
                row['VILLE'], row['DEPARTEMENT'], row['PAYS'], row['latitude'], row['longitude'], row['source'], row['date_extraction']
            ))
        self.conn.commit()
        cursor.close()

    def insert_ecole(self, data):
        cursor = self.conn.cursor()
        for _, row in data.iterrows():
            cursor.execute("""
                INSERT INTO ecole (nom_etablissement, type_etablissement, statut, adresse, code_postal, ville, departement, pays, latitude, longitude, source, date_extract) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['nom_etablissement'], row['type_etablissement'], row['statut_public_prive'],
                row['adresse_1'], row['code_postal'], row['VILLE'], row['DEPARTEMENT'], row['PAYS'],
                row['latitude'], row['longitude'], row['source'], row['date_extraction']
            ))
        self.conn.commit()
        cursor.close()

    def insert_sport(self, data):
        cursor = self.conn.cursor()
        for _, row in data.iterrows():
            cursor.execute("""
                INSERT INTO sport (nom_etablissement, adresse, code_postal, type_equipement, famille_equipement, ville, departement, pays, latitude, longitude, source, date_extract)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['nom_etablissement'], row['adresse'], row['code_postal'],
                row['type_equipement'], row['famille_equipement'], row['VILLE'], row['DEPARTEMENT'], row['PAYS'],
                row['latitude'], row['longitude'], row['source'], row['date_extraction']
            ))
        self.conn.commit()
        cursor.close()

    def insert_metro(self, data):
        cursor = self.conn.cursor()
        for _, row in data.iterrows():
            cursor.execute("""
                INSERT INTO metro (nom_station, ligne, type, operateur, latitude, longitude, ville, departement, pays, source, date_extract)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['nom_station'], row['ligne'], row['type_transport'], row['operateur'],
                row['latitude'], row['longitude'], row['VILLE'], row['DEPARTEMENT'], row['PAYS'],
                row['source'], row['date_extraction']
            ))
        self.conn.commit()
        cursor.close()


if __name__ == "__main__":
    bdd = Bdd()
    bdd.create_table_hopital()
    bdd.create_table_ecole()
    bdd.create_table_sport()
    bdd.create_table_metro()

    bdd.close_conn()

