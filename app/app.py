import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st

from src.preprocessing import (
    FEATURE_COLUMNS,
    create_input_dataframe
)

from src.predict import predict_water_quality

st.set_page_config(
    page_title="Predicción Calidad del Agua",
    page_icon="💧",
    layout="wide"
)

st.title("💧 Predicción de Calidad del Agua")

st.write(
    """
    Modelo Random Forest entrenado con datos de monitoreo
    del Río Cauca para clasificar la calidad del agua.
    """
)

datos = {}

col1, col2 = st.columns(2)

for i, variable in enumerate(FEATURE_COLUMNS):

    if i % 2 == 0:
        datos[variable] = col1.number_input(
            variable,
            value=0.0,
            format="%.4f"
        )
    else:
        datos[variable] = col2.number_input(
            variable,
            value=0.0,
            format="%.4f"
        )

if st.button("Predecir"):

    df_input = create_input_dataframe(datos)

    resultado = predict_water_quality(df_input)

    if resultado == "Buena":
        st.success(f"Calidad del agua: {resultado}")

    elif resultado == "Regular":
        st.warning(f"Calidad del agua: {resultado}")

    else:
        st.error(f"Calidad del agua: {resultado}")