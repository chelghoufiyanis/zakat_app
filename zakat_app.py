import streamlit as st
import requests
from datetime import datetime

# Configuration de la page (pour que ça ressemble à une appli mobile)
st.set_page_config(page_title="Zakat Pro", page_icon="🌙")

# --- FONCTION API ---
def obtenir_prix_or():
    CLE_API = "goldapi-9um5smlc6thjh-io"
    url = "https://www.goldapi.io/api/XAU/EUR"
    headers = {"x-access-token": CLE_API, "Content-Type": "application/json"}
    try:
        reponse = requests.get(url, headers=headers)
        if reponse.status_code == 200:
            return reponse.json()['price'] / 31.1035
        return 134.50
    except:
        return 134.50

# --- INTERFACE GRAPHIQUE ---
st.title("🌙 Zakat Calculator")
st.write("Calculez votre Zakat avec le cours de l'or en temps réel.")

prix_g = obtenir_prix_or()
nisab = prix_g * 85

# Affichage des infos marchés dans des jolis encadrés
col1, col2 = st.columns(2)
col1.metric("Or (1g)", f"{prix_g:.2f} €")
col2.metric("Nisab", f"{nisab:.2f} €")

st.divider()

# Formulaire de saisie
with st.container():
    epargne = st.number_input("Épargne totale (Banque + Espèces)", min_value=0.0, step=100.0)
    or_val = st.number_input("Valeur de l'or possédé (€)", min_value=0.0, step=100.0)
    dettes = st.number_input("Dettes à déduire", min_value=0.0, step=10.0)

    richesse = (epargne + or_val) - dettes

if st.button("Calculer ma Zakat", use_container_width=True):
    if richesse >= nisab:
        zakat = richesse * 0.025
        st.success(f"Salam {nom}, votre Zakat est de **{zakat:.2f} €**")
        st.balloons() # Petite animation de fête !
    else:
        st.info(f"Salam {nom}, la Zakat n'est pas due. (Manque {(nisab - richesse):.2f} €)")
        
# --- PREMIER MENU : LE POURQUOI ---
with st.expander("🧐 Pourquoi calculer le Nisab ?"):
    st.markdown("""
    Le **Nisab** est le seuil minimum de richesse au-delà duquel la Zakat devient une obligation. 
    
    * **Si votre patrimoine est inférieur au Nisab :** vous n'avez pas à payer la Zakat.
    * **Si votre patrimoine est supérieur au Nisab :** vous devez verser 2,5 % de vos avoirs.
    
    Cela permet de s'assurer que seuls ceux qui ont une épargne stable participent à cet effort de solidarité, protégeant ainsi les foyers plus modestes.
    """)

# --- DEUXIÈME MENU : LE COMMENT ---
with st.expander("🧮 Comment est-ce calculé ?"):
    st.markdown("""
    ### L'origine historique
    À l'époque du Prophète (SWS), le seuil de richesse a été fixé à **20 Dinars d'or** (aussi appelés *Mithqal*). 
    
    Les historiens et les savants ont établi qu'un Dinar d'or pesait **4,25 grammes**. 
    Le calcul pour trouver le poids de référence est donc :
    """)
    
    # Formule du poids historique
    st.latex(r"20 \text{ Dinars} \times 4,25\text{g} = 85\text{g}")

    st.markdown("""
    ---
    ### Le calcul monétaire actuel
    Pour transformer ces 85g en euros, l'application multiplie ce poids par le cours de l'or en temps réel :
    """)
    
    # Formule du prix du jour
    st.latex(r"85\text{g} \times \text{Prix du gramme d'or} = \text{Nisab (€)}")
    
    st.markdown(f"""
    **Détails du calcul en direct :**
    * Poids de référence : **85g**
    * Prix du gramme : **{prix_g:.2f} €/g**
    * **Seuil final : {nisab:.2f} €**
    
    *Si votre épargne dépasse ce montant, vous devez verser 2,5 %.*
    """)



