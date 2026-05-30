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

# ── CSS personalizado ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --brand-dark:    #0A2540;
    --brand-mid:     #1A4A7A;
    --brand-accent:  #1B6FBF;
    --brand-water:   #0EA5E9;
    --surface:       #F0F7FF;
    --card-bg:       #FFFFFF;
    --text-main:     #0A2540;
    --text-muted:    #5A7A9A;
    --border:        #C8DDEF;
    --green:         #0A7030;
    --green-bg:      #E8F9EF;
    --green-border:  #1DB954;
    --yellow:        #7A5500;
    --yellow-bg:     #FFF8E1;
    --yellow-border: #F5A623;
    --red:           #B82020;
    --red-bg:        #FEF0F0;
    --red-border:    #E84040;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-main);
}

.stApp { background: var(--surface); }

/* Hero */
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
.hero-header p { font-size: 0.95rem; color: rgba(255,255,255,0.70); margin: 0; }
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

/* Métricas */
.metrics-row {
    display: flex;
    gap: 10px;
    margin-bottom: 1.8rem;
    flex-wrap: wrap;
}
.metric-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.9rem 1.2rem;
    flex: 1;
    min-width: 110px;
    text-align: center;
}
.metric-card .m-label {
    font-size: 0.70rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 3px;
}
.metric-card .m-value {
    font-family: 'DM Serif Display', serif;
    font-size: 1.55rem;
    color: var(--brand-accent);
}
.metric-card .m-sub { font-size: 0.68rem; color: var(--text-muted); }

/* Sección título */
.section-title {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.09em;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.4rem;
    margin-bottom: 0.9rem;
}

/* Referencia de valores */
.ref-table {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.9rem 1rem;
    margin-bottom: 1rem;
    font-size: 0.82rem;
}
.ref-table table { width: 100%; border-collapse: collapse; }
.ref-table th {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
    border-bottom: 1px solid var(--border);
    padding: 4px 6px;
    text-align: left;
}
.ref-table td { padding: 4px 6px; color: var(--text-main); }
.ref-table tr:nth-child(even) td { background: var(--surface); }
.dot-buena  { color: var(--green);  font-weight: 600; }
.dot-regular{ color: #8A6000; font-weight: 600; }
.dot-mala   { color: var(--red);   font-weight: 600; }

/* Resultado */
.result-box {
    border-radius: 14px;
    padding: 1.6rem 1.2rem;
    text-align: center;
    margin-bottom: 1rem;
}
.result-buena   { background: var(--green-bg);  border: 1.5px solid var(--green-border); }
.result-regular { background: var(--yellow-bg); border: 1.5px solid var(--yellow-border); }
.result-mala    { background: var(--red-bg);    border: 1.5px solid var(--red-border); }
.result-icon { font-size: 2.6rem; margin-bottom: 0.4rem; }
.result-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.7rem;
    margin: 0 0 0.3rem;
}
.result-buena   .result-title { color: var(--green); }
.result-regular .result-title { color: var(--yellow); }
.result-mala    .result-title { color: var(--red); }
.result-desc { font-size: 0.88rem; color: #555; margin: 0; }

/* Info cards */
.info-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.7rem;
    font-size: 0.83rem;
    color: #333;
}
.info-card strong { color: var(--brand-mid); display: block; margin-bottom: 2px; font-size: 0.80rem; }

