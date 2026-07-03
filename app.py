import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Pronos Cousins", layout="wide")

# Simulation de base de données (Dans le futur, remplace ceci par un fichier CSV ou une base SQL)
if 'pronos' not in st.session_state:
    st.session_state.pronos = pd.DataFrame(columns=["Utilisateur", "Match", "Prono", "Points"])

# --- ESPACE ADMIN ---
def admin_panel():
    st.sidebar.header("🔧 Espace Admin")
    if st.sidebar.checkbox("Activer mode Admin"):
        st.write("### Gestion des données")
        # Exemple : Reset un prono
        if st.button("Reset tous les pronos"):
            st.session_state.pronos = pd.DataFrame(columns=["Utilisateur", "Match", "Prono", "Points"])
            st.success("Données réinitialisées")

# --- INTERFACE PRINCIPALE ---
st.title("⚽ Pronostics Coupe du Monde - Cousins")

admin_panel()

# Matchs du 6 au 10 juillet
matchs = ["Brésil vs France", "Argentine vs Allemagne", "Espagne vs Portugal"]

user_name = st.text_input("Ton prénom :")
match_select = st.selectbox("Choisir le match :", matchs)
prono = st.text_input("Ton pronostic (ex: 2-1) :")

if st.button("Valider mon prono"):
    new_entry = {"Utilisateur": user_name, "Match": match_select, "Prono": prono, "Points": 0}
    st.session_state.pronos = pd.concat([st.session_state.pronos, pd.DataFrame([new_entry])], ignore_index=True)
    st.success("Prono enregistré !")

# --- CLASSEMENT ---
st.write("## 🏆 Classement")
st.table(st.session_state.pronos.groupby("Utilisateur")["Points"].sum().sort_values(ascending=False))