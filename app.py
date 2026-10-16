import sqlite3
import pandas as pd
import streamlit as st

# ==========================================
# CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="Cytex Automation - Offres & Gestion Commerciale",
    page_icon="⚡",
    layout="wide",
)

# Style CSS aux normes de la charte graphique et des rapports officiels
st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; color: #111111; }
    h1, h2, h3 { color: #1e293b; font-family: 'Sora', sans-serif; }
    .report-header {
        border-bottom: 3px solid #f4b41a;
        padding-bottom: 15px;
        margin-bottom: 25px;
    }
    .stButton>button {
        background-color: #f4b41a;
        color: #0f1115;
        font-weight: bold;
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# BASE DE DONNÉES (SQLite)
# ==========================================
DB_NAME = "cytex_crm.db"


def init_db():
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS offres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ref_offre TEXT UNIQUE,
            client_nom TEXT,
            client_attn TEXT,
            date_offre TEXT,
            type_projet TEXT,
            objet TEXT,
            montant_total REAL,
            statut TEXT,
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
# INTERFACE UTILISATEUR
# ==========================================

st.sidebar.header("Navigation")
menu = st.sidebar.selectbox(
    "Aller à",
    [
        "📄 Générateur d'Offre (Format Officiel)",
        "📋 Tableau de Bord Commercial",
        "➕ Créer une Offre",
    ],
)

PHOTOS_GARDE = {
    "Photovoltaïque": "https://images.unsplash.com/photo-1509391365360-e944cf9659d7?auto=format&fit=crop&w=1000&q=80",
    "Domotique": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=1000&q=80",
    "Immotique": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1000&q=80",
}

if menu == "📄 Générateur d'Offre (Format Officiel)":
  st.markdown(
      """
    <div class="report-header">
        <h1>CYTEX AUTOMATION</h1>
        <p><b>Commercial Proposal & Technical Project Management</b> | Document Officiel d'Offre</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  offres = run_query("SELECT * FROM offres", fetch=True)
  if not offres:
    st.info(
        "Aucune offre enregistrée. Veuillez utiliser l'onglet 'Créer une Offre'."
    )
  else:
    refs = [o[1] for o in offres]
    selected_ref = st.selectbox("Sélectionner l'Offre / Projet à éditer", refs)

    offre = [o for o in offres if o[1] == selected_ref][0]
    # offre structure: id(0), ref(1), client(2), attn(3), date(4), type(5), objet(6), montant(7), statut(8), rem(9)

    col1, col2 = st.format = st.columns([2, 1])
    with col1:
      st.markdown(f"### Réf : **{offre[1]}**")
      st.markdown(f"**Date :** {offre[4]}")
      st.markdown(f"**Client :** {offre[2]}")
      st.markdown(f"**À l'attention de :** {offre[3]}")
      st.markdown(f"**Objet :** {offre[6]}")
    with col2:
      type_p = offre[5]
      st.image(
          PHOTOS_GARDE.get(type_p, PHOTOS_GARDE["Domotique"]),
          caption=f"Couverture - {type_p}",
          use_container_width=True,
      )

    st.markdown("---")
    st.subheader("1. Bill of Quantities (Détail estimatif)")
    st.markdown(
        """
        | S.No | Description des Équipements / Prestations | Type / Spécification | Qte | Prix Unitaire (TND) | Total (TND) |
        | :--- | :--- | :--- | :---: | :---: | :---: |
        | 1 | Étude technique, ingénierie et synoptique | Standard | 1 | 1,200.00 | 1,200.00 |
        | 2 | Fourniture et pose des équipements principaux | """
        + offre[5]
        + """ | 1 | """
        + f"{offre[7]:,.2f}"
        + """ | """
        + f"{offre[7]:,.2f}"
        + """ |
        | 3 | Câblage, raccordement et mise en service | Sur site | 1 | 850.00 | 850.00 |
        """
    )

    st.subheader("2. Scope of Works (Étendue des Travaux)")
    st.markdown(
        "- Installation complète selon les règles de l'art et les normes de sécurité en vigueur.\n"
        "- Tests de bon fonctionnement, paramétrage initial et remise des manuels d'utilisation.\n"
        "- Formation de l'équipe technique du client sur site."
    )

    st.subheader("3. Client's Scope (Engagements Client)")
    st.markdown(
        "- Fournir l'accès sécurisé au site et l'énergie nécessaire pour les travaux.\n"
        "- Obtenir les autorisations administratives préalables si requis."
    )

    st.subheader("4. Commercial Proposal Summary")
    st.success(f"**Montant Total HT de l'Offre : {offre[7]:,.2f} TND**")
    st.markdown(f"**Statut Actuel de l'Offre :** `{offre[8]}`")
    st.markdown(f"**Remarques particulières :** {offre[9]}")

elif menu == "➕ Créer une Offre":
  st.header("➕ Établir une Nouvelle Offre Commerciale")

  with st.form("form_offre"):
    col1, col2 = st.columns(2)
    with col1:
      ref_offre = st.text_input("Référence Offre", value="CYTEX-OFF-2026-01")
      client_nom = st.text_input("Nom de l'Entreprise / Client")
      client_attn = st.text_input("À l'attention de (Contact)")
      date_offre = st.date_input("Date de l'offre")
    with col2:
      type_projet = st.selectbox(
          "Type de Projet", ["Photovoltaïque", "Domotique", "Immotique"]
      )
      objet = st.text_input(
          "Objet de l'Offre", value="Installation et mise en service"
      )
      montant_total = st.number_input(
          "Montant Total Proposé (TND)", value=5500.0
      )
      statut = st.selectbox(
          "Statut Commercial",
          [
              "En attente de validation",
              "Offre Validée / Bon de Commande",
              "En cours de réalisation",
              "Clôturé / Réceptionné",
          ],
      )

    remarques = st.text_area(
        "Notes et conditions particulières (Validité, Délais...)"
    )

    submit = st.form_submit_button("Enregistrer l'Offre")
    if submit:
      try:
        run_query(
            """
                    INSERT INTO offres (ref_offre, client_nom, client_attn, date_offre, type_projet, objet, montant_total, statut, remarques)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
            (
                ref_offre,
                client_nom,
                client_attn,
                str(date_offre),
                type_projet,
                objet,
                montant_total,
                statut,
                remarques,
            ),
        )
        st.success(
            "✅ Offre enregistrée avec succès ! Vous pouvez la visualiser dans"
            " l'onglet 'Générateur d'Offre'."
        )
      except sqlite3.IntegrityError:
        st.error("Erreur : Cette référence d'offre existe déjà.")

elif menu == "📋 Tableau de Bord Commercial":
  st.header("📊 Suivi Global des Offres et Projets")
  df = pd.read_sql_query("SELECT * FROM offres", sqlite3.connect(DB_NAME))
  if not df.empty:
    st.dataframe(df, use_container_width=True)
    st.metric("Chiffre d'affaires potentiel (Total)", f"{df['montant_total'].sum():,.2f} TND")
  else:
    st.info("Aucune donnée à afficher.")
