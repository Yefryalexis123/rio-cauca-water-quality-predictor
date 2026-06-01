# Predicción de Calidad del Agua — Río Cauca

## Descripción

Aplicación web de Machine Learning que predice la **calidad del agua del Río Cauca** (`Buena`, `Regular` o `Mala`) a partir de variables fisicoquímicas medidas en estaciones de monitoreo a lo largo del río. El modelo utiliza **Random Forest** entrenado con datos reales del portal de Datos Abiertos Colombia.

La clasificación se basa en el nivel de oxígeno disuelto del agua: valores mayores o iguales a 5 mg O2/l se clasifican como *Buena*, entre 3 y 5 como *Regular*, y menores a 3 como *Mala*.

---

## Demostración

**Aplicación desplegada:** [https://rio-cauca-water-quality-predictor-6rtfvyxdq7k4wkqryawjn6.streamlit.app](https://rio-cauca-water-quality-predictor-6rtfvyxdq7k4wkqryawjn6.streamlit.app)

**Repositorio GitHub:** [https://github.com/Yefryalexis123/rio-cauca-water-quality-predictor](https://github.com/Yefryalexis123/rio-cauca-water-quality-predictor)

---

## Algoritmo utilizado

**Random Forest Classifier** (scikit-learn)

Random Forest es un algoritmo de aprendizaje por conjuntos (*ensemble learning*) que construye múltiples árboles de decisión durante el entrenamiento y emite como resultado la moda de las clases predichas por cada árbol individual. Es apropiado para este problema porque:

- Maneja bien datos con valores faltantes y variables de diferente escala.
- Es robusto frente al sobreajuste gracias al promediado de múltiples árboles.
- Proporciona importancia de características (*feature importance*), útil para seleccionar las 15 variables más relevantes de las 56 disponibles.
- Funciona bien con problemas de clasificación multiclase (Buena / Regular / Mala).

### Métricas de desempeño

| Clase        | Precisión | Recall | F1-Score | Soporte |
|--------------|-----------|--------|----------|---------:|
| Buena        | 0.96      | 0.98   | 0.97     | 173     |
| Mala         | 0.95      | 0.93   | 0.94     | 141     |
| Regular      | 0.94      | 0.94   | 0.94     | 126     |
| **Accuracy** |           |        | **0.95** | **440** |
| Macro avg    | 0.95      | 0.95   | 0.95     | 440     |
| Weighted avg | 0.95      | 0.95   | 0.95     | 440     |

Accuracy del **95.0%** sobre el conjunto de prueba (split 80/20, `random_state=42`).

---

## Dataset

- **Fuente:** [Data Histórica de Calidad de Agua — Datos Abiertos Colombia](https://www.datos.gov.co/Ambiente-y-Desarrollo-Sostenible/Data-Hist-rica-de-Calidad-de-Agua/62gv-3857/about_data)
- **Registros:** 2.368 muestras recolectadas desde 1990 hasta 2026
- **Features originales:** 56 columnas (variables fisicoquímicas y metadatos)
- **Features utilizadas (modelo final):** 15 variables seleccionadas por importancia de Random Forest

Las 15 variables seleccionadas son:

| Variable                              | Unidad       |
|---------------------------------------|--------------|
| Conductividad eléctrica               | µS/cm        |
| Alcalinidad total                     | mg CaCO3/l   |
| Bicarbonatos                          | mg CaCO3/l   |
| Demanda bioquímica de oxígeno (DBO)   | mg O2/l      |
| Cloruros                              | mg Cl/l      |
| Dureza cálcica                        | mg CaCO3/l   |
| Sodio total                           | mg Na/l      |
| Dureza total                          | mg CaCO3/l   |
| Calcio                                | mg Ca/l      |
| Turbiedad                             | UNT          |
| Sulfatos                              | mg SO4/l     |
| Nitratos                              | mg N-NO3/l   |
| pH                                    | —            |
| Sólidos suspendidos totales           | mg SS/l      |
| Sólidos totales                       | mg SST/l     |

---

## Estructura del proyecto

```
rio-cauca-water-quality-predictor/
│
├── README.md                         # Documentación principal
├── requirements.txt                  # Dependencias Python
├── .gitignore                        # Archivos ignorados por Git
│
├── data/
│   └── raw/
│       └── Calidad_del_agua_del_Rio_Cauca_20260530.csv
│
├── notebooks/
│   └── 01_training_optimized.ipynb   # Notebook de entrenamiento y evaluación
│
├── models/
│   └── water_quality_pipeline.joblib # Pipeline serializado (Imputer + Random Forest)
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py              # Definición de features y creación del DataFrame
│   └── predict.py                    # Carga del modelo y función de predicción
│
├── app/
│   └── app.py                        # Aplicación Streamlit
│
└── docs/
    ├── captura_inicio.png            # Captura del estado inicial de la app
    └── captura_resultado.png         # Captura con resultado de clasificación
```

---

## Instalación local

### Requisitos previos

- Python 3.11 o superior
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/Yefryalexis123/rio-cauca-water-quality-predictor.git
cd rio-cauca-water-quality-predictor

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la aplicación
python -m streamlit run app/app.py
```

La aplicación estará disponible en `http://localhost:8501`.

---

## Uso de la aplicación

1. Acceder a la URL pública de la aplicación o ejecutarla localmente.
2. Ingresar los valores de las 15 variables fisicoquímicas medidas en la estación de monitoreo.
3. Presionar el botón **Clasificar calidad del agua**.
4. La aplicación mostrará el resultado: **Buena**, **Regular** o **Mala**, según la calidad detectada.

---

## Despliegue

La aplicación está desplegada en **Streamlit Community Cloud**, conectado directamente al repositorio de GitHub. Cualquier `push` a la rama `main` desencadena un redespliegue automático.

Pasos seguidos:

1. Subir el código a GitHub (repositorio público).
2. Conectar el repositorio en [https://streamlit.io/cloud](https://streamlit.io/cloud).
3. Configurar el archivo de entrada como `app/app.py`.
4. Desplegar con un clic.

---

## Autores

| Nombre                        | Rol                                               |
|-------------------------------|---------------------------------------------------|
| Juan Fernando Bueno Torres    | Entrenamiento del modelo y análisis exploratorio  |
| Yefry Alexis Muñetón Córdoba  | Desarrollo de la aplicación web y despliegue      |
| Jonathan Pedroza Bernal       | Preprocesamiento de datos y documentación         |

**Grupo 6 — Inteligencia Artificial I**
Fundación Universitaria Los Libertadores

---

## Licencia

MIT License

---

## Referencias

- Datos Abiertos Colombia. *Data Histórica de Calidad de Agua*. [En línea]. Disponible en: https://www.datos.gov.co/Ambiente-y-Desarrollo-Sostenible/Data-Hist-rica-de-Calidad-de-Agua/62gv-3857/about_data. [Accedido: mayo 2026].
- L. Breiman, «Random Forests,» *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001. https://doi.org/10.1023/A:1010933404324
- F. Pedregosa et al., «Scikit-learn: Machine Learning in Python,» *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, 2011. http://jmlr.org/papers/v12/pedregosa11a.html
- Streamlit Inc., *Streamlit Documentation*, 2024. [En línea]. Disponible en: https://docs.streamlit.io. [Accedido: mayo 2026].
