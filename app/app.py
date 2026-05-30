import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st
from src.preprocessing import FEATURE_COLUMNS, create_input_dataframe
from src.predict import predict_water_quality

# ── Configuración de página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Calidad del Agua - Rio Cauca",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp { background: #F0F7FF; }

/* ── Hero ── */
.hero-header {
    background: linear-gradient(135deg, #0A2540 0%, #1A4A7A 60%, #1B6FBF 100%);
    border-radius: 16px;
    padding: 2.2rem 2rem 1.8rem;
    margin-bottom: 1.8rem;
}
.hero-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    font-weight: 400;
    margin: 0 0 0.3rem;
    color: white !important;
}
.hero-header p { font-size: 0.95rem; color: #FFFFFF !important; margin: 0; text-shadow: 0 1px 3px rgba(0,0,0,0.5); font-weight: 500; }
.badge-algo {
    display: inline-block;
    background: rgba(14,165,233,0.20);
    border: 1px solid rgba(14,165,233,0.45);
    color: #7DD3FC;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.07em;
    padding: 3px 11px;
    border-radius: 20px;
    margin-bottom: 0.8rem;
    text-transform: uppercase;
}

/* ── Métricas ── */
.metrics-row {
    display: flex;
    gap: 10px;
    margin-bottom: 1.8rem;
    flex-wrap: wrap;
}
.metric-card {
    background: #FFFFFF;
    border: 1px solid #C8DDEF;
    border-radius: 12px;
    padding: 0.9rem 1.2rem;
    flex: 1;
    min-width: 110px;
    text-align: center;
}
.metric-card .m-label {
    font-size: 0.70rem;
    color: #5A7A9A;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 3px;
}
.metric-card .m-value {
    font-family: 'DM Serif Display', serif;
    font-size: 1.55rem;
    color: #1B6FBF;
}
.metric-card .m-sub { font-size: 0.68rem; color: #5A7A9A; }

/* ── Título de sección ── */
.section-title {
    font-size: 0.72rem;
    font-weight: 600;
    color: #0A2540;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    border-bottom: 1px solid #C8DDEF;
    padding-bottom: 0.4rem;
    margin-bottom: 0.9rem;
}

/* ── Labels del formulario ── */
label,
.stNumberInput label,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] {
    color: #0A2540 !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
}

/* ── Textos generales en modo oscuro ── */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] td,
[data-testid="stMarkdownContainer"] th {
    color: #1A3A5C !important;
}

/* ── Tabla de referencia ── */
.ref-table {
    background: #FFFFFF;
    border: 1px solid #C8DDEF;
    border-radius: 10px;
    padding: 0.9rem 1rem;
    margin-bottom: 1rem;
    font-size: 0.82rem;
    color: #0A2540;
}
.ref-table table { width: 100%; border-collapse: collapse; }
.ref-table th {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #5A7A9A;
    border-bottom: 1px solid #C8DDEF;
    padding: 4px 6px;
    text-align: left;
}
.ref-table td { padding: 4px 6px; color: #0A2540; }
.ref-table tr:nth-child(even) td { background: #F0F7FF; }

/* ── Resultado ── */
.result-box {
    border-radius: 14px;
    padding: 1.6rem 1.2rem;
    text-align: center;
    margin-bottom: 1rem;
}
.result-buena   { background: #E8F9EF; border: 1.5px solid #1DB954; }
.result-regular { background: #FFF8E1; border: 1.5px solid #F5A623; }
.result-mala    { background: #FEF0F0; border: 1.5px solid #E84040; }
.result-icon { font-size: 2.6rem; margin-bottom: 0.4rem; }
.result-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.7rem;
    margin: 0 0 0.3rem;
}
.result-buena   .result-title { color: #0A7030; }
.result-regular .result-title { color: #7A5500; }
.result-mala    .result-title { color: #B82020; }
.result-desc { font-size: 0.88rem; color: #333; margin: 0; }

/* ── Info cards ── */
.info-card {
    background: #FFFFFF;
    border: 1px solid #C8DDEF;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.7rem;
    font-size: 0.83rem;
    color: #1A3A5C;
}
.info-card strong {
    color: #1A4A7A;
    display: block;
    margin-bottom: 3px;
    font-size: 0.80rem;
}

/* ── Botón ── */
.stButton > button {
    background: #1B6FBF !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
    opacity: 1 !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stButton > button p,
.stButton > button span {
    color: #FFFFFF !important;
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="badge-algo">Random Forest · Clasificación multiclase</div>
    <h1>Predicción de Calidad del Agua — Río Cauca</h1>
    <span style="font-size:0.95rem; color:#FFFFFF !important; font-weight:500; display:block; margin-top:0.3rem;">Ingrese los parámetros fisicoquímicos medidos en el río y el modelo clasificará la calidad del agua como Buena, Regular o Mala.</span>
</div>
""", unsafe_allow_html=True)


# ── Métricas ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="metrics-row">
    <div class="metric-card">
        <div class="m-label">Accuracy</div>
        <div class="m-value">95.0%</div>
        <div class="m-sub">en conjunto de prueba</div>
    </div>
    <div class="metric-card">
        <div class="m-label">Precisión</div>
        <div class="m-value">95.0%</div>
        <div class="m-sub">ponderada</div>
    </div>
    <div class="metric-card">
        <div class="m-label">Recall</div>
        <div class="m-value">95.0%</div>
        <div class="m-sub">ponderado</div>
    </div>
    <div class="metric-card">
        <div class="m-label">F1-Score</div>
        <div class="m-value">95.0%</div>
        <div class="m-sub">ponderado</div>
    </div>
    <div class="metric-card">
        <div class="m-label">Registros</div>
        <div class="m-value">2.199</div>
        <div class="m-sub">válidos para entrenamiento</div>
    </div>
    <div class="metric-card">
        <div class="m-label">Árboles</div>
        <div class="m-value">200</div>
        <div class="m-sub">n_estimators</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Layout principal ──────────────────────────────────────────────────────────
col_form, col_result = st.columns([1.3, 1], gap="large")

with col_form:
    st.markdown('<div class="section-title">Parámetros fisicoquímicos</div>',
                unsafe_allow_html=True)

    defaults = {
        'CONDUCTIVIDAD ELÉCTRICA (µS/cm)':         122.50,
        'ALCALINIDAD TOTAL (mg CaCO3/l)':            46.00,
        'BICARBONATOS (mg CaCO3/l)':                 56.00,
        'DEMANDA BIOQUIMICA DE OXIGENO (mg O2/l)':    3.16,
        'CLORUROS (mg Cl/l)':                         5.00,
        'DUREZA CALCICA (mg CaCO3/l)':               28.00,
        'SODIO TOTAL (mg Na/l)':                     11.00,
        'DUREZA TOTAL (mg CaCO3/l)':                 48.00,
        'CALCIO (mg Ca/l)':                          11.20,
        'TURBIEDAD (UNT)':                           85.00,
        'SULFATOS (mg SO4/l)':                       10.00,
        'NITRATOS (mg N-NO3/l)':                      0.50,
        'pH':                                         7.07,
        'SOLIDOS SUSPENDIDOS TOTALES (mg SS/l)':     80.00,
        'SOLIDOS TOTALES (mg SST/l)':               180.00,
    }

    labels = {
        'CONDUCTIVIDAD ELÉCTRICA (µS/cm)':         'Conductividad eléctrica (µS/cm)',
        'ALCALINIDAD TOTAL (mg CaCO3/l)':           'Alcalinidad total (mg CaCO3/l)',
        'BICARBONATOS (mg CaCO3/l)':                'Bicarbonatos (mg CaCO3/l)',
        'DEMANDA BIOQUIMICA DE OXIGENO (mg O2/l)':  'DBO — Demanda bioquímica de oxígeno (mg O2/l)',
        'CLORUROS (mg Cl/l)':                       'Cloruros (mg Cl/l)',
        'DUREZA CALCICA (mg CaCO3/l)':              'Dureza cálcica (mg CaCO3/l)',
        'SODIO TOTAL (mg Na/l)':                    'Sodio total (mg Na/l)',
        'DUREZA TOTAL (mg CaCO3/l)':                'Dureza total (mg CaCO3/l)',
        'CALCIO (mg Ca/l)':                         'Calcio (mg Ca/l)',
        'TURBIEDAD (UNT)':                          'Turbiedad (UNT)',
        'SULFATOS (mg SO4/l)':                      'Sulfatos (mg SO4/l)',
        'NITRATOS (mg N-NO3/l)':                    'Nitratos (mg N-NO3/l)',
        'pH':                                       'pH',
        'SOLIDOS SUSPENDIDOS TOTALES (mg SS/l)':    'Sólidos suspendidos totales (mg SS/l)',
        'SOLIDOS TOTALES (mg SST/l)':               'Sólidos totales (mg SST/l)',
    }

    datos = {}
    cols_izq = list(FEATURE_COLUMNS[:8])
    cols_der = list(FEATURE_COLUMNS[8:])

    c1, c2 = st.columns(2)
    with c1:
        for var in cols_izq:
            datos[var] = st.number_input(
                labels[var],
                value=defaults[var],
                min_value=0.0,
                format="%.2f"
            )
    with c2:
        for var in cols_der:
            datos[var] = st.number_input(
                labels[var],
                value=defaults[var],
                min_value=0.0,
                format="%.2f"
            )

    st.markdown("<br>", unsafe_allow_html=True)
    predecir = st.button("Clasificar calidad del agua")


# ── Resultado ─────────────────────────────────────────────────────────────────
with col_result:
    st.markdown('<div class="section-title">Resultado de la clasificación</div>',
                unsafe_allow_html=True)

    if predecir:
        df_input = create_input_dataframe(datos)
        resultado = predict_water_quality(df_input)

        if resultado == "Buena":
            st.markdown("""
            <div class="result-box result-buena">
                <div class="result-icon">+</div>
                <div class="result-title">Calidad Buena</div>
                <p class="result-desc">El agua presenta condiciones fisicoquímicas
                adecuadas para los usos establecidos.</p>
            </div>
            """, unsafe_allow_html=True)
        elif resultado == "Regular":
            st.markdown("""
            <div class="result-box result-regular">
                <div class="result-icon">~</div>
                <div class="result-title">Calidad Regular</div>
                <p class="result-desc">El agua presenta alteraciones moderadas.
                Se recomienda tratamiento antes de su uso.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-box result-mala">
                <div class="result-icon">-</div>
                <div class="result-title">Calidad Mala</div>
                <p class="result-desc">El agua presenta contaminación significativa.
                No es apta para consumo sin tratamiento previo.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Resumen de parámetros ingresados:**")
        st.markdown(f"""
| Parámetro | Valor |
|---|---|
| pH | {datos['pH']:.2f} |
| Turbiedad | {datos['TURBIEDAD (UNT)']:.2f} UNT |
| Conductividad | {datos['CONDUCTIVIDAD ELÉCTRICA (µS/cm)']:.2f} µS/cm |
| DBO | {datos['DEMANDA BIOQUIMICA DE OXIGENO (mg O2/l)']:.2f} mg O2/l |
| Sólidos totales | {datos['SOLIDOS TOTALES (mg SST/l)']:.2f} mg/l |
""")

    else:
        st.info("Complete el formulario y presione **Clasificar calidad del agua** para ver el resultado.")

        st.markdown("""
        <div class="ref-table">
            <strong style="font-size:0.78rem; color:#1A4A7A; display:block; margin-bottom:8px;">
                Valores de referencia por clase (medianas del dataset)
            </strong>
            <table>
                <tr>
                    <th>Parámetro</th>
                    <th style="color:#0A7030">Buena</th>
                    <th style="color:#7A5500">Regular</th>
                    <th style="color:#B82020">Mala</th>
                </tr>
                <tr><td>pH</td><td>7.08</td><td>7.07</td><td>7.05</td></tr>
                <tr><td>Turbiedad (UNT)</td><td>60.50</td><td>85.00</td><td>60.00</td></tr>
                <tr><td>DBO (mg O2/l)</td><td>2.10</td><td>3.16</td><td>4.36</td></tr>
                <tr><td>Conductividad (µS/cm)</td><td>85.00</td><td>122.50</td><td>152.00</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card">
            <strong>Dataset</strong>
            Data Histórica de Calidad del Agua — Datos Abiertos Colombia<br>
            2.368 registros · 56 variables · 15 características seleccionadas
        </div>
        <div class="info-card">
            <strong>Algoritmo</strong>
            Random Forest Classifier<br>
            200 árboles · SimpleImputer (mediana) · random_state=42
        </div>
        <div class="info-card">
            <strong>Variable objetivo</strong>
            Clasificación basada en Oxígeno Disuelto:<br>
            Buena (&ge; 5 mg/l) &nbsp;·&nbsp; Regular (3–5 mg/l) &nbsp;·&nbsp; Mala (&lt; 3 mg/l)
        </div>
        <div class="info-card">
            <strong>Grupo 6 · IA I</strong>
            Fundación Universitaria Los Libertadores<br>
            Juan Fernando · Yefry · Jonathan
        </div>
        """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#5A7A9A; font-size:0.78rem;'>"
    "Grupo 6 &nbsp;·&nbsp; Inteligencia Artificial I &nbsp;·&nbsp; "
    "Fundación Universitaria Los Libertadores &nbsp;·&nbsp; 2026 &nbsp;·&nbsp; "
    "Random Forest + Streamlit &nbsp;·&nbsp; Datos: datos.gov.co"
    "</p>",
    unsafe_allow_html=True
)
