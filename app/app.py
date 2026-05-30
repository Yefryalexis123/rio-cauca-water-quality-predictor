import streamlit as st

from src.preprocessing import (
    FEATURE_COLUMNS,
    create_input_dataframe
)

from src.predict import predict_water_quality

st.set_page_config(
    page_title="Predicción Calidad del Agua",
    page_icon="💧"
)

st.title("💧 Predicción de Calidad del Agua")

st.write(
    """
    Sistema basado en Random Forest para clasificar
    la calidad del agua en:

    - Buena
    - Regular
    - Mala
    """
)

datos = {}

col1, col2 = st.columns(2)

for i, variable in enumerate(FEATURE_COLUMNS):

    if i % 2 == 0:
        datos[variable] = col1.number_input(
            variable,
            value=0.0
        )
    else:
        datos[variable] = col2.number_input(
            variable,
            value=0.0
        )

if st.button("Predecir"):

    df_input = create_input_dataframe(datos)

    resultado = predict_water_quality(df_input)

    st.success(
        f"Calidad estimada del agua: {resultado}"
    )