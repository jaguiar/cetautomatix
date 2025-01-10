import streamlit as st

from dotenv import load_dotenv
import os

load_dotenv()


# Inspired by an example app from streamlit app galery : https://knowledgegpt.streamlit.app/
def sidebar():
    with st.sidebar:
        st.markdown(
            "## \n"
            "1. Entrez votre [clef d'accès à l'API Albert](https://github.com/etalab-ia/albert-api/)🔑\n"
            "2. Référencez un document en ligne📄\n"
            "3. Demandez un résumé du document en question, en utilisant les collections d'Albert à utiliser💬\n"
        )
        api_key_input = st.text_input(
            "Albert API Key",
            type="password",
            placeholder="Entrez votre clef d'API ici",
            help="vous pouvez obtenir une clef en demandant à [Etalab](https://etalab.gouv.fr).",
            value=os.environ.get("ALBERT_API_KEY", None) or st.session_state.get("ALBERT_API_KEY", ""),
        )

        st.session_state["ALBERT_API_KEY"] = api_key_input
