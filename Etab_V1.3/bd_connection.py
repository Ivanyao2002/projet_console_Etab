import mysql.connector
import bcrypt
from mysql.connector import Error
import time


def create_connection():
    """Crée une connexion à la base de données."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='etab_db'
        )
        return connection
    except Error as e:
        print(f"Erreur de connexion: {e}")
        return None

def create_database_and_tables(curseur):
    """Crée la base de données et les tables nécessaires."""
    curseur.execute("CREATE DATABASE IF NOT EXISTS etab_db;")
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
        CREATE TABLE IF NOT EXISTS personnes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date_naissance DATE NOT NULL,
            ville VARCHAR(100) NOT NULL,
            prenom VARCHAR(50) NOT NULL,
            nom VARCHAR(50) NOT NULL,
            telephone VARCHAR(15) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS eleves (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_personne INT,
            classe VARCHAR(50),
            matricule VARCHAR(50) UNIQUE,
            FOREIGN KEY (id_personne) REFERENCES personnes(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS professeurs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_personne INT,
            vacant BOOLEAN,
            matiere_enseigne VARCHAR(100),
            prochain_cours VARCHAR(100),
            sujet_prochaine_reunion VARCHAR(100),
            FOREIGN KEY (id_personne) REFERENCES personnes(id)
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
    connection = create_connection() # Connection à la BD
    if connection.is_connected():
        print("\033[0;92mCONNECTION REUSSIE A LA BASE DE DONNEE\033[0m")
    else:
        print("\033[0;91m ECHEC DE CONNECTION A LA BASE DE DONNEE\033[0m")

    if connection: # Si la connection reussie
        try:
            curseur = connection.cursor() 
            create_database_and_tables(curseur)
            time.sleep(1)
            print("\033[0;92m\nGENERATION DES TABLES DANS LA BD\033[0m")
            default_values_admin(curseur) # admin par defaut 
            time.sleep(1)
            print("\033[0;92m\nAJOUT DE L'ADMIN PAR DEFAUT\033[0m")
            connection.commit() # Validation des changements et mise à jour dans la BD
        except Error as e:
            print(f"Erreur!! {e}")
            connection.rollback() # Si il y'a une erreur dans les requetes revenir au dernier enregistrement
        finally:
            if connection.is_connected():
                curseur.close() # Fermeture de du curseur de requette
                connection.close() # Fermeture de la connexion

if __name__ == "__main__":
    main()