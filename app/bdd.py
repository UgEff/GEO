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
        
    def get_conn(self):
        return self.conn
    
    def close_conn(self):
        self.conn.close()
        
    def create_table_hopital(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hopital (
                id SERIAL PRIMARY KEY,
                nom_hopital VARCHAR(255),
                adresse_hopital VARCHAR(255),
                ville_hopital VARCHAR(255),
                latitude_hopital VARCHAR(255),
                longitude_hopital VARCHAR(255)
            )
        """)
        self.conn.commit()
        cursor.close()  

    def create_table_ecole(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ecole (
                id SERIAL PRIMARY KEY,
                nom_ecole VARCHAR(255),
                adresse_ecole VARCHAR(255),
                ville_ecole VARCHAR(255),
                latitude_ecole VARCHAR(255),
                longitude_ecole VARCHAR(255)
            )
        """)
        self.conn.commit()
        cursor.close()


    def create_table_sport(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sport (
                id SERIAL PRIMARY KEY,
                nom_sport VARCHAR(255),
                adresse_sport VARCHAR(255),
                ville_sport VARCHAR(255),
                latitude_sport VARCHAR(255),
                longitude_sport VARCHAR(255)
            )
        """)
        self.conn.commit()
        cursor.close() 

    def create_table_metro(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metro (
                id SERIAL PRIMARY KEY,
                nom_metro VARCHAR(255),
                adresse_metro VARCHAR(255),
                ville_metro VARCHAR(255),
                latitude_metro VARCHAR(255),
                longitude_metro VARCHAR(255)
            )
        """)
        self.conn.commit()
        cursor.close()

    def controle_if_data_different(self, data):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM hopital WHERE nom_hopital = %s AND adresse_hopital = %s AND ville_hopital = %s AND latitude_hopital = %s AND longitude_hopital = %s
        """, (data['nom_hopital'], data['adresse_hopital'], data['ville_hopital'], data['latitude_hopital'], data['longitude_hopital']))
        return cursor.fetchone()
    

