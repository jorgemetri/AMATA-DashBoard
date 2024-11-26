import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards

st.header("Modelo Tora 🤖📊")
st.divider()
st.header("Resultado do Modelo")
@st.cache_data
def load_data():
    data = pd.read_csv(r"Modelos\tora-model4\train\results.csv")
    return data

def Metricas(data):
    col1, col2, col3 = st.columns(3)

    col1.metric(label="metrics/precision(B)", value=f"{round(np.average(data["metrics/precision(B)"]),2)}%", delta=9)
    col2.metric(label="metrics/recall(B)", value=f"{round(np.average(data["metrics/recall(B)"]),2)}%", delta=2)
    col3.metric(label="metrics/mAP50-95(B)", value=f"{round(np.average(data["metrics/mAP50-95(B)"]),2)}%", delta=4)

    style_metric_cards(border_left_color="#145550")

data = load_data()
Metricas(data)

def Graficos(data):

    st.line_chart(data["metrics/mAP50-95(B)"])
    st.line_chart(data["metrics/mAP50-95(B)"])
    st.line_chart(data["metrics/mAP50-95(B)"])
def images():
    st.image(r"Modelos\tora-model4\val\val_batch0_labels.jpg")
    st.image(r"Modelos\tora-model4\val\val_batch0_pred.jpg")

Graficos(data)
images()