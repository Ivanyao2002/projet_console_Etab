from datetime import datetime
import bd_connection

class Utilisateur:
    """
        Classe représentant un utilisateur avec un pseudo et un mot de passe.
    """
    __idUnique =  0

    # Initialisation d'un nouvel utilisateur 
    def __init__(self, pseudo, motDePasse, dateCreation):
        Utilisateur.__idUnique += 1
        self.__id =  Utilisateur.__idUnique 
        self.__pseudo = pseudo 
        self.__motDePasse = motDePasse      
        self.__dateCreation = dateCreation
    
    # Retourne une représentation sous forme de chaîne de l'utilisateur. 
    def __str__(self):
        return f"\033[0;92mUtilisateur n0 {self.__id} : {self.__pseudo} crée le {self.__dateCreation}\033[0m"
    
    # Retourne l'identifiant unique de l'utilisateur
    @property
    def id(self):
        return self.__id

    # Retourne le pseudo de l'utilisateur
    @property
    def pseudo(self):
        return self.__pseudo  
    
    # Retourne la date de création du compte de l'utilisateur
    @property
    def dateCreation(self):
        return self.__dateCreation

    def nouveauMotDePasse(self, nouveauMotDePasse):
        self.__motDePasse = nouveauMotDePasse

    # Vérifie si les identifiants fournis correspondent à ceux de l'utilisateur.      
    def authentification(self, identifiant, motDePasse):
        if self.__pseudo == identifiant and self.__motDePasse == motDePasse :
            return True
        return False

    @classmethod
    def ajouterCompte(cls, pseudo, motDePasse):
        """Ajoute un nouvel utilisateur à la base de données."""
        dateCreation = datetime.now()
        nouvel_utilisateur = cls(pseudo, motDePasse, dateCreation)
        
        connection = bd_connection.create_connection()
        if connection and connection.is_connected():
            try:
                curseur = connection.cursor()
                query = "INSERT INTO utilisateurs (pseudo, mot_de_passe, date_creation) VALUES (%s, %s, NOW())"
                curseur.execute(query, (pseudo, motDePasse))
                connection.commit()
                nouvel_utilisateur.__id = curseur.lastrowid  
                return f"\033[0;92mCompte créé avec succès !!\n-->Pseudo : {pseudo}\033[0m"
            except Exception as e:
                print(f"\033[0;91mErreur lors de la création du compte: {e}\033[0m")
            finally:
                curseur.close()
                connection.close()
        return f"\033[0;91mÉchec de la connexion à la base de données.\033[0m"

    def modifierMotDePasse(self, nouveauMotDePasse):
        """Modifie le mot de passe de l'utilisateur dans la base de données."""
        self.__motDePasse = nouveauMotDePasse
        connection = bd_connection.create_connection()
        if connection and connection.is_connected():
            try:
                curseur = connection.cursor()
                query = "UPDATE utilisateurs SET mot_de_passe = %s WHERE pseudo = %s"
                curseur.execute(query, (self.__pseudo, nouveauMotDePasse))
                connection.commit()
                print(f"\033[0;92mMot de passe modifié pour l'utilisateur {self.__pseudo}.\033[0m")
            except Exception as e:
                print(f"\033[0;91mErreur lors de la modification du mot de passe: {e}\033[0m")
            finally:
                curseur.close()
                connection.close()

    @classmethod
    def supprimerCompte(cls, pseudo):
        """Supprime un utilisateur de la base de données."""
        connection = bd_connection.create_connection()
        if connection and connection.is_connected():
            try:
                curseur = connection.cursor()
                query = "DELETE FROM utilisateurs WHERE pseudo = %s"
                curseur.execute(query, (pseudo,))
                connection.commit()
                print(f"\033[0;92mUtilisateur {pseudo} supprimé.\033[0m")
            except Exception as e:
                print(f"\033[0;91mErreur lors de la suppression de l'utilisateur: {e}\033[0m")
            finally:
                curseur.close()
                connection.close()

    @classmethod
    def listerUtilisateurs(cls):
        """Liste tous les utilisateurs de la base de données."""
        connection = bd_connection.create_connection()
        utilisateurs = []
        if connection and connection.is_connected():
            try:
                curseur = connection.cursor()
                query = "SELECT id, pseudo, date_creation FROM utilisateurs"
                curseur.execute(query)
                for user in curseur.fetchall():
                    print(f"\033[0;92mID: {user[0]}, Pseudo: {user[1]}, Date de création: {user[2]}\033[0m")
                return utilisateurs
            except Exception as e:
                print(f"\033[0;91mErreur lors de la récupération des utilisateurs: {e}\033[0m")
            finally:
                curseur.close()
                connection.close()
        return utilisateurs

    @classmethod
    def recuperer_utilisateur(cls, pseudo):
        connection = bd_connection.create_connection()
        if connection:
            curseur = connection.cursor()
            query = "SELECT id, pseudo, date_creation FROM utilisateurs WHERE pseudo = %s"
            curseur.execute(query, (pseudo,))
            result = curseur.fetchone()
            connection.close()
            if result:
                return cls(result[0], result[1], result[2]) 
        return None