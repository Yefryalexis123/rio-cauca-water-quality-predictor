# 💧 Predictor de Calidad del Agua – Río Cauca

## Descripción

Aplicación web de Machine Learning que predice la **calidad del agua del Río Cauca** (`Buena`, `Regular` o `Mala`) a partir de variables fisicoquímicas medidas en estaciones de monitoreo a lo largo del río. El modelo utiliza **Random Forest** entrenado con datos reales del Sistema de Información Ambiental de Colombia (SIAC).

La clasificación se basa en el nivel de oxígeno disuelto del agua: valores ≥ 5 mg O₂/l se clasifican como *Buena*, entre 3 y 5 como *Regular*, y < 3 como *Mala*.

## 🌐 Demostración

> **Aplicación desplegada:** [https://rio-cauca-water-quality-predictor.streamlit.app](https://rio-cauca-water-quality-predictor.streamlit.app)
>
> **Repositorio GitHub:** [https://github.com/Yefryalexis123/rio-cauca-water-quality-predictor](https://github.com/Yefryalexis123/rio-cauca-water-quality-predictor)

## 🤖 Algoritmo utilizado

**Random Forest Classifier** (scikit-learn)

Random Forest es un algoritmo de aprendizaje por conjuntos (*ensemble learning*) que construye múltiples árboles de decisión durante el entrenamiento y emite como resultado la moda de las clases predichas por cada árbol individual. Es apropiado para este problema porque:

- Maneja bien datos con valores faltantes y variables de diferente escala.
- Es robusto frente al sobreajuste gracias al promediado de múltiples árboles.
- Proporciona importancia de características (*feature importance*), útil para seleccionar las 15 variables más relevantes de las 32 disponibles.
- Funciona bien con problemas de clasificación multiclase (Buena / Regular / Mala).

### Métricas de desempeño

| Clase    | Precisión | Recall | F1-Score | Soporte |
|----------|-----------|--------|----------|---------|
| Buena    | 0.77      | 0.86   | 0.81     | 156     |
| Mala     | 0.75      | 0.82   | 0.78     | 159     |
| Regular  | 0.58      | 0.43   | 0.50     | 125     |
| **Accuracy** | | | **0.72** | **440** |
| Macro avg| 0.70      | 0.70   | 0.70     | 440     |
| Weighted avg | 0.71  | 0.72   | 0.71     | 440     |

> Accuracy del **72.27%** sobre el conjunto de prueba (split 80/20, `random_state=42`).

## 📊 Dataset

- **Fuente:** [Datos Abiertos Colombia – Calidad del agua del Río Cauca](https://www.datos.gov.co)
- **Registros:** 2 368 muestras recolectadas desde 1990 hasta 2026
- **Features originales:** 56 columnas (variables fisicoquímicas y metadatos)
- **Features utilizadas (modelo final):** 15 variables seleccionadas por importancia de Random Forest

Las 15 variables seleccionadas son:

| Variable | Unidad |
|---|---|
| Conductividad eléctrica | µS/cm |
| Alcalinidad total | mg CaCO₃/l |
| Bicarbonatos | mg CaCO₃/l |
| Demanda bioquímica de oxígeno (DBO) | mg O₂/l |
| Cloruros | mg Cl/l |
| Dureza cálcica | mg CaCO₃/l |
| Sodio total | mg Na/l |
| Dureza total | mg CaCO₃/l |
| Calcio | mg Ca/l |
| Turbiedad | UNT |
| Sulfatos | mg SO₄/l |
| Nitratos | mg N-NO₃/l |
| pH | – |
| Sólidos suspendidos totales | mg SS/l |
| Sólidos totales | mg SST/l |

## 🏗️ Estructura del proyecto

```
rio-cauca-water-quality-predictor/
│
├── README.md                         # Documentación principal
├── requirements.txt                  # Dependencias Python
├── .gitignore                        # Archivos ignorados por Git
│
├── data/
│   └── raw/
│       └── Calidad_del_agua_del_Rio_Cauca_20260530.csv   # Dataset original
│
├── notebooks/
│   └── 01_training_optimized.ipynb   # Notebook de entrenamiento y evaluación
│
├── models/
│   └── water_quality_pipeline.joblib # Pipeline (imputer + RF) serializado
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py              # Definición de features y creación del DataFrame
│   └── predict.py                    # Carga del modelo y función de predicción
│
└── app/
    └── app.py                        # Aplicación Streamlit
```

## ⚙️ Instalación local

### Requisitos previos

- Python 3.11+
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/Yefryalexis123/rio-cauca-water-quality-predictor.git
cd rio-cauca-water-quality-predictor

# 2. (Opcional) Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
streamlit run app/app.py
```

La aplicación estará disponible en `http://localhost:8501`.

## 🚀 Uso de la aplicación

1. Acceder a la URL pública de la aplicación (o ejecutarla localmente).
2. Ingresar los valores de las 15 variables fisicoquímicas medidas en la estación de monitoreo.
3. Presionar el botón **Predecir**.
4. La aplicación mostrará el resultado:
   - ✅ **Buena** – agua apta para la mayoría de usos.
   - ⚠️ **Regular** – calidad limitada, requiere tratamiento.
   - ❌ **Mala** – agua con niveles críticos de contaminación.

## ☁️ Despliegue

La aplicación está desplegada en **Streamlit Community Cloud**, conectado directamente al repositorio de GitHub. Cualquier `push` a la rama `main` desencadena un redespliegue automático.

**Pasos seguidos:**
1. Subir código a GitHub (repositorio público).
2. Conectar el repositorio en [https://streamlit.io/cloud](https://streamlit.io/cloud).
3. Configurar el archivo de entrada como `app/app.py`.
4. Desplegar con un clic.

## 👥 Autores

| Nombre | Rol |
|---|---|
| Juan Fernando Bueno Torres | Entrenamiento del modelo y análisis exploratorio |
| Yefry Alexis Muñetón Córdoba | Desarrollo de la aplicación web y despliegue |
| Jonathan Pedroza Bernal | Preprocesamiento de datos y documentación |

**Grupo 6 – Inteligencia Artificial I**
Fundación Universitaria Los Libertadores

## 📄 Licencia

MIT License

## 📚 Referencias

- Datos Abiertos Colombia. *Calidad del agua del Río Cauca*. https://www.datos.gov.co
- Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324
- Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR*, 12, 2825–2830. http://jmlr.org/papers/v12/pedregosa11a.html
- Streamlit Inc. (2024). *Streamlit Documentation*. https://docs.streamlit.io
- Streamlit Community Cloud. *Deploy your app*. https://docs.streamlit.io/streamlit-community-cloud
