import streamlit as st
import pandas as pd
import sqlite3
import json

# --- CONFIGURATION ---
st.set_page_config(page_title="Prono Cousins - CDM 2026", page_icon="⚽", layout="wide")
DB_FILE = "pronos_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Table des pronos: stocke le JSON des pronostics par cousin
    c.execute('''CREATE TABLE IF NOT EXISTS pronos (cousin TEXT PRIMARY KEY, data TEXT)''')
    # Table des résultats réels: stocke le JSON des résultats par match
    c.execute('''CREATE TABLE IF NOT EXISTS reels (match_id TEXT PRIMARY KEY, data TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Fonctions d'accès aux données
def get_pronos():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM pronos", conn)
    conn.close()
    return {row['cousin']: json.loads(row['data']) for _, row in df.iterrows()}

def save_prono(nom, data):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT OR REPLACE INTO pronos VALUES (?, ?)", (nom, json.dumps(data)))
    conn.commit()
    conn.close()

def get_reels():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM reels", conn)
    conn.close()
    return {row['match_id']: json.loads(row['data']) for _, row in df.iterrows()}

def save_reels(data_dict):
    conn = sqlite3.connect(DB_FILE)
    for m_id, content in data_dict.items():
        conn.execute("INSERT OR REPLACE INTO reels VALUES (?, ?)", (m_id, json.dumps(content)))
    conn.commit()
    conn.close()

# Initialisation session_state
if 'db_pronos' not in st.session_state: st.session_state.db_pronos = get_pronos()
if 'db_reels' not in st.session_state: st.session_state.db_reels = get_reels()

# --- RESTE DU CODE (Même logique que ton original) ---
# [Copie ici toute ta logique d'interface en remplaçant juste tes fonctions
# charger_json/sauvegarder_json par :
# save_prono(nom, data) et save_reels(data_dict)]

# Exemple de modification pour l'Admin :
# Remplace ton sauvegarder_json(REELS_FILE, nouveaux_reels) par :
# save_reels(nouveaux_reels)
# st.session_state.db_reels = get_reels()