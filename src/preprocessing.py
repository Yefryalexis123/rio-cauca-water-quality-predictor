import pandas as pd

FEATURE_COLUMNS = [
    'pH',
    'TEMPERATURA (°C)',
    'COLOR (UPC)',
    'TURBIEDAD (UNT)',
    'SOLIDOS TOTALES (mg SST/l)',
    'SOLIDOS SUSPENDIDOS TOTALES (mg SS/l)',
    'SOLIDOS DISUELTOS (mg SD/l)',
    'DEMANDA BIOQUIMICA DE OXIGENO (mg O2/l)',
    'DEMANDA QUIMICA DE OXIGENO (mg O2/l)',
    'DUREZA TOTAL (mg CaCO3/l)',
    'DUREZA CALCICA (mg CaCO3/l)',
    'DUREZA MAGNESICA (mg CaCO3/l)',
    'CALCIO (mg Ca/l)',
    'MAGNESIO (mg Mg/l)',
    'ALCALINIDAD TOTAL (mg CaCO3/l)',
    'BICARBONATOS (mg CaCO3/l)',
    'CONDUCTIVIDAD ELÉCTRICA (µS/cm)',
    'HIERRO TOTAL (mg Fe/l)',
    'MANGANESO TOTAL (mg Mn/l)',
    'SODIO TOTAL (mg Na/l)',
    'POTASIO TOTAL (mg K/l)',
    'ZINC TOTAL (mg Zn/l)',
    'NITROGENO TOTAL (mg N/l)',
    'NITROGENO AMONIACAL (mg N-NH3/l)',
    'NITRITOS (mg N-NO2/l)',
    'NITRATOS (mg N-NO3/l)',
    'CLORUROS (mg Cl/l)',
    'FOSFORO TOTAL (mg P/l)',
    'FOSFATOS (mg PO4/l)',
    'SULFATOS (mg SO4/l)',
    'COLIFORMES TOTALES (NMP/100 ml)',
    'COLIFORMES FECALES (NMP/100 ml)'
]


def create_input_dataframe(data: dict) -> pd.DataFrame:
    return pd.DataFrame([data], columns=FEATURE_COLUMNS)