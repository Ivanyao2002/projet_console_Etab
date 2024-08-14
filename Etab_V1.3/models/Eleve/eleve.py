from datetime import datetime
from models.personne import Personne
from models.Eleve.ICrudEleve import ICRUDEleve
import bd_connection

class Eleve(Personne, ICRUDEleve):
    """
        Classe représentant un élève, héritant de la classe Personne et de la classe ICRUDEleve.
    """
    __eleves = []

    # Initialise un nouvel élève avec ses informations personnelles
    def __init__(self, dateNaissance, ville, prenom, nom, telephone, classe, matricule):
        super().__init__(dateNaissance, ville, prenom, nom, telephone)
        self.__classe = classe
        self.__matricule = matricule

    # Retourne une représentation sous forme de chaîne de l'élève
    def __str__(self):
        return f"Eleve n° {self.get_id} : {self.get_nom} {self.get_prenom}, née le {self.get_date_naissance} à {self.get_ville}, classe: {self.__classe}, matricule: {self.__matricule}, téléphone: {self.get_telephone}"

    # Retourne le matricule de l'élève.
    @property 
    def get_matricule(self):
        return self.__matricule
    
    @property 
    def get_classe(self):
        return self.__classe

    def set_classe(self, classe):
        self.__classe = classe            

    def set_matricule(self, matricule):
        self.__matricule = matricule

    # Implémentation des méthodes CRUD
    # Ajouter un élève
    @classmethod
    def ajouter(cls, eleve):
        """Ajoute un élève à la base de données."""
        connection = bd_connection.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query_personne = """
                    INSERT INTO personnes (date_naissance, ville, prenom, nom, telephone) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                date_naissance = datetime.strptime(eleve.get_date_naissance, '%d-%m-%Y').strftime('%Y-%m-%d')
                cursor.execute(query_personne, (
                    date_naissance,
                    eleve.get_ville,
                    eleve.get_prenom,
                    eleve.get_nom,
                    eleve.get_telephone
                ))
                id_personne = cursor.lastrowid

                query_eleve = """
                    INSERT INTO eleves (id_personne, classe, matricule) 
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query_eleve, (
                    id_personne,
                    eleve._Eleve__classe,  
                    eleve._Eleve__matricule  
                ))

                connection.commit()
                print(f"\033[0;92mÉlève {eleve.get_prenom} {eleve.get_nom} ajouté avec succès.\033[0m")
            except Exception as e:
                print(f"\033[0;91mErreur lors de l'ajout de l'élève: {e}\033[0m")
            finally:
                cursor.close()
                connection.close()

    # Modifie un élèvé
    def modifier(cls, eleve):
        """Modifie un élève dans la base de données."""
        connection = bd_connection.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    UPDATE personnes SET date_naissance = %s, ville = %s, prenom = %s, nom = %s, telephone = %s 
                    WHERE id = (SELECT id_personne FROM eleves WHERE matricule = %s)
                """
                date_naissance = datetime.strptime(eleve.get_date_naissance, '%d-%m-%Y').strftime('%Y-%m-%d')
                cursor.execute(query, (
                    date_naissance,
                    eleve.get_ville,
                    eleve.get_prenom,
                    eleve.get_nom,
                    eleve.get_telephone,
                    eleve._Eleve__matricule
                ))

                query_eleve = """
                    UPDATE eleves SET classe = %s 
                    WHERE matricule = %s
                """
                cursor.execute(query_eleve, (
                    eleve._Eleve__classe,
                    eleve._Eleve__matricule
                ))

                connection.commit()
                print(f"\033[0;92mÉlève {eleve.get_prenom} {eleve.get_nom} modifié avec succès.\033[0m")
                return True
            except Exception as e:
                print(f"\033[0;91mErreur lors de la modification de l'élève: {e}\033[0m")
                return False
            finally:
                cursor.close()
                connection.close()
        return False

    # Obtenir les élèves
    @classmethod
    def obtenirEleve(cls):
        """Obtenir tous les élèves de la base de données."""
        connection = bd_connection.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT * FROM eleves"
                cursor.execute(query)
                resultats = cursor.fetchall()

                eleves = []
                for row in resultats:
                    eleves.append(row)  

                return eleves
            except Exception as e:
                print(f"\033[0;91mErreur lors de l'obtention des élèves: {e}\033[0m")
                return []
            finally:
                cursor.close()
                connection.close()
        return []

    # Supprimer un élève 
    @classmethod
    def supprimer(cls, identifiant):
        """Supprime un élève de la base de données."""
        connection = bd_connection.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    DELETE FROM eleves WHERE matricule = %s
                """
                cursor.execute(query, (identifiant,))
                connection.commit()

                if cursor.rowcount > 0:
                    print(f"\033[0;92mÉlève avec matricule {identifiant} supprimé avec succès.\033[0m")
                    return True
                else:
                    print("\033[0;91mMatricule non trouvé.\033[0m")
                    return False
            except Exception as e:
                print(f"\033[0;91mErreur lors de la suppression de l'élève: {e}\033[0m")
                return False
            finally:
                cursor.close()
                connection.close()
        return False    

    # Obtenir un élève par son matricule
    @classmethod
    def obtenir(cls, identifiant):
        """Obtenir un élève par son matricule."""
        connection = bd_connection.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT * FROM eleves WHERE matricule = %s"
                cursor.execute(query, (identifiant,))
                resultat = cursor.fetchone()

                if resultat:
                    return resultat  
                else:
                    print("\033[0;91mMatricule non trouvé.\033[0m")
                    return None
            except Exception as e:
                print(f"\033[0;91mErreur lors de l'obtention de l'élève: {e}\033[0m")
                return None
            finally:
                cursor.close()
                connection.close()
        return None
    
    # Vérifie si le matricule existe
    @classmethod
    def exists(cls, matricule):
        """Vérifie si un matricule existe déjà dans la base de données."""
        connection = bd_connection.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT COUNT(*) FROM eleves WHERE matricule = %s"
                cursor.execute(query, (matricule,))
                count = cursor.fetchone()[0]
                return count > 0
            except Exception as e:
                print(f"\033[0;91mErreur lors de la vérification du matricule: {e}\033[0m")
                return False
            finally:
                cursor.close()
                connection.close()
        return False