import time
from datetime import datetime
from menus import afficherSousMenuProf, accueil
from models.Professeur.professeur import Professeur

def ajouterProfesseur():
    try:
        nom = input("\033[0;33mNom du professeur : \033[0m")
        prenom = input("\033[0;33mPrénom du professeur : \033[0m")
        
        while True:
            date_naissance = input("\033[0;33mDate de naissance (JJ-MM-AAAA) : \033[0m")
            try:
                datetime.strptime(date_naissance, '%d-%m-%Y')
                break  
            except ValueError:
                print("\033[0;91mDate invalide !! Veuillez entrer une date au format JJ-MM-AAAA.\033[0m")

        while True:
            telephone = input("\033[0;33mEntrez le numéro de téléphone (10 chiffres) :  \033[0m")
            if telephone.isdigit() and len(telephone) == 10:
                break  
            else:
                print("\033[0;91mNuméro invalide !! Veuillez entrer un numéro au format numérique (0708862333).\033[0m")
            continue

        while True:
            vacant_input = input("\033[0;33mStatut vacant Oui(1) / Non(0) : \033[0m").strip().lower()
            if vacant_input in ['oui', '1']:
                vacant = "Oui"
                break
            elif vacant_input in ['non', '0']:
                vacant = "Non"
                break
            else:
                print("\033[0;91mChoix invalide !! Veuillez choisir Oui(1) ou Non(0) \033[0m")
                continue
        
        ville = input("\033[0;33mVille : \033[0m")
        matiereEnseigne = input("\033[0;33mEntrez la matière enseigné : \033[0m")
        prochainCours = input("\033[0;33mEntrez le prochain cours : \033[0m")
        sujetProchaineReunion = input("\033[0;33mEntrez le sujet de la prochaine reunion : \033[0m")
        professeur = Professeur(date_naissance, ville, prenom, nom, telephone, vacant, matiereEnseigne, prochainCours, sujetProchaineReunion)
        Professeur.ajouter(professeur)
    
    except Exception as e:
        print(f"\033[0;91mErreur lors de l'ajout d'un professeur : {e}\033[0m")
        time.sleep(0.5)

def listerProfesseurs():
    """Lister tous les professeurs."""
    professeurs = Professeur.obtenirProfesseur()
    if professeurs:
        print("\033[0;92mListe des professeurs :")
        for prof in professeurs:
            print(prof)
    else:
        print("Aucun professeur enregistré.")

def modifierProfesseur():
    """Modifier un professeur existant."""
    identifiant = input("Entrez l'identifiant du professeur à modifier : ")
    professeur = Professeur.obtenir(identifiant)
    if professeur:
        print(f"Modification du professeur : {professeur}")
        
        # Demande des nouvelles informations
        professeur.date_naissance = input("Nouvelle date de naissance (JJ-MM-AAAA) : ") or professeur.get_date_naissance
        professeur.ville = input("Nouvelle ville : ") or professeur.get_ville
        professeur.prenom = input("Nouveau prénom : ") or professeur.get_prenom
        professeur.nom = input("Nouveau nom : ") or professeur.get_nom
        professeur.telephone = input("Nouveau téléphone : ") or professeur.get_telephone
        professeur.vacant = input("Est-ce vacant ? (oui/non) : ").lower() == 'oui' or professeur.get_vacant
        professeur.matiereEnseigne = input("Nouvelle matière enseignée : ") or professeur.get_matiereEnseigne
        professeur.prochainCours = input("Nouveau sujet du prochain cours : ") or professeur.get_prochainCours
        professeur.sujetProchaineReunion = input("Nouveau sujet de la prochaine réunion : ") or professeur.get_sujetProchaineReunion
        
        Professeur.modifier(professeur)

def supprimerProfesseur():
    """Supprimer un professeur."""
    identifiant = input("\033[0;33mEntrez l'identifiant du professeur à supprimer : \033[0m")
    Professeur.supprimer(identifiant)

def gestionProfesseurs():
    accueil("GESTION DES PROFESSEURS")
    while True:
        afficherSousMenuProf()
        try:
            choix = int(input("\033[0;37mChoisissez une option dans le menu : \033[0m"))
        except ValueError:
            print('\033[0;93mVous devez entrer un chiffre du menu !!\033[0m')
            time.sleep(0.5)
            continue

        match choix:
            case 1:
                ajouterProfesseur()
            case 2:
                supprimerProfesseur()
            case 3:
                modifierProfesseur()
            case 4:
                listerProfesseurs()               
            case 5:
                break             
            case 0:
                return                   
            case _:
                print("\033[0;93mOption invalide, veuillez réessayer !!\033[0m")
                time.sleep(0.5)
                continue