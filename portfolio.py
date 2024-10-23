import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_compact_histogram(x_column, data, labels_dict, title, fig_size=(5, 3)):
    plt.figure(figsize=fig_size)  # Ajuster la taille de la figure
    sns.countplot(x=x_column, data=data, palette="viridis", order=labels_dict.keys())
    plt.title(title, fontsize=14, weight='bold')
    plt.xlabel(x_column, fontsize=10)
    plt.ylabel("Fréquence", fontsize=10)
    
    plt.xticks(rotation=45, ha="right")
    
    # Appliquer les nouvelles étiquettes
    plt.xticks(ticks=range(len(labels_dict)), labels=list(labels_dict.values()), rotation=45, ha="right")
    
    plt.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(plt)

# Charger les données

data = pd.read_csv("DS_RP_POPULATION_PRINC_sample.csv", sep=';', header=0)
"""
#TEMPORAIRE
sample_size = int(len(data) / 10)  # Calculer un dixième du nombre total de lignes
data = data.sample(n=sample_size, random_state=42)  # Prendre un échantillon aléatoire
data.to_csv("DS_RP_POPULATION_PRINC_sample.csv", sep=';', index=False)
"""


time_period_dict = {
    '2010': '2010',
    '2015': '2015',
    '2021': '2021'
}

emp_status_dict = {
    '_T': 'Total',
    '1': 'Actif occupé',
    '2': 'Chômeur',
    '31': 'Retraités ou préretraités',
    '33': 'Élèves, étudiants',
    '35': 'Au foyer',
    '36': 'Autres inactifs'
}

# Nouveau dictionnaire d'âge
age_dict = {
    '_T': 'Total',
    'Y_GE15': '15 ans ou plus',
    'Y_GE65': '65 ans ou plus',
    'Y_GE80': '80 ans ou plus',
    'Y_LT15': 'Moins de 15 ans',
    'Y_LT20': 'Moins de 20 ans',
    'Y15T24': '15-24 ans',
    'Y25T39': '25-39 ans',
    'Y40T54': '40-54 ans',
    'Y55T64': '55-64 ans',
    'Y65T79': '65-79 ans'
}

sex_dict = {
    'M': 'Homme',
    'F': 'Femme',
    '_T': 'Total'
}

civil_status_dict = {
    '_T': 'Total',
    '1': 'Marié',
    '2': 'Pacsé',
    '3': 'Concubinage',
    '4': 'Veuf',
    '5': 'Divorcé',
    '6': 'Célibataire'
}

population_category_dict = {
    '_T': 'Total',
    '01': 'Logement',
    '11': 'Long séjour, maison de retraite',
    '12': 'Communauté religieuse',
    '13': 'Militaire',
    '14': 'Élève interne',
    '15_17': 'Autre',
    '16': 'Court séjour',
    '20': 'Sans-abri'
}


# Personnalisation globale des graphiques
sns.set(style="whitegrid")

# Initialisation de cleaned_data
cleaned_data = data.copy()


# Titre de la page
st.set_page_config(page_title="Analyse de la Population", page_icon=":bar_chart:", layout="wide")
st.title("Analyse de la Population - Visualisation des données")






# Barre de navigation
nav_option = st.sidebar.selectbox("Projet Population :", 
                                    ["Données brutes", 
                                     "Données Etat civil",
                                     "Données Statut d'Emploi",
                                     "Données HAR",
                                     "Homme vs Femme"])



# Ajout des coordonnées et du lien LinkedIn dans la barre de navigation
st.sidebar.header("Mes Coordonnées")
st.sidebar.text("Nom: HO Stéphane")
st.sidebar.text("Email: truong.ho@efrei.net")
st.sidebar.markdown("[Mon LinkedIn](https://www.linkedin.com/in/votreprofil)")

# Bouton pour télécharger le CV
st.sidebar.download_button(
    label="Télécharger mon CV",
    data=open("C:/Users\steph\OneDrive\Desktop\CV Stephane HO.pdf", 'rb').read(),  # Remplacez par le chemin vers votre CV
    file_name='Mon_CV.pdf',
    mime='application/pdf'
)

st.sidebar.image("efrei logo.png", use_column_width=True)

if nav_option == "Données brutes":
    # Section Données brutes

    # Création d'un sélecteur pour choisir l'année
    years = ['Tout', 2010, 2015, 2021]  # Liste des années avec l'option "Tout"
    selected_year = st.selectbox("Sélectionner une année :", years)

    # Filtrage des données en fonction de l'année sélectionnée
    if selected_year == 'Tout':
        cleaned_data = data  # Pas de filtrage
    else:
        cleaned_data = data[data['TIME_PERIOD'] == selected_year]

    # Afficher le nombre de lignes et les premières lignes du DataFrame nettoyé
    st.write(f"Nombre de lignes dans les données : {len(cleaned_data)}")
    st.write("Premières lignes des données nettoyées :")
    st.dataframe(cleaned_data.head())

    # Disposition en deux lignes avec 3 colonnes par ligne
    col1, col2, col3 = st.columns(3)  # Première ligne
    col4, col5, col6 = st.columns(3)  # Deuxième ligne

    with col1:
        plot_compact_histogram('TIME_PERIOD', cleaned_data, time_period_dict, "Distribution par Période de Temps", fig_size=(5, 3))

    with col2:
        plot_compact_histogram('EMPSTA_ENQ', cleaned_data, emp_status_dict, "Distribution par Statut d'Emploi", fig_size=(5, 3))

    with col3:
        plot_compact_histogram('AGE', cleaned_data, age_dict, "Distribution par Âge", fig_size=(5, 3))

    with col4:
        plot_compact_histogram('SEX', cleaned_data, sex_dict, "Distribution par Sexe", fig_size=(5, 3))

    with col5:
        plot_compact_histogram('CIVIL_STATUS', cleaned_data, civil_status_dict, "Distribution par État Civil", fig_size=(5, 3))

    with col6:
        plot_compact_histogram('HAR', cleaned_data, population_category_dict, "Distribution par HAR", fig_size=(5, 3))
    
    
    
    
    

elif nav_option == "Données Etat civil":
    filtres = ["Sans filtre", "Sexe connu","Sexe inconnu", "Voir distribution de l'age"] 
    selected_filter = st.selectbox("Filtre pour CIVIL_STATUS :", filtres)

    cleaned_data = data[data['TIME_PERIOD'] == 2021]
    cleaned_data = cleaned_data[cleaned_data['CIVIL_STATUS']!='_T']
    if selected_filter in  ["Sans filtre", "Sexe connu","Sexe inconnu"] :
    
        if selected_filter == 'Sans filtre':
            cleaned_data = data[data['TIME_PERIOD'] == 2021]
            cleaned_data = cleaned_data[cleaned_data['CIVIL_STATUS']!='_T']
        elif selected_filter == 'Sexe connu':
            cleaned_data = cleaned_data[cleaned_data['SEX']!='_T']
        elif selected_filter == 'Sexe inconnu':
            cleaned_data = cleaned_data[cleaned_data['SEX']=='_T']   
            
    
    
        # Affichage des données filtrées
        st.write(f"Nombre de lignes dans les données filtrées : {len(cleaned_data)}")
        st.write("Premières lignes des données filtrées :")
        st.dataframe(cleaned_data.head())
        
        
        
    
        col1, col2, col3 = st.columns(3)  # Première ligne
        col4, col5, col6 = st.columns(3)  # Deuxième ligne
    
        with col1:
            plot_compact_histogram('TIME_PERIOD', cleaned_data, time_period_dict, "Distribution par Période de Temps (Données nettoyées)", fig_size=(5, 3))
    
        with col2:
            plot_compact_histogram('EMPSTA_ENQ', cleaned_data, emp_status_dict, "Distribution par Statut d'Emploi (Données nettoyées)", fig_size=(5, 3))
    
        with col3:
            plot_compact_histogram('AGE', cleaned_data, age_dict, "Distribution par Âge (Données nettoyées)", fig_size=(5, 3))
    
        with col4:
            plot_compact_histogram('SEX', cleaned_data, sex_dict, "Distribution par Sexe (Données nettoyées)", fig_size=(5, 3))
    
        with col5:
            plot_compact_histogram('CIVIL_STATUS', cleaned_data, civil_status_dict, "Distribution par État Civil (Données nettoyées)", fig_size=(5, 3))
        with col6:
            plot_compact_histogram('HAR', cleaned_data, population_category_dict, "Distribution par HAR", fig_size=(5, 3))
    
    elif selected_filter == "Voir distribution de l'age":
        
        
        cleaned_data = data[data['TIME_PERIOD'] == 2021]
        cleaned_data = cleaned_data[cleaned_data['CIVIL_STATUS']!='_T']
        cleaned_data = cleaned_data[cleaned_data['AGE']!='Y_GE15']
        
        cleaned_data1 = cleaned_data[cleaned_data['CIVIL_STATUS']=='1']
        cleaned_data2 = cleaned_data[cleaned_data['CIVIL_STATUS']=='2']
        cleaned_data3 = cleaned_data[cleaned_data['CIVIL_STATUS']=='3']
        cleaned_data4 = cleaned_data[cleaned_data['CIVIL_STATUS']=='4']
        cleaned_data5 = cleaned_data[cleaned_data['CIVIL_STATUS']=='5']
        cleaned_data6 = cleaned_data[cleaned_data['CIVIL_STATUS']=='6']
        
        
        col1, col2, col3 = st.columns(3)  # Première ligne
        col4, col5, col6 = st.columns(3)  # Deuxième ligne

        with col1:
            plot_compact_histogram('AGE', cleaned_data1, age_dict, "Distribution Marié", fig_size=(5, 3))

        with col2:
            plot_compact_histogram('AGE', cleaned_data2, age_dict, "Distribution Pacsé", fig_size=(5, 3))

        with col3:
            plot_compact_histogram('AGE', cleaned_data3, age_dict, "Distribution Concubinage", fig_size=(5, 3))

        with col4:
            plot_compact_histogram('AGE', cleaned_data4, age_dict, "Distribution Veuf", fig_size=(5, 3))

        with col5:
            plot_compact_histogram('AGE', cleaned_data5, age_dict, "Distribution Divorcé", fig_size=(5, 3))
        with col6:
            plot_compact_histogram('AGE', cleaned_data6, age_dict, "Distribution Célibataire", fig_size=(5, 3))
    
    
    
    
    
    
elif nav_option == "Données Statut d'Emploi":
    
    filtres = ["Sans filtre", "Sexe connu", "Sexe inconnu","Voir distribution de l'age"]  # Liste des années avec l'option "Tout"
    selected_filter = st.selectbox("Filtre pour CIVIL_STATUS :", filtres)

    cleaned_data = data[data['TIME_PERIOD'] == 2021]
    cleaned_data = cleaned_data[cleaned_data['EMPSTA_ENQ']!='_T']
    if selected_filter in ["Sans filtre", "Sexe connu", "Sexe inconnu"]:
        if selected_filter == 'Sans filtre':
            cleaned_data = data[data['TIME_PERIOD'] == 2021]
            cleaned_data = cleaned_data[cleaned_data['EMPSTA_ENQ']!='_T']
        elif selected_filter == 'Sexe connu':
            cleaned_data = cleaned_data[cleaned_data['SEX']!='_T']
        elif selected_filter == 'Sexe inconnu':
            cleaned_data = cleaned_data[cleaned_data['SEX']=='_T']    
            
        
        
        st.write(f"Nombre de lignes dans les données filtrées : {len(cleaned_data)}")
        st.write("Premières lignes des données filtrées :")
        st.dataframe(cleaned_data.head())
    
        col1, col2, col3 = st.columns(3)  
        col4, col5, col6 = st.columns(3) 
    
        with col1:
            plot_compact_histogram('TIME_PERIOD', cleaned_data, time_period_dict, "Distribution par Période de Temps (Données nettoyées)", fig_size=(5, 3))
    
        with col2:
            plot_compact_histogram('EMPSTA_ENQ', cleaned_data, emp_status_dict, "Distribution par Statut d'Emploi (Données nettoyées)", fig_size=(5, 3))
    
        with col3:
            plot_compact_histogram('AGE', cleaned_data, age_dict, "Distribution par Âge (Données nettoyées)", fig_size=(5, 3))
    
        with col4:
            plot_compact_histogram('SEX', cleaned_data, sex_dict, "Distribution par Sexe (Données nettoyées)", fig_size=(5, 3))
    
        with col5:
            plot_compact_histogram('CIVIL_STATUS', cleaned_data, civil_status_dict, "Distribution par État Civil (Données nettoyées)", fig_size=(5, 3))
        with col6:
            plot_compact_histogram('HAR', cleaned_data, population_category_dict, "Distribution par HAR", fig_size=(5, 3))


    elif selected_filter == "Voir distribution de l'age":
        

        cleaned_data = data[data['TIME_PERIOD'] == 2021]
        cleaned_data = cleaned_data[cleaned_data['EMPSTA_ENQ']!='_T']
        cleaned_data = cleaned_data[cleaned_data['AGE']!='Y_GE15']
        
        cleaned_data1 = cleaned_data[cleaned_data['EMPSTA_ENQ']=='1']
        cleaned_data2 = cleaned_data[cleaned_data['EMPSTA_ENQ']=='2']
        cleaned_data3 = cleaned_data[cleaned_data['EMPSTA_ENQ']=='31']
        cleaned_data4 = cleaned_data[cleaned_data['EMPSTA_ENQ']=='33']
        cleaned_data5 = cleaned_data[cleaned_data['EMPSTA_ENQ']=='35']
        cleaned_data6 = cleaned_data[cleaned_data['EMPSTA_ENQ']=='36']
        
        
        col1, col2, col3 = st.columns(3)  # Première ligne
        col4, col5, col6 = st.columns(3)  # Deuxième ligne

        with col1:
            plot_compact_histogram('AGE', cleaned_data1, age_dict, "Distribution Actif occupé", fig_size=(5, 3))

        with col2:
            plot_compact_histogram('AGE', cleaned_data2, age_dict, "Distribution Chômeur", fig_size=(5, 3))

        with col3:
            plot_compact_histogram('AGE', cleaned_data3, age_dict, "Distribution Retraités ou préretraités", fig_size=(5, 3))

        with col4:
            plot_compact_histogram('AGE', cleaned_data4, age_dict, "Distribution Élèves, étudiants", fig_size=(5, 3))

        with col5:
            plot_compact_histogram('AGE', cleaned_data5, age_dict, "Distribution Au foyer", fig_size=(5, 3))
        with col6:
            plot_compact_histogram('AGE', cleaned_data6, age_dict, "Distribution Autres inactifs", fig_size=(5, 3))
    
    
    

elif nav_option == "Données HAR":
    
    filtres = ["Sans filtre", "Sexe connu","Sexe inconnu","Voir distribution de l'age"]  # Liste des années avec l'option "Tout"
    selected_filter = st.selectbox("Filtre pour HAR :", filtres)

    cleaned_data = data[data['TIME_PERIOD'] == 2021]
    cleaned_data = cleaned_data[cleaned_data['HAR']!='_T']
    
    
    if selected_filter in ["Sans filtre", "Sexe connu","Sexe inconnu"]:
        if selected_filter == 'Sans filtre':
            cleaned_data = data[data['TIME_PERIOD'] == 2021]
            cleaned_data = cleaned_data[cleaned_data['HAR']!='_T']
        elif selected_filter == 'Sexe connu':
            cleaned_data = cleaned_data[cleaned_data['SEX']!='_T']
        elif selected_filter == 'Sexe inconnu':
            cleaned_data = cleaned_data[cleaned_data['SEX']=='_T']   
        
    
        st.write(f"Nombre de lignes dans les données filtrées : {len(cleaned_data)}")
        st.write("Premières lignes des données filtrées :")
        st.dataframe(cleaned_data.head())
        
        col1, col2, col3 = st.columns(3)  
        col4, col5, col6 = st.columns(3)  
        with col1:
            plot_compact_histogram('TIME_PERIOD', cleaned_data, time_period_dict, "Distribution par Période de Temps (Données nettoyées)", fig_size=(5, 3))
    
        with col2:
            plot_compact_histogram('EMPSTA_ENQ', cleaned_data, emp_status_dict, "Distribution par Statut d'Emploi (Données nettoyées)", fig_size=(5, 3))
    
        with col3:
            plot_compact_histogram('AGE', cleaned_data, age_dict, "Distribution par Âge (Données nettoyées)", fig_size=(5, 3))
    
        with col4:
            plot_compact_histogram('SEX', cleaned_data, sex_dict, "Distribution par Sexe (Données nettoyées)", fig_size=(5, 3))
    
        with col5:
            plot_compact_histogram('CIVIL_STATUS', cleaned_data, civil_status_dict, "Distribution par État Civil (Données nettoyées)", fig_size=(5, 3))
        with col6:
            plot_compact_histogram('HAR', cleaned_data, population_category_dict, "Distribution par HAR", fig_size=(5, 3))


    elif selected_filter == "Voir distribution de l'age":


        cleaned_data = data[data['TIME_PERIOD'] == 2021]
        cleaned_data = cleaned_data[cleaned_data['HAR']!='_T']
        
        cleaned_data = cleaned_data[cleaned_data['AGE']!='Y_GE15']
        cleaned_data = cleaned_data[cleaned_data['AGE']!='_T']
        
        cleaned_data1 = cleaned_data[cleaned_data['HAR']=='01']
        cleaned_data2 = cleaned_data[cleaned_data['HAR']=='11']
        cleaned_data3 = cleaned_data[cleaned_data['HAR']=='12']
        cleaned_data4 = cleaned_data[cleaned_data['HAR']=='13']
        cleaned_data5 = cleaned_data[cleaned_data['HAR']=='14']
        cleaned_data6 = cleaned_data[cleaned_data['HAR']=='15_17']
        cleaned_data7 = cleaned_data[cleaned_data['HAR']=='16']
        cleaned_data8 = cleaned_data[cleaned_data['HAR']=='20']
        
        
        col1, col2, col3 = st.columns(3)  # Première ligne
        col4, col5, col6 = st.columns(3)  # Deuxième ligne
        col7, col8, col9 = st.columns(3)

        with col1:
            plot_compact_histogram('AGE', cleaned_data1, age_dict, "Distribution Logement", fig_size=(5, 3))

        with col2:
            plot_compact_histogram('AGE', cleaned_data2, age_dict, "Distribution Long séjour, maison de retraite", fig_size=(5, 3))

        with col3:
            plot_compact_histogram('AGE', cleaned_data3, age_dict, "Distribution communauté religieuse", fig_size=(5, 3))
            
        with col4:
            plot_compact_histogram('AGE', cleaned_data4, age_dict, "Distribution Militaire", fig_size=(5, 3))

        with col5:
            plot_compact_histogram('AGE', cleaned_data5, age_dict, "Distribution Eleve interne", fig_size=(5, 3))
        with col6:
            plot_compact_histogram('AGE', cleaned_data6, age_dict, "Distribution Autre", fig_size=(5, 3))
        with col7:
            plot_compact_histogram('AGE', cleaned_data7, age_dict, "Distribution Court séjour", fig_size=(5, 3))
        with col8:
            plot_compact_histogram('AGE', cleaned_data8, age_dict, "Distribution Sans abri", fig_size=(5, 3))
            

elif nav_option == "Homme vs Femme":
    cleaned_data_emploi = data[data['TIME_PERIOD'] == 2021]
    cleaned_data_emploi = cleaned_data_emploi[cleaned_data_emploi['EMPSTA_ENQ'] != '_T']
    cleaned_data_emploi = cleaned_data_emploi[cleaned_data_emploi['SEX'] != '_T']
    
    cleaned_data_civil = data[data['TIME_PERIOD'] == 2021]
    cleaned_data_civil = cleaned_data_civil[cleaned_data_civil['CIVIL_STATUS'] != '_T']
    cleaned_data_civil = cleaned_data_civil[cleaned_data_civil['SEX'] != '_T']
    
    
    cleaned_data_har = data[data['TIME_PERIOD'] == 2021]
    cleaned_data_har = cleaned_data_har[cleaned_data_har['HAR'] != '_T']
    cleaned_data_har = cleaned_data_har[cleaned_data_har['SEX'] != '_T']
    
    hommes_data_emploi = cleaned_data_emploi[cleaned_data_emploi['SEX'] == 'M']
    femmes_data_emploi = cleaned_data_emploi[cleaned_data_emploi['SEX'] == 'F']
    
    hommes_data_civil = cleaned_data_civil[cleaned_data_civil['SEX'] == 'M']
    femmes_data_civil = cleaned_data_civil[cleaned_data_civil['SEX'] == 'F']
    
    hommes_data_har = cleaned_data_har[cleaned_data_har['SEX'] == 'M']
    femmes_data_har = cleaned_data_har[cleaned_data_har['SEX'] == 'F']
    
    col1, col2 = st.columns(2)
    
    
    with col1:
        plot_compact_histogram('CIVIL_STATUS', hommes_data_civil, civil_status_dict, "Hommes avec État Civil", fig_size=(5, 3))
    
    with col2:
        plot_compact_histogram('CIVIL_STATUS', femmes_data_civil, civil_status_dict, "Femmes avec État Civil", fig_size=(5, 3))
    st.write("Les etats civils sont équilibrés")
    
    col3, col4 = st.columns(2)
    
    with col3:
        plot_compact_histogram('EMPSTA_ENQ', hommes_data_emploi, emp_status_dict, "Hommes avec Statut d'Emploi", fig_size=(5, 3))
    
    with col4:
        plot_compact_histogram('EMPSTA_ENQ', femmes_data_emploi, emp_status_dict, "Femmes avec Statut d'Emploi", fig_size=(5, 3))
    col5, col6 = st.columns(2)
    
    st.write("Il y a 2 fois moins d'homme au foyer")
    
    with col5:
        plot_compact_histogram('HAR', hommes_data_har, population_category_dict, "Hommes avec HAR", fig_size=(5, 3))
    
    with col6:
        plot_compact_histogram('HAR', femmes_data_har, population_category_dict, "Femmes avec HAR", fig_size=(5, 3))



    
