import mysql.connector
import bcrypt
from mysql.connector import Error
import time

class BD: 
    def create_connection():
        """Crée une connexion à la base de données."""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
            )
            curseur = connection.cursor()
            curseur.execute("CREATE DATABASE IF NOT EXISTS etab_db;")
            curseur.close()
            connection.database = 'etab_db'
            return connection
        except Error as e:
            print(f"\033[0;31mErreur de connexion: {e}\033[0m")
            return None

    def create_tables(curseur):
        """Crée les tables nécessaires."""
        curseur.execute("USE etab_db;")

        tables = [
            """
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                pseudo VARCHAR(50) NOT NULL UNIQUE,
                mot_de_passe VARCHAR(255) NOT NULL,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS eleves (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date_naissance DATE NOT NULL,
                ville VARCHAR(40) NOT NULL,
                prenom VARCHAR(100) NOT NULL,
                nom VARCHAR(30) NOT NULL,
                telephone VARCHAR(15) NOT NULL,
                classe VARCHAR(30),
                matricule VARCHAR(30) UNIQUE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS professeurs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date_naissance DATE NOT NULL,
                ville VARCHAR(100) NOT NULL,
                prenom VARCHAR(100) NOT NULL,
                nom VARCHAR(30) NOT NULL,
                telephone VARCHAR(15) NOT NULL,
                vacant BOOLEAN,
                matiere_enseigne VARCHAR(50),
                prochain_cours VARCHAR(50),
                sujet_prochaine_reunion VARCHAR(200)
            );
            """
        ]

        for table in tables:
            curseur.execute(table)

    def default_values_admin(curseur):
        """Vérifie et ajoute l'utilisateur administrateur si nécessaire."""
        pseudo_admin = 'admin'
        mot_de_passe_admin = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())

        curseur.execute("SELECT * FROM utilisateurs WHERE pseudo = %s", (pseudo_admin,))
        if curseur.fetchone() is None:
            curseur.execute("INSERT INTO utilisateurs (pseudo, mot_de_passe) VALUES (%s, %s);", (pseudo_admin, mot_de_passe_admin))

    def main():
        connection = BD.create_connection() # Connection à la BD
        if connection.is_connected():
            print("\033[0;92mCONNECTION REUSSIE A LA BASE DE DONNEE\033[0m")
        else:
            print("\033[0;91m ECHEC DE CONNECTION A LA BASE DE DONNEE\033[0m")

        if connection: # Si la connection reussie
            try:
                curseur = connection.cursor() 
                BD.create_tables(curseur)
                time.sleep(1)
                print("\033[0;92m\nGENERATION DES TABLES DANS LA BD\033[0m")
                BD.default_values_admin(curseur) # admin par defaut 
                time.sleep(1)
                print("\033[0;92m\nAJOUT DE L'ADMIN PAR DEFAUT\033[0m")
                connection.commit() # Validation des changements et mise à jour dans la BD
            except Error as e:
                print(f"\033[0;31mErreur!! {e}\033[0m")
                connection.rollback() # Si il y'a une erreur dans les requetes revenir au dernier enregistrement
            finally:
                if connection.is_connected():
                    curseur.close() # Fermeture de du curseur de requette
                    connection.close() # Fermeture de la connexion

if __name__ == "__main__":
    BD.main()