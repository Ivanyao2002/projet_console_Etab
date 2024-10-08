from datetime import datetime
from models.personne import Personne
from models.Professeur.ICrudProfesseur import ICRUDProfesseur
from models.Professeur.IEducation import IEducation
from bd_connection import BD

class Professeur(Personne, IEducation, ICRUDProfesseur):
    """
        Classe représentant un professeur, héritant de Personne et implémentant des interfaces éducatives.
    """
    
    # Initialise un nouveau professeur avec ses informations personnelles et ses responsabilités.
    def __init__(self, dateNaissance, ville, prenom, nom, telephone, vacant, matiereEnseigne, prochainCours, sujetProchaineReunion):
        super().__init__(dateNaissance, ville, prenom, nom, telephone)
        self.__vacant = vacant
        self.__matiereEnseigne = matiereEnseigne
        self.__prochainCours = prochainCours
        self.__sujetProchaineReunion = sujetProchaineReunion

    # Retourne une représentation sous forme de chaîne du professeur.
    def __str__(self):
        statut_affiche = "Oui" if self.__vacant else "Non"
        return f"Professeur n° {self.get_id} : {self.get_nom} {self.get_prenom}, née le {self.get_date_naissance} à {self.get_ville}, numéro de téléphone : {self.get_telephone}, vacant: {statut_affiche}, enseigne {self.__matiereEnseigne}"

    @property 
    def get_vacant(self):
        return self.__vacant
    
    @property 
    def get_matiereEnseigne(self):
        return self.__matiereEnseigne

    @property 
    def get_prochainCours(self):
        return self.__prochainCours
    
    @property 
    def get_sujetProchaineReunion(self):
        return self.__sujetProchaineReunion

    def set_sujetProchaineReunion(self, sujetProchaineReunion):
        self.__sujetProchaineReunion = sujetProchaineReunion            

    def set_prochainCours(self, prochainCours):
        self.__prochainCours = prochainCours

    def set_matiereEnseigne(self, matiereEnseigne):
        self.__matiereEnseigne = matiereEnseigne            

    def set_vacant(self, vacant):
        self.__vacant = vacant    
  
    # Retourne un message indiquant la matière enseignée par le professeur.
    def enseigner(self, matiere):
        self.__matiereEnseigne = matiere
        return f"Enseigne la matière {self.__matiereEnseigne}"
    
    # Retourne un message indiquant le sujet du prochain cours à préparer.
    def preparerCours(self, cours):
        self.__prochainCours = cours
        return f"Prépare le contenu d'un cours sur le sujet {self.__prochainCours}"
    
    # Retourne un message indiquant le sujet de la prochaine réunion à laquelle le professeur doit assister.
    def assisterReunion(self, sujet):
        self.__sujetProchaineReunion = sujet
        return f"Doit assister à une reunion sur {self.__sujetProchaineReunion}"

    # Implémentation des méthodes CRUD
    @classmethod
    def ajouter(cls, professeur):
        """Ajoute un professeur à la base de données."""
        connection = BD.create_connection()
        if connection:
            try:
                cursor = connection.cursor()

                date_naissance = datetime.strptime(professeur.get_date_naissance, '%d-%m-%Y').strftime('%Y-%m-%d')

                query_professeur = """
                    INSERT INTO professeurs (date_naissance, ville, prenom, nom, telephone, vacant, matiere_enseigne, prochain_cours, sujet_prochaine_reunion) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_professeur, (
                    date_naissance,
                    professeur.get_ville,
                    professeur.get_prenom,
                    professeur.get_nom,
                    professeur.get_telephone,
                    professeur._Professeur__vacant,
                    professeur._Professeur__matiereEnseigne,
                    professeur._Professeur__prochainCours,
                    professeur._Professeur__sujetProchaineReunion
                ))

                connection.commit()
                print(f"\033[0;92mProfesseur {professeur.get_prenom} {professeur.get_nom} ajouté avec succès.\033[0m")
            except Exception as e:
                print(f"\033[0;91mErreur lors de l'ajout du professeur: {e}\033[0m")
            finally:
                cursor.close()
                connection.close()


    @classmethod
    def modifier(cls, professeur):
        """Modifie un professeur dans la base de données."""
        connection = BD.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query_professeur = """
                    UPDATE professeurs SET date_naissance = %s, ville = %s, prenom = %s, nom = %s, telephone = %s, vacant = %s, matiere_enseigne = %s, prochain_cours = %s, sujet_prochaine_reunion = %s 
                    WHERE id = %s
                """
                try:
                    date_naissance = professeur.get_date_naissance.strftime('%Y-%m-%d')
                except AttributeError:
                    date_naissance = datetime.strptime(professeur.get_date_naissance, '%d-%m-%Y').strftime('%Y-%m-%d')
                
                cursor.execute(query_professeur, (
                    date_naissance,
                    professeur.get_ville,
                    professeur.get_prenom,
                    professeur.get_nom,
                    professeur.get_telephone,
                    professeur.get_vacant,
                    professeur.get_matiereEnseigne,
                    professeur.get_prochainCours,
                    professeur.get_sujetProchaineReunion,                    
                    professeur.get_id,
                ))

                connection.commit()
                print(f"\033[0;92mProfesseur {professeur.get_prenom} {professeur.get_nom} modifié avec succès.\033[0m")
                return True
            except Exception as e:
                print(f"\033[0;91mErreur lors de la modification du professeur: {e}\033[0m")
                return False
            finally:
                cursor.close()
                connection.close()
        return False


    @classmethod
    def supprimer(cls, identifiant):
        """Supprime un professeur de la base de données."""
        connection = BD.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    DELETE FROM professeurs WHERE id = %s
                """
                cursor.execute(query, (identifiant,))
                connection.commit()

                if cursor.rowcount > 0:
                    print(f"\033[0;92mProfesseur avec ID {identifiant} supprimé avec succès.\033[0m")
                    return True
                else:
                    print("\033[0;91mID non trouvé.\033[0m")
                    return False
            except Exception as e:
                print(f"\033[0;91mErreur lors de la suppression du professeur: {e}\033[0m")
                return False
            finally:
                cursor.close()
                connection.close()
        return False


    @classmethod
    def obtenirProfesseur(cls):
        """Obtenir tous les professeurs de la base de données."""
        connection = BD.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT * FROM professeurs"
                cursor.execute(query)
                resultats = cursor.fetchall()

                professeurs = []
                for row in resultats:
                    professeurs.append(row)

                return professeurs
            except Exception as e:
                print(f"\033[0;91mErreur lors de l'obtention des professeurs: {e}\033[0m")
                return []
            finally:
                cursor.close()
                connection.close()
        return []


    @classmethod
    def obtenir(cls, identifiant):
        """Obtenir un professeur par son ID."""
        connection = BD.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query_professeur = """
                        SELECT date_naissance, ville, prenom, nom, telephone, vacant, matiere_enseigne, prochain_cours, sujet_prochaine_reunion 
                        FROM professeurs 
                        WHERE id = %s
                        """
                cursor.execute(query_professeur, (identifiant,))
                resultat = cursor.fetchone()

                if resultat:
                    return cls(*resultat) 
                else:
                    return None
            except Exception as e:
                print(f"\033[0;91mErreur lors de l'obtention du professeur: {e}\033[0m")
                return None
            finally:
                cursor.close()
                connection.close()
        return None