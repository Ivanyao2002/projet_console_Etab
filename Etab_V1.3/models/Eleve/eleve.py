from datetime import datetime
from models.personne import Personne
from models.Eleve.ICrudEleve import ICRUDEleve
from bd_connection import BD

class Eleve(Personne, ICRUDEleve):
    """
        Classe représentant un élève, héritant de la classe Personne et de la classe ICRUDEleve.
    """

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
        connection = BD.create_connection()
        if connection:
            try:
                cursor = connection.cursor()

                date_naissance = datetime.strptime(eleve.get_date_naissance, '%d-%m-%Y').strftime('%Y-%m-%d')

                query_eleve = """
                    INSERT INTO eleves (date_naissance, ville, prenom, nom, telephone, classe, matricule) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_eleve, (
                    date_naissance,
                    eleve.get_ville,
                    eleve.get_prenom,
                    eleve.get_nom,
                    eleve.get_telephone,
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
    @classmethod
    def modifier(cls, eleve):
        """Modifie un élève dans la base de données."""
        connection = BD.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query_eleve = """
                    UPDATE eleves SET date_naissance = %s, ville = %s, prenom = %s, nom = %s, telephone = %s,
                    classe = %s 
                    WHERE matricule = %s
                """
                try:
                    date_naissance = eleve.get_date_naissance.strftime('%Y-%m-%d')
                except AttributeError:
                    date_naissance = datetime.strptime(eleve.get_date_naissance, '%d-%m-%Y').strftime('%Y-%m-%d')

                cursor.execute(query_eleve, (
                    date_naissance,
                    eleve.get_ville,
                    eleve.get_prenom,
                    eleve.get_nom,
                    eleve.get_telephone,
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
        connection = BD.create_connection()
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
        connection = BD.create_connection()
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
        connection = BD.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query_eleve = """
                    SELECT date_naissance, ville, prenom, nom, telephone, classe, matricule
                    FROM eleves 
                    WHERE matricule = %s
                """
                
                cursor.execute(query_eleve, (identifiant,))
                resultat = cursor.fetchone()

                if resultat:
                    return cls(*resultat)  
                else:
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
        connection = BD.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query_eleve = "SELECT COUNT(*) FROM eleves WHERE matricule = %s"
                cursor.execute(query_eleve, (matricule,))
                count = cursor.fetchone()[0]
                return count > 0
            except Exception as e:
                print(f"\033[0;91mErreur lors de la vérification du matricule: {e}\033[0m")
                return False
            finally:
                cursor.close()
                connection.close()
        return False