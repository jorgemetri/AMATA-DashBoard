import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards


st.header("Modelo Baliza Baliza 📊")
st.divider()
st.header("Resultado do Modelo")
@st.cache_data
def load_data():
    data = pd.read_csv("Modelos/baliza-model/train/results.csv")
    return data
@st.cache_data
def Metricas(data):
    col1, col2, col3 = st.columns(3)

    col1.metric(label="metrics/precision(B)", value=f"{round(np.average(data['metrics/precision(B)']), 2)}%", delta=9)
    col2.metric(label="metrics/recall(B)", value=f"{round(np.average(data['metrics/recall(B)']), 2)}%", delta=2)
    col3.metric(label="metrics/mAP50-95(B)", value=f"{round(np.average(data['metrics/mAP50-95(B)']), 2)}%", delta=4)

    style_metric_cards(background_color="#262730",border_left_color="#FFFFF",border_color="black")



def Grafico_Rotulo(data, x_column, y_column, titulo):
    hover = alt.selection_single(
        fields=[x_column],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    # Linha principal
    lines = (
        alt.Chart(data, title=titulo)
        .mark_line()
        .encode(
            x=alt.X(x_column, title=x_column),
            y=alt.Y(y_column, title=y_column)
        )
    )

    # Pontos nos valores mais próximos
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Regras e tooltips
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x=alt.X(x_column, title=x_column),
            y=alt.Y(y_column, title=y_column),
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip(x_column, title=x_column),
                alt.Tooltip(y_column, title=y_column),
            ],
        )
        .add_selection(hover)
    )

    # Camada combinada do gráfico
    data_layer = lines + points + tooltips
    combined_chart = data_layer
    st.altair_chart(combined_chart, use_container_width=True)

def images():
    st.image("Modelos/baliza-model/val/val_batch0_labels.jpg")
    st.image("Modelos/baliza-model/val/val_batch0_pred.jpg")


data = load_data()
Metricas(data)


# Chamar a função com os dados adequados
Grafico_Rotulo(data, "epoch", "metrics/precision(B)", "metrics/precision(B)")
Grafico_Rotulo(data, "epoch", "metrics/recall(B)", "metrics/recall(B)")
Grafico_Rotulo(data, "epoch", "metrics/mAP50-95(B)", "metrics/mAP50-95(B)")
images()
