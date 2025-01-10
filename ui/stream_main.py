import streamlit as st
from components.sidebar import sidebar
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()


st.set_page_config(page_title="Cétautomatix", page_icon="🤖", layout="wide")
st.header("Cétautomatix")
sidebar()

#### UTILS METHODS TO PROBABLY PUT SOMEWHERE ELSE ####
# Inspired by: https://discuss.streamlit.io/t/after-clicking-a-submit-button-create-another-submit-button-and-do-something-else-when-that-button-is-clicked/33425/7
# if "stage" not in st.session_state:
#    st.session_state.stage = 0
#
#
# def set_stage(stage):
#    st.session_state.stage = stage
### In the end, I found a dirty way to do it for this POC instead of trying to mimic React states, but you should not do this at home
#### END OF UTILS METHODS TO PROBABLY PUT SOMEWHERE ELSE ####

albert_api_key = st.session_state.get("ALBERT_API_KEY")
# in the end, I rather not use an api key here for security reasons
if not albert_api_key:
    st.warning("Entrez votre clef d'API Albert, vous pouvez en obtenir une en demandant à l'équipe Etalab." "https://etalab.gouv.fr")

st.write("Bonjour, je suis Cétautomatix, votre assistant virtuel de CERFA en cours de developpement.")
user_choice = st.radio(
    "Que voulez-vous faire aujourd'hui?",
    [
        "1. lister les collections d'Albert disponibles",
        "2. Obtenir de l'aide pour remplir un CERFA (WIP)",
        "3. Obtenir un résumé sur un document en particulier",
    ],
    key="user_choice",
    index=None,
)

# submit = st.button("Valider", key="submit", on_click=set_stage, args=(1,))
# if st.session_state["stage"] == 1:
backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000")
debug_st = os.environ.get("DEBUG_ST", False)
if user_choice == "1. lister les collections d'Albert disponibles":
    response = requests.get(f"{backend_url}/collections")
    c = response.json()["collections"]
    st.table(c.values())
elif user_choice == "2. Obtenir de l'aide pour remplir un CERFA (WIP)":
    cerfa_choice = st.radio(
        "Pour quel CERFA, voulez-vous obtenir de l'aide?",
        [
            "1. CERFA xxx",
            "2. CERFA_yyy",
            "3. CERFA_zzz",
        ],
        key="cerfa_choice",
    )
elif user_choice == "3. Obtenir un résumé sur un document en particulier":
    with st.form("summary_form"):
        document_url = st.text_input("Entrez l'url du document à résumer", value="")
        collections = requests.get(f"{backend_url}/collections").json()["collections"]
        collections_to_use = st.multiselect(
            "Quelles collections voulez-vous utiliser?",
            collections.keys(),
            format_func=lambda x: collections.get(x).get("name"),
            key="collections_to_use",
        )
        topic_of_interest = st.text_input(
            "Sujet particulier du document à mettre en lumière",
            value="",
            help="Vous pouvez ajouter un sujet particulier du document sur lequel Albert devrait se concentrer",
            key="topic_of_interest",
        )
        ask_for_document_summary_button = st.form_submit_button(
            "Valider",
            # on_click=set_stage, args=(2,)
        )
        if ask_for_document_summary_button:
            data = {
                "document_url": document_url,
                "collections_to_use": collections_to_use,
                "topic_of_interest": topic_of_interest,
            }
            if debug_st:
                with st.expander("See request"):
                    st.write("Request:")
                    st.write(data)
            response = requests.post(
                url=f"{backend_url}/summary/",
                data=json.dumps(data),
                headers={"Content-Type": "application/json"},
            )
            with st.container():
                st.write("Response:")
                st.write(response.json())