/* Botón */
.stButton > button {
    background: var(--brand-accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

label { color: #cccccc !important; }
[data-testid="stMarkdownContainer"] p { color: #cccccc; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="badge-algo">Random Forest · Clasificacion multiclase</div>
    <h1>Prediccion de Calidad del Agua - Rio Cauca</h1>
    <p>Ingresa los parametros fisicoquimicos medidos en el rio y el modelo clasifica la calidad del agua como Buena, Regular o Mala.</p>
</div>
""", unsafe_allow_html=True)


# ── METRICAS DEL MODELO ───────────────────────────────────────────────────────
st.markdown("""
<div class="metrics-row">
    <div class="metric-card">
        <div class="m-label">Accuracy</div>
        <div class="m-value">95.0%</div>
        <div class="m-sub">en test set</div>
    </div>
    <div class="metric-card">
        <div class="m-label">Precision</div>
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
        <div class="m-label">Dataset</div>
        <div class="m-value">2.199</div>
        <div class="m-sub">registros validos</div>
    </div>
    <div class="metric-card">
        <div class="m-label">Arboles</div>
        <div class="m-value">200</div>
        <div class="m-sub">n_estimators</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── LAYOUT ────────────────────────────────────────────────────────────────────
col_form, col_result = st.columns([1.3, 1], gap="large")

with col_form:
    st.markdown('<div class="section-title">Parametros fisicoquimicos</div>', unsafe_allow_html=True)

    # Valores por defecto basados en medianas del dataset (clase Regular)
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

    # Etiquetas más amigables para mostrar
    labels = {
        'CONDUCTIVIDAD ELÉCTRICA (µS/cm)':         'Conductividad electrica (µS/cm)',
        'ALCALINIDAD TOTAL (mg CaCO3/l)':           'Alcalinidad total (mg CaCO3/l)',
        'BICARBONATOS (mg CaCO3/l)':                'Bicarbonatos (mg CaCO3/l)',
        'DEMANDA BIOQUIMICA DE OXIGENO (mg O2/l)':  'DBO - Demanda bioquimica oxigeno (mg O2/l)',
        'CLORUROS (mg Cl/l)':                       'Cloruros (mg Cl/l)',
        'DUREZA CALCICA (mg CaCO3/l)':              'Dureza calcica (mg CaCO3/l)',
        'SODIO TOTAL (mg Na/l)':                    'Sodio total (mg Na/l)',
        'DUREZA TOTAL (mg CaCO3/l)':                'Dureza total (mg CaCO3/l)',
        'CALCIO (mg Ca/l)':                         'Calcio (mg Ca/l)',
        'TURBIEDAD (UNT)':                          'Turbiedad (UNT)',
        'SULFATOS (mg SO4/l)':                      'Sulfatos (mg SO4/l)',
        'NITRATOS (mg N-NO3/l)':                    'Nitratos (mg N-NO3/l)',
        'pH':                                       'pH',
        'SOLIDOS SUSPENDIDOS TOTALES (mg SS/l)':    'Solidos suspendidos totales (mg SS/l)',
        'SOLIDOS TOTALES (mg SST/l)':               'Solidos totales (mg SST/l)',
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


# ── RESULTADO ─────────────────────────────────────────────────────────────────
with col_result:
    st.markdown('<div class="section-title">Resultado de la clasificacion</div>', unsafe_allow_html=True)

    if predecir:
        df_input = create_input_dataframe(datos)
        resultado = predict_water_quality(df_input)

        if resultado == "Buena":
            st.markdown("""
            <div class="result-box result-buena">
                <div class="result-icon">+</div>
                <div class="result-title">Calidad Buena</div>
                <p class="result-desc">El agua presenta condiciones fisicoquimicas adecuadas para los usos establecidos.</p>
            </div>
            """, unsafe_allow_html=True)
        elif resultado == "Regular":
            st.markdown("""
            <div class="result-box result-regular">
                <div class="result-icon">~</div>
                <div class="result-title">Calidad Regular</div>
                <p class="result-desc">El agua presenta alteraciones moderadas. Se recomienda tratamiento antes de su uso.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-box result-mala">
                <div class="result-icon">-</div>
                <div class="result-title">Calidad Mala</div>
                <p class="result-desc">El agua presenta contaminacion significativa. No apta para consumo sin tratamiento.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Resumen de parametros ingresados:**")
        st.markdown(f"""
| Parametro | Valor |
|---|---|
| pH | {datos['pH']:.2f} |
| Turbiedad | {datos['TURBIEDAD (UNT)']:.2f} UNT |
| Conductividad | {datos['CONDUCTIVIDAD ELÉCTRICA (µS/cm)']:.2f} µS/cm |
| DBO | {datos['DEMANDA BIOQUIMICA DE OXIGENO (mg O2/l)']:.2f} mg O2/l |
| Solidos totales | {datos['SOLIDOS TOTALES (mg SST/l)']:.2f} mg/l |
""")

    else:
        st.info("Complete el formulario y presione Clasificar calidad del agua para ver el resultado.")

        # Tabla de referencia de valores tipicos
        st.markdown("""
        <div class="ref-table">
            <strong style="font-size:0.78rem; color:#1A4A7A; display:block; margin-bottom:8px;">
                Valores de referencia por clase (medianas del dataset)
            </strong>
            <table>
                <tr>
                    <th>Parametro</th>
                    <th class="dot-buena">Buena</th>
                    <th class="dot-regular">Regular</th>
                    <th class="dot-mala">Mala</th>
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
            Data Historica Calidad del Agua - Datos Abiertos Colombia<br>
            2.368 registros · 56 variables · 15 features seleccionadas
        </div>
        <div class="info-card">
            <strong>Algoritmo</strong>
            Random Forest Classifier<br>
            200 arboles · SimpleImputer (mediana) · random_state=42
        </div>
        <div class="info-card">
            <strong>Variable objetivo</strong>
            Clasificacion basada en Oxigeno Disuelto:<br>
            Buena (&gt;= 5 mg/l) · Regular (3-5 mg/l) · Mala (&lt; 3 mg/l)
        </div>
        <div class="info-card">
            <strong>Grupo 6 · IA I</strong>
            Fundacion Universitaria Los Libertadores<br>
            Juan Fernando · Yefry · Jonathan
        </div>
        """, unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#6B7A9A; font-size:0.78rem;'>"
    "Grupo 6 · Inteligencia Artificial I · Fundacion Universitaria Los Libertadores · 2026 · "
    "Random Forest + Streamlit · Datos: datos.gov.co"
    "</p>",
    unsafe_allow_html=True
)
