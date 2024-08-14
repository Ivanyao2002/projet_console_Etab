import time
from datetime import datetime
from menus import afficherSousMenuElev, accueil
from models.Eleve.eleve import Eleve

def ajouterEleve():
    try:
        nom = input("\033[0;33mNom de l'élève : \033[0m")
        prenom = input("\033[0;33mPrénom de l'élève : \033[0m")
        
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
        ville = input("\033[0;33mVille : \033[0m")
        classe = input("\033[0;33mEntrez la classe : \033[0m")

        while True:
            matricule = input("\033[0;33mEntrez le matricule : \033[0m")
            try:
                if Eleve.exists(matricule):  
                    print("\033[0;91mMatricule déjà existant !! Veuillez entrer un matricule unique.\033[0m")
                else:
                    break
            except Exception as e:
                print(f"\033[0;91mErreur lors de la vérification du matricule : {e}\033[0m")
            continue

        eleve = Eleve(date_naissance, ville, prenom, nom, telephone, classe, matricule)
        Eleve.ajouter(eleve)
    
    except Exception as e:
        print(f"\033[0;91mErreur lors de l'ajout d'un élève : {e}\033[0m")
        time.sleep(0.5)


def listerEleves():
    eleves = Eleve.obtenirEleve()
    if eleves:
        print("\033[0;92mListe des élèves :")
        for eleve in eleves:
            print(eleve)
    else:
        print("Aucun élève enregistré.")

def modifierEleve():
    matricule = input("Entrez le matricule de l'élève à modifier : ")
    eleve = Eleve.obtenir(matricule)
    if eleve:
        print(f"Modification de l'élève : {eleve}")
        eleve.date_naissance = input("Nouvelle date de naissance (JJ-MM-AAAA) : ") or eleve.get_date_naissance
        eleve.ville = input("Nouvelle ville : ") or eleve.get_ville
        eleve.prenom = input("Nouveau prénom : ") or eleve.get_prenom
        eleve.nom = input("Nouveau nom : ") or eleve.get_nom
        eleve.telephone = input("Nouveau téléphone : ") or eleve.get_telephone
        eleve.classe = input("Nouvelle classe : ") or eleve.get_classe
        
        Eleve.modifier(eleve)


def supprimerEleve():
    matricule = input("\033[0;33mEntrez le matricule de l'élève à supprimer : \033[0m")
    Eleve.supprimer(matricule)

def gestionEleves():
    accueil("GESTION DES ÉLÈVES")
    while True:
        afficherSousMenuElev()
        try:
            choix = int(input("\033[0;37mChoisissez une option dans le menu : \033[0m"))
        except ValueError:
            print('\033[0;93mVous devez entrer un chiffre du menu !!\033[0m')
            time.sleep(0.5)
            continue

        match choix:
            case 1:
                ajouterEleve()
            case 2:
                supprimerEleve()
            case 3:
                modifierEleve()
            case 4:
                listerEleves()               
            case 5:
                break             
            case 0:
                return                   
            case _:
                print("\033[0;93mOption invalide, veuillez réessayer !!\033[0m")
                time.sleep(0.5)
                continue