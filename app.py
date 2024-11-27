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
        link="https://innovatechgestao.com.br/",size="large"
    )

st.set_page_config(layout="wide")
baliza1 = st.Page("Modelos/baliza-model1.py",title="Modelo Baliza",icon=":material/dashboard:")
modelo1 =  st.Page("Modelos/tora-model4.py",title="Modelo Tora",icon=":material/dashboard:")
aplication = st.Page("Aplication/aplication.py",title="Aplicação",icon=":material/dashboard:")


LOGO_URL_LARGE="log1.png"
Logo(LOGO_URL_LARGE)

pg = st.navigation(
    {
        "Aplicação":[aplication],
        "Modelos Tora":[modelo1],
        "Modelos Baliza":[baliza1]
    }
)
pg.run()