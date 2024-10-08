import time
import bcrypt
from menus import Menu
from services.gestion_utilisateurs import ServicesUtilisateur as gestion_utilisateurs
from services.gestion_professeurs import ServicesProfesseur as gestion_professeurs
from services.gestion_eleves import ServicesEleve as gestion_eleves
from bd_connection import BD 


class Main:
    def main(self) -> None:
        debut = time.time() 

        Menu.accueil("BIENVENUE DANS L'APPLICATION ETAB v1.3")
        while True:
            identifiant = input("\033[0;37mEntrez votre identifiant : \033[0m")
            mot_de_passe = input("\033[0;37mEntrez votre mot de passe : \033[0m")
            
            utilisateur_data = gestion_utilisateurs.recuperer_utilisateur(BD, identifiant)
            
            if utilisateur_data and bcrypt.checkpw(mot_de_passe.encode('utf-8'), utilisateur_data[1].encode('utf-8')):  # Vérifiez le mot de passe
                print("\033[0;92mAuthentification réussie !!\033[0m")
                time.sleep(0.6)
                Menu.accueil("BIENVENUE DANS L'APPLICATION ETAB v1.3")
                while True:
                    Menu.afficher_menu()
                    try:
                        choix = int(input("\033[0;37mChoisissez une option dans le menu : \033[0m"))
                    except ValueError:
                        print('\033[0;93mVous devez entrer un chiffre du menu !!\033[0m')
                        time.sleep(0.5)
                        continue

                    match choix:
                        case 1:
                            time.sleep(0.4)
                            gestion_eleves.gestionEleves()
                        case 2:
                            time.sleep(0.4)
                            gestion_professeurs.gestionProfesseurs()
                        case 3:
                            gestion_utilisateurs.gestionUtilisateurs()
                        case 0:
                            Menu.quitter(debut)     
                            break               
                        case _:
                            print("\033[0;93mOption invalide, veuillez réessayer !!\033[0m")
                            time.sleep(0.5)
                            continue
            else:
                print("\033[0;91mÉchec de l'authentification, veuillez vérifier les informations saisies !\033[0m")
                time.sleep(0.4)
                continue
            break 

if __name__ == "__main__":
    
    app = Main()
    app.main()