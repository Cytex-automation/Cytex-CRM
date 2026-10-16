import os
import sqlite3
import streamlit as st

# ==========================================
# CONFIGURATION DE LA PAGE & CHARTE GRAPHIQUE
# ==========================================
st.set_page_config(
    page_title="CRM Cytex Automation - Projets & Offres",
    page_icon="⚡",
    layout="wide",
)

# Application de la charte graphique Cytex Automation (Couleurs & Styles CSS)
st.markdown(
    """
    <style>
    .main {
        background-color: #0f1115;
        color: #ffffff;
    }
    h1, h2, h3 {
        color: #f4b41a; /* Jaune / Or de la charte Cytex Automation */
        font-family: 'Sora', sans-serif;
    }
    .stButton>button {
        background-color: #f4b41a;
        color: #0f1115;
        font-weight: bold;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #d19a12;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# GESTION DE LA BASE DE DONNÉES (SQLite)
# ==========================================
DB_NAME = "cytex_crm.db"


def init_db():
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS projets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code_projet TEXT UNIQUE,
            nom_projet TEXT,
            type_projet TEXT,
            client TEXT,
            date_debut TEXT,
            responsable TEXT,
            statut TEXT,
            temps_estime REAL,
            temps_reel REAL,
            date_reception TEXT,
            statut_reception TEXT,
            remarques TEXT
        )
    """)
  conn.commit()
  conn.close()


init_db()


def run_query(query, params=(), fetch=False):
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute(query, params)
  if fetch:
    result = cursor.fetchall()
    conn.close()
    return result
  conn.commit()
  conn.close()


# ==========================================
# INTERFACE UTILISATEUR (UI)
# ==========================================

# En-tête avec Logo / Identité Cytex Automation
st.title("⚡ CYTEX AUTOMATION - CRM & Gestion de Projets")
st.markdown(
    "Plateforme unifiée de gestion commerciale, des offres et des projets"
    " techniques."
)

# Barre latérale pour la navigation et filtres
st.sidebar.header("Navigation")
menu = st.sidebar.选择(
    "Aller à",
    [
        "Tableau de Bord & Projets",
        "Ajouter une Offre / Projet",
        "Gestion & Suivi",
    ],
)

# Photos de garde par défaut selon le type de projet (liens ou images locales)
PHOTOS_GARDE = {
    "Photovoltaïque": "https://images.unsplash.com/photo-1509391365360-e944cf9659d7?auto=format&fit=crop&w=1000&q=80",
    "Domotique": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=1000&q=80",
    "Immotique": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1000&q=80",
}

if menu == "Tableau de Bord & Projets":
  st.header("📋 Vue d'ensemble des Projets & Offres")

  # Filtre par type de projet
  filtre_type = st.sidebar.selectbox(
      "Filtrer par type",
      ["Tous", "Photovoltaïque", "Domotique", "Immotique"],
  )

  if filtre_type == "Tous":
    projets = run_query("SELECT * FROM projets", fetch=True)
  else:
    projets = run_query(
        "SELECT * FROM projets WHERE type_projet = ?", (filtre_type,), fetch=True
    )

  if not projets:
    st.info(
        "Aucun projet enregistré pour le moment. Utilisez l'onglet 'Ajouter une"
        " Offre / Projet'."
    )
  else:
    for p in projets:
      # p structure: id(0), code(1), nom(2), type(3), client(4), date_d(5), resp(6), statut(7), t_est(8), t_reel(9), date_rec(10), s_rec(11), rem(12)
      with st.expander(f"📁 [{p[1]}] {p[2]} — Client: {p[4]} ({p[3]})"):
        col1, col2 = st.columns([1, 2])

        with col1:
          # Affichage de la photo de garde selon le type de projet
          type_p = p[3]
          img_url = PHOTOS_GARDE.get(type_p, PHOTOS_GARDE["Domotique"])
          st.image(
              img_url,
              caption=f"Type : {type_p}",
              use_container_width=True,
          )

        with col2:
          st.markdown(f"**Responsable :** {p[6]}")
          st.markdown(f"**Date de début :** {p[5]}")
          st.markdown(f"**Statut Actuel :** `{p[7]}`")
          st.markdown(
              f"**Temps (Estimé / Réel) :** {p[8]}h / {p[9]}h"
          )
          st.markdown(
              f"**Réception :** {p[10]} (Statut : *{p[11]}*)"
          )
          st.markdown(f"**Remarques :** {p[12]}")

elif menu == "Ajouter une Offre / Projet":
  st.header("➕ Créer une nouvelle Offre ou un nouveau Projet")

  with st.form("form_projet"):
    col1, col2 = st.columns(2)

    with col1:
      code_projet = st.text_input(
          "Code Projet / Réf", value="PRJ-2026-004"
      )
      nom_projet = st.text_input(
          "Nom du Projet", value="Installation Smart Home"
      )
      type_projet = st.selectbox(
          "Type de Projet", ["Photovoltaïque", "Domotique", "Immotique"]
      )
      client = st.text_input("Nom du Client")
      date_debut = st.date_input("Date de Début")

    with col2:
      responsable = st.text_input("Responsable Technique / Commercial")
      statut = st.selectbox(
          "Statut",
          [
              "Étude & Plans",
              "Offre Envoyée",
              "Commande",
              "Chantier en cours",
              "Réceptionné",
          ],
      )
      temps_estime = st.number_input("Temps Estimé (heures)", value=40.0)
      temps_reel = st.number_input("Temps Réel (heures)", value=0.0)
      date_reception = st.date_input("Date Réception Prévisionnelle")
      statut_reception = st.selectbox(
          "Statut Réception", ["Non démarré", "En attente", "PV Signé"]
      )

    remarques = st.text_area("Remarques & Historique des offres")

    submit = st.form_submit_button("Enregistrer le Projet")

    if submit:
      try:
        run_query(
            """
                    INSERT INTO projets (code_projet, nom_projet, type_projet, client, date_debut, responsable, statut, temps_estime, temps_reel, date_reception, statut_reception, remarques)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
            (
                code_projet,
                nom_projet,
                type_projet,
                client,
                str(date_debut),
                responsable,
                statut,
                temps_estime,
                temps_reel,
                str(date_reception),
                statut_reception,
                remarques,
            ),
        )
        st.success(
            "✅ Projet / Offre enregistré avec succès dans la base de données !"
        )
      except sqlite3.IntegrityError:
        st.error(
            "Erreur : Un projet avec ce code existe déjà. Veuillez modifier le"
            " code."
        )

elif menu == "Gestion & Suivi":
  st.header("📊 Indicateurs Clés & Exportation")

  projets = run_query("SELECT * FROM projets", fetch=True)
  if projets:
    st.metric("Nombre total de projets / offres", len(projets))

    # Option pour exporter en CSV pour partage Drive
    if st.button("📥 Télécharger les données (CSV)"):
      import pandas as pd

      df = pd.read_sql_query("SELECT * FROM projets", sqlite3.connect(DB_NAME))
      st.download_button(
          label="Confirmer le téléchargement CSV",
          data=df.to_csv(index=False).encode("utf-8"),
          file_name="CytexAutomation_CRM_Export.csv",
          mime="text/csv",
      )
  else:
    st.info("Aucune donnée disponible.")