import streamlit as st
from components.sidebar import sidebar
import requests
import os
import json


st.set_page_config(page_title="Cétautomatix", page_icon="🤖", layout="wide")
st.header("Cétautomatix")
sidebar()

albert_api_key = st.session_state.get("ALBERT_API_KEY")

# in the end, I rather not use an api key here for security reasons
if not albert_api_key:
    st.warning(
        "Entrez votre clef d'API Albert, vous pouvez en obtenir une en demandant à l'équipe Etalab."
        "https://etalab.gouv.fr"
    )

st.write("Bonjour, je suis Cétautomatix, votre assistant virtuel de CERFA en cours de developpement.")
user_choice = st.radio("Que voulez-vous faire aujourd'hui?", [
                                                "1. lister les collections d'Albert disponibles", 
                                                "2. Obtenir de l'aide pour remplir un CERFA (WIP)",
                                                "3. Obtenir un résumé sur un document en particulier",
                                                ], key="user_choice")

submit = st.button("Valider")
if(submit):
    backend_url=os.environ.get("BACKEND_URL", "http://localhost:8000")
    if user_choice == "1. lister les collections d'Albert disponibles":
        response = requests.get(f"{backend_url}/collections")
        c = response.json()["collections"]
        st.table(c.values())
    elif user_choice == "2. Obtenir de l'aide pour remplir un CERFA":
        cerfa_choice = st.radio("Pour quel CERFA, voulez-vous obtenir de l'aide?", [
                                                "1. CERFA xxx", 
                                                "2. CERFA_yyy",
                                                "3. CERFA_zzz",
                                                ], key="cerfa_choice")
        pass
    elif user_choice == "3. Obtenir un résumé sur un document en particulier":
        with st.form("summary_form"):
            document_url = st.text_input("Entrez l'url du document à résumer", value="")
            collections = requests.get(f"{backend_url}/collections").json()["collections"]
            collections_to_use = st.multiselect("Quelles collections voulez-vous utiliser?", collections.keys(), format_func=lambda x: collections.get(x).get("name"), key="collections_to_use")    
            submitted = st.form_submit_button("Valider")
            if(submitted): 
                st.write("Recherche en cours...")    
                data = {
                    "document_url": document_url,
                    "collections_to_use": collections_to_use.keys()
                    }
                st.write(data)
                response = requests.post(url=f"{backend_url}/summary/", 
                                    data=json.dumps(data),
                    headers={"Content-Type": "application/json"},
                )
                st.write(response.json())



