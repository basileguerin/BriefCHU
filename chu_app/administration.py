import mysql.connector as mysqlpy
import pandas as pd

class Archive():
    """Definition de la classe Archive"""
    def __init__(self, nom: str, prenom: str, date_entree: str, date_sortie: str) -> None:
        self.nom = nom
        self.prenom = prenom
        self.date_entree = date_entree
        self.date_sortie = date_sortie

    def enregister_en_base(self, config, id_resident) -> None:
        """Enregistre l'archive dans la BDD"""

        bdd = mysqlpy.connect(**config)
        cursor = bdd.cursor()
        query = f"""INSERT IGNORE INTO archives(id_resident, date_entree, date_sortie)
        VALUES ('{id_resident}', '{self.date_entree}', '{self.date_sortie}');"""
        cursor.execute(query)
        bdd.commit()
        cursor.close()
        bdd.close()

    @staticmethod
    def afficher_les_archives_console(config) -> None:
        """Affiche le contenu de la table archives dans la console"""

        bdd = mysqlpy.connect(**config)
        cursor = bdd.cursor()
        query = """SELECT * FROM archives"""
        cursor.execute(query)
        for archive in cursor:
            print(archive)
        cursor.close()
        bdd.close()

    @staticmethod
    def afficher_les_archives_streamlit(config) -> pd.DataFrame:
        """Renvoie un dataframe contenant les infos de la table archives"""

        bdd = mysqlpy.connect(**config)
        cursor = bdd.cursor()
        infos= []
        query = """SELECT * FROM archives"""
        cursor.execute(query)
        for row in cursor:
            infos.append(row)
        cursor.close()
        bdd.close()
        return pd.DataFrame(data=infos, columns=['id_resident', 'date_entree', 'date_sortie'])

