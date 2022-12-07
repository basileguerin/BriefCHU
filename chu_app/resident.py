import mysql.connector as mysqlpy
import datetime
from administration import Archive
from config import get_db_config
import pandas as pd

CONFIG = get_db_config()

class Patient:
    """Definition de la classe Patient"""
    is_in_hospital = False

    def __init__(self, nom: str, prenom: str, groupe_sanguin: str, date_entree: str) -> None:
        """Constructeur"""
        self.nom = nom
        self.prenom = prenom
        self.groupe_sanguin = groupe_sanguin
        self.date_entree = date_entree
        self.id_patient = nom + prenom + groupe_sanguin + date_entree

    def entrer_a_l_hopital(self, config):
        """Stocke le patient dans la BDD et ajoute une archive"""

        bdd = mysqlpy.connect(**config)
        cursor = bdd.cursor()
        self.is_in_hospital = True
        archive = Archive(self.nom, self.prenom, self.date_entree, '')
        archive.enregister_en_base(CONFIG, self.id_patient)
        query = f"""INSERT IGNORE INTO patients(id, nom, prenom, groupe_sanguin, is_in_hospital)
        VALUES ('{self.id_patient}', '{self.nom}', '{self.prenom}', '{self.groupe_sanguin}', 1);"""
        cursor.execute(query)
        bdd.commit()
        cursor.close()
  
    def sortir_de_l_hopital(self, config):
        """Supprime le patient de la BDD et ajoute une date de sortie à l'archive"""

        bdd = mysqlpy.connect(**config)
        cursor = bdd.cursor()
        self.is_in_hospital = False
        date_sortie = str(datetime.date.today())
        query = f"""UPDATE archives SET date_sortie = '{date_sortie}'
        WHERE id_resident = '{self.id_patient}'"""
        cursor.execute(query)
        query = f"""DELETE FROM patients WHERE id = '{self.id_patient}'"""
        cursor.execute(query)
        bdd.commit()
        cursor.close()

    @staticmethod
    def affiche_patients(config):
        """Renvoie un dataframe contenant les infos de la table patients"""

        bdd = mysqlpy.connect(**config)
        cursor = bdd.cursor()
        infos= []
        query = """SELECT * FROM patients"""
        cursor.execute(query)
        for row in cursor:
            infos.append(row)
        cursor.close()
        bdd.close()
        return pd.DataFrame(data=infos, columns=['id', 'nom', 'prenom', 'groupe_sanguin', 'is_in_hospital'])
            

class RH:
    """Definition de la classe RH"""
    working_at_hospital = False

    def __init__(self, nom: str, prenom: str, salaire: float, date_recrutement: str) -> None:
        """Constructeur"""
        self.nom = nom
        self.prenom = prenom
        self.salaire = salaire
        self.date_recrutement = date_recrutement
        self.id_rh = nom + prenom + date_recrutement
    
    def debuter_CDD_CDI(self, config):
        """Stocke le RH dans la BDD et ajoute une archive"""

        bdd = mysqlpy.connect(**config)
        cursor = bdd.cursor()
        self.working_at_hospital = True
        archive = Archive(self.nom, self.prenom, self.date_recrutement, '')
        archive.enregister_en_base(CONFIG, self.id_rh)
        query = f"""INSERT IGNORE INTO rh(id, nom, prenom, salaire, working_at_hospital)
        VALUES ('{self.id_rh}', '{self.nom}', '{self.prenom}', {self.salaire}, 1)"""
        cursor.execute(query)
        bdd.commit()
        cursor.close()

    def quitter_CDD_CDI(self, config):
        """Supprime le RH de la table rh et ajoute une date de sortie à l'archive"""

        bdd = mysqlpy.connect(**config)
        cursor = bdd.cursor()
        self.working_at_hospital = False
        date_fin_contrat = str(datetime.date.today())
        query = f"""UPDATE archives SET date_sortie = '{date_fin_contrat}'
        WHERE id_resident = '{self.id_rh}'"""
        cursor.execute(query)
        query = f"""DELETE FROM rh WHERE id = '{self.id_rh}'"""
        cursor.execute(query)
        bdd.commit()
        cursor.close()
    
    @staticmethod
    def affiche_rh(config):
        """Renvoie un dataframe contenant les infos de la table rh"""

        bdd = mysqlpy.connect(**config)
        cursor = bdd.cursor()
        infos= []
        query = """SELECT * FROM rh"""
        cursor.execute(query)
        for row in cursor:
            infos.append(row)
        cursor.close()
        bdd.close()
        return pd.DataFrame(data=infos, columns=['id', 'nom', 'prenom', 'salaire', 'working_at_hospital'])

