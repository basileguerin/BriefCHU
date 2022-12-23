import random
import datetime
import names
from resident import Patient, RH
from config import get_db_config

def fill_with_fake(nombre_residents):
    """Remplit les tables patients et RH avec des résidents générés aléatoirement"""
    
    CONFIG = get_db_config()

    for i in range(nombre_residents):
        print(f"{i}/{nombre_residents}")
        categorie = random.randint(0,1) #Si 0 -> Patient sinon RH

        if categorie == 0:
            groupes = ['A', 'B', 'AB', 'O'] #Liste des groupes sanguins
            nom_p = names.get_last_name().upper()
            prenom_p = names.get_first_name()
            groupe = random.choice(groupes) #Random groupe
            date_entree = str(datetime.date.today())
            new_patient = Patient(nom_p, prenom_p, groupe, date_entree) #Nouvelle instance patient
            new_patient.entrer_a_l_hopital(CONFIG) #Ajout à la BDD
        
        if categorie == 1:
            nom_rh = names.get_last_name().upper()
            prenom_rh = names.get_first_name()
            salaire = random.randint(1000,100000) #Random salaire
            date_recrutement = str(datetime.date.today())
            new_rh = RH(nom_rh, prenom_rh, salaire, date_recrutement) #Nouvelle instance RH
            new_rh.debuter_CDD_CDI(CONFIG) #Ajout à la BDD

