# Predictor de Calidad del Agua - Rio Cauca

## Descripcion

Aplicacion web de Machine Learning que predice la **calidad del agua del Rio Cauca** (`Buena`, `Regular` o `Mala`) a partir de variables fisicoquimicas medidas en estaciones de monitoreo a lo largo del rio. El modelo utiliza **Random Forest** entrenado con datos reales del Sistema de Informacion Ambiental de Colombia (SIAC).

La clasificacion se basa en el nivel de oxigeno disuelto del agua: valores mayores o iguales a 5 mg O2/l se clasifican como *Buena*, entre 3 y 5 como *Regular*, y menores a 3 como *Mala*.

## Demostracion

**Aplicacion desplegada:** [https://rio-cauca-water-quality-predictor.streamlit.app](https://rio-cauca-water-quality-predictor.streamlit.app)

**Repositorio GitHub:** [https://github.com/Yefryalexis123/rio-cauca-water-quality-predictor](https://github.com/Yefryalexis123/rio-cauca-water-quality-predictor)

## Algoritmo utilizado

**Random Forest Classifier** (scikit-learn)

Random Forest es un algoritmo de aprendizaje por conjuntos (*ensemble learning*) que construye multiples arboles de decision durante el entrenamiento y emite como resultado la moda de las clases predichas por cada arbol individual. Es apropiado para este problema porque:

- Maneja bien datos con valores faltantes y variables de diferente escala.
- Es robusto frente al sobreajuste gracias al promediado de multiples arboles.
- Proporciona importancia de caracteristicas (*feature importance*), util para seleccionar las 15 variables mas relevantes de las 32 disponibles.
- Funciona bien con problemas de clasificacion multiclase (Buena / Regular / Mala).

### Metricas de desempeno

| Clase        | Precision | Recall | F1-Score | Soporte |
|--------------|-----------|--------|----------|---------|
| Buena        | 0.77      | 0.86   | 0.81     | 156     |
| Mala         | 0.75      | 0.82   | 0.78     | 159     |
| Regular      | 0.58      | 0.43   | 0.50     | 125     |
| **Accuracy** |           |        | **0.72** | **440** |
| Macro avg    | 0.70      | 0.70   | 0.70     | 440     |
| Weighted avg | 0.71      | 0.72   | 0.71     | 440     |

Accuracy del **72.27%** sobre el conjunto de prueba (split 80/20, `random_state=42`).

## Dataset

- **Fuente:** [Datos Abiertos Colombia - Calidad del agua del Rio Cauca](https://www.datos.gov.co)
- **Registros:** 2368 muestras recolectadas desde 1990 hasta 2026
- **Features originales:** 56 columnas (variables fisicoquimicas y metadatos)
- **Features utilizadas (modelo final):** 15 variables seleccionadas por importancia de Random Forest

Las 15 variables seleccionadas son:

| Variable                              | Unidad       |
|---------------------------------------|--------------|
| Conductividad electrica               | uS/cm        |
| Alcalinidad total                     | mg CaCO3/l   |
| Bicarbonatos                          | mg CaCO3/l   |
| Demanda bioquimica de oxigeno (DBO)   | mg O2/l      |
| Cloruros                              | mg Cl/l      |
| Dureza calcica                        | mg CaCO3/l   |
| Sodio total                           | mg Na/l      |
| Dureza total                          | mg CaCO3/l   |
| Calcio                                | mg Ca/l      |
| Turbiedad                             | UNT          |
| Sulfatos                              | mg SO4/l     |
| Nitratos                              | mg N-NO3/l   |
| pH                                    | -            |
| Solidos suspendidos totales           | mg SS/l      |
| Solidos totales                       | mg SST/l     |

## Estructura del proyecto

```
rio-cauca-water-quality-predictor/
|
+-- README.md                         # Documentacion principal
+-- requirements.txt                  # Dependencias Python
+-- .gitignore                        # Archivos ignorados por Git
|
+-- data/
|   +-- raw/
|       +-- Calidad_del_agua_del_Rio_Cauca_20260530.csv   # Dataset original
|
+-- notebooks/
|   +-- 01_training_optimized.ipynb   # Notebook de entrenamiento y evaluacion
|
+-- models/
|   +-- water_quality_pipeline.joblib # Pipeline (imputer + RF) serializado
|
+-- src/
|   +-- __init__.py
|   +-- preprocessing.py              # Definicion de features y creacion del DataFrame
|   +-- predict.py                    # Carga del modelo y funcion de prediccion
|
+-- app/
    +-- app.py                        # Aplicacion Streamlit
```

## Instalacion local

### Requisitos previos

- Python 3.11 o superior
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/Yefryalexis123/rio-cauca-water-quality-predictor.git
cd rio-cauca-water-quality-predictor

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicacion
streamlit run app/app.py
```

La aplicacion estara disponible en `http://localhost:8501`.

## Uso de la aplicacion

1. Acceder a la URL publica de la aplicacion o ejecutarla localmente.
2. Ingresar los valores de las 15 variables fisicoquimicas medidas en la estacion de monitoreo.
3. Presionar el boton **Predecir**.
4. La aplicacion mostrara el resultado: **Buena**, **Regular** o **Mala**, segun la calidad detectada.

## Despliegue

La aplicacion esta desplegada en **Streamlit Community Cloud**, conectado directamente al repositorio de GitHub. Cualquier `push` a la rama `main` desencadena un redespliegue automatico.

Pasos seguidos:

1. Subir el codigo a GitHub (repositorio publico).
2. Conectar el repositorio en [https://streamlit.io/cloud](https://streamlit.io/cloud).
3. Configurar el archivo de entrada como `app/app.py`.
4. Desplegar con un clic.

## Autores

| Nombre                        | Rol                                              |
|-------------------------------|--------------------------------------------------|
| Juan Fernando Bueno Torres    | Entrenamiento del modelo y analisis exploratorio |
| Yefry Alexis Muneton Cordoba  | Desarrollo de la aplicacion web y despliegue     |
| Jonathan Pedroza Bernal       | Preprocesamiento de datos y documentacion        |

**Grupo 6 - Inteligencia Artificial I**
Fundacion Universitaria Los Libertadores

## Licencia

MIT License

## Referencias

- Datos Abiertos Colombia. *Calidad del agua del Rio Cauca*. https://www.datos.gov.co
- Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5-32. https://doi.org/10.1023/A:1010933404324
- Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR*, 12, 2825-2830. http://jmlr.org/papers/v12/pedregosa11a.html
- Streamlit Inc. (2024). *Streamlit Documentation*. https://docs.streamlit.io
- Streamlit Community Cloud. *Deploy your app*. https://docs.streamlit.io/streamlit-community-cloud
