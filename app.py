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


baliza1 = st.Page("Modelos/baliza-model1.py",title="Modelo1",icon=":material/dashboard:")
modelo1 =  st.Page("Modelos/tora-model1.py",title="Modelo 1",icon=":material/dashboard:")
modelo2 =  st.Page("Modelos/tora-model2.py",title="Modelo 2",icon=":material/dashboard:")
modelo3 =  st.Page("Modelos/tora-model3.py",title="Modelo 3",icon=":material/dashboard:")
aplication = st.Page("Aplication/aplication.py",title="Aplicação",icon=":material/dashboard:")


LOGO_URL_LARGE="images/samarco.png"
#Logo(LOGO_URL_LARGE)


pg = st.navigation(
    {
        "Aplicação":[aplication],
        "Modelos Tora":[modelo1,modelo2,modelo3],
        "Modelos Baliza":[baliza1]
    }
)
pg.run()