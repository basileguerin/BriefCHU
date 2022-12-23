from resident import Patient, RH
from administration import Archive
from fake_resident import fill_with_fake
from config import get_db_config
import streamlit as st

CONFIG = get_db_config()

df_patient = Patient.affiche_patients(CONFIG)
df_rh = RH.affiche_rh(CONFIG)
df_archive = Archive.afficher_les_archives_streamlit(CONFIG)

st.set_page_config(layout='wide', page_title='CHU_APP', page_icon=':hospital')
st.title('App CHU_Caen 🏥')
col1, col2,= st.columns(2)

with col1:
    st.subheader('Patients')
    with st.form('new_patient', clear_on_submit=True):
        st.subheader('Ajouter un patient en DB: ')
        nom = st.text_input('Nom de patient :')
        prenom = st.text_input('Prenom du patient :')
        groupe_sanguin = st.radio('Groupe sanguin :', ('A', 'B', 'O', 'AB'))
        date_entree = str(st.date_input("Date d'entrée"))
        submitted = st.form_submit_button('Ajouter')
        if submitted:
            new_patient = Patient(nom, prenom, groupe_sanguin, date_entree)
            new_patient.entrer_a_l_hopital(CONFIG)

with col2:
    st.subheader('RH')
    with st.form('new_rh', clear_on_submit=True):
        st.subheader('Ajouter un RH en DB: ')
        nom = st.text_input('Nom RH :')
        prenom = st.text_input('Prenom RH :')
        salaire = st.number_input('Salaire annuel :', min_value=0, max_value=100000, step=1)
        date_recrutement = str(st.date_input('Date de recrutement'))
        submitted = st.form_submit_button('Ajouter')
        if submitted:
            new_rh = RH(nom, prenom, salaire, date_entree)
            new_rh.debuter_CDD_CDI(CONFIG)

st.subheader("Remplissage aléatoire")
fakes = int(st.number_input("Nombre de faux résidents", step=1))
if st.button("Ajouter"):
    fill_with_fake(fakes)

st.subheader('Affichage des données')
if st.button('Afficher les archives'):
    st.dataframe(df_archive, use_container_width=True)
if st.button('Afficher la table patients'):
    st.dataframe(df_patient, use_container_width=True)
if st.button('Afficher la table rh'):
    st.dataframe(df_rh, use_container_width=True)

st.subheader('Administration des résidents')
col3, col4 = st.columns(2)

with col3:
    st.subheader('Patients')
    with st.form('gone_patient', clear_on_submit=True):
        st.subheader("Quel patient sort de l'hopital ? ")
        id_patient = st.text_input('ID Patient :')
        submitted = st.form_submit_button('Supprimer')
        if submitted:
            Patient.sortir_de_l_hopital(id_patient, CONFIG)

with col4:
    st.subheader('RH')
    with st.form('gone_rh', clear_on_submit=True):
        st.subheader('Quel RH a finit son contrat ? ')
        id_rh = st.text_input('ID RH :')
        submitted = st.form_submit_button('Supprimer')
        if submitted:
            RH.quitter_CDD_CDI(id_rh, CONFIG)

if st.button('⚠️VIDER LA BASE DE DONNEES⚠️'):
    Patient.vider_bdd(CONFIG)
