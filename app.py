import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import string
import time
#Definindo função para pegar dados

#Definindo as pages
def Logo(url):
    st.logo(
        url,
        link="https://streamlit.io/gallery",size="large"
    )

custom_css = """
<style>
/* Altera a cor dos títulos na sidebar */
[data-testid="stSidebar"] .css-qrbaxs p {
    color: #FF6347; /* Define a cor para o texto dos títulos */
    font-weight: bold; /* Opcional: deixa o texto em negrito */
    font-size: 18px; /* Opcional: ajusta o tamanho da fonte */
}
</style>
"""

# Aplica o CSS ao Streamlit
st.markdown(custom_css, unsafe_allow_html=True)

baliza1 = st.Page("Modelos/baliza-model1.py",title="Modelo Baliza",icon=":material/dashboard:")
modelo1 =  st.Page("Modelos/tora-model4.py",title="Modelo Tora",icon=":material/dashboard:")
aplication = st.Page("Aplication/aplication.py",title="Aplicação",icon=":material/dashboard:")


LOGO_URL_LARGE="images/samarco.png"
#Logo(LOGO_URL_LARGE)


pg = st.navigation(
    {
        "Aplicação":[aplication],
        "Modelos Tora":[modelo1],
        "Modelos Baliza":[baliza1]
    }
)
pg.run()