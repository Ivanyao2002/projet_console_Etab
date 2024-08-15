import time
from datetime import datetime
from menus import Menu
from models.Eleve.eleve import Eleve

class ServicesEleve:
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
                id_eleve = eleve[0]
                date_naissance = eleve[1].strftime('%d-%m-%Y')
                ville = eleve[2]
                prenom = eleve[3]
                nom = eleve[4]
                telephone = eleve[5]
                classe = eleve[6]
                matricule = eleve[7]
                print(f"ID: {id_eleve}, Nom: {nom}, Prénom: {prenom}, Date de naissance: {date_naissance}, Ville: {ville}, Téléphone: {telephone}, Classe: {classe}, Matricule: {matricule}")
        else:
            print("Aucun élève enregistré.")

    def modifierEleve():
        while True:
            try:
                matricule = input("\033[0;33mEntrez le matricule de l'élève à modifier : \033[0m")
                eleve = Eleve.obtenir(matricule)
                
                if eleve is None:
                    print("\033[0;91mAucun élève trouvé avec ce matricule. Veuillez réessayer.\033[0m")
                    continue 
                
                if eleve:
                    print(f"Modification de l'élève : \033[0;32m\n-> {eleve}\033[0m")
                    while True:
                        date_naissance = input("\033[0;33mNouvelle date de naissance (JJ-MM-AAAA) (Appuyez sur entrée pour garder l'ancienne valeur): \033[0m")
                        if not date_naissance:  
                            date_naissance = eleve.get_date_naissance
                            break
                        try:
                            datetime.strptime(date_naissance, '%d-%m-%Y')
                            break
                        except ValueError:
                            print("\033[0;91mDate invalide !! Veuillez entrer une date au format JJ-MM-AAAA.\033[0m")
                    ville = input("\033[0;33mNouvelle ville (Appuyez sur entrée pour garder l'ancienne valeur): \033[0m") or eleve.get_ville
                    prenom = input("\033[0;33mNouveau prénom (Appuyez sur entrée pour garder l'ancienne valeur): \033[0m") or eleve.get_prenom
                    nom = input("\033[0;33mNouveau nom (Appuyez sur entrée pour garder l'ancienne valeur): \033[0m") or eleve.get_nom
                    
                    while True:
                        telephone = input("\033[0;33mNouveau téléphone (Appuyez sur entrée pour garder l'ancienne valeur): \033[0m")
                        if not telephone:  
                            telephone = eleve.get_telephone
                            break
                        if telephone.isdigit() and len(telephone) == 10:
                            break  
                        else:
                            print("\033[0;91mNuméro invalide !! Veuillez entrer un numéro au format numérique (10 chiffres).\033[0m")
                    
                    classe = input("\033[0;33mNouvelle classe (Appuyez sur entrée pour garder l'ancienne valeur): \033[0m") or eleve.get_classe
                    if date_naissance:
                        eleve.set_date_naissance(date_naissance)
                    if ville:
                        eleve.set_ville(ville)
                    if prenom:
                        eleve.set_prenom(prenom)
                    if nom:
                        eleve.set_nom(nom)
                    if telephone:
                        eleve.set_telephone(telephone)
                    if classe:
                        eleve.set_classe(classe)
                    Eleve.modifier(eleve)
                return  
            except Exception as e:
                print(f"\033[0;91mErreur lors de la modification de l'élève : {e}\033[0m")
                time.sleep(0.5) 


    def supprimerEleve():
        matricule = input("\033[0;33mEntrez le matricule de l'élève à supprimer : \033[0m")
        Eleve.supprimer(matricule)

    def gestionEleves():
        Menu.accueil("GESTION DES ÉLÈVES")
        while True:
            Menu.afficherSousMenuElev()
            try:
                choix = int(input("\033[0;37mChoisissez une option dans le menu : \033[0m"))
            except ValueError:
                print('\033[0;93mVous devez entrer un chiffre du menu !!\033[0m')
                time.sleep(0.5)
                continue

            match choix:
                case 1:
                    ServicesEleve.ajouterEleve()
                case 2:
                    ServicesEleve.supprimerEleve()
                case 3:
                    ServicesEleve.modifierEleve()
                case 4:
                    ServicesEleve.listerEleves()               
                case 5:
                    break             
                case 0:
                    return                   
                case _:
                    print("\033[0;93mOption invalide, veuillez réessayer !!\033[0m")
                    time.sleep(0.5)
                    continue