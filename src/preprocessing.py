import pandas as pd

FEATURE_COLUMNS = [
    'CONDUCTIVIDAD ELÉCTRICA (µS/cm)',
    'ALCALINIDAD TOTAL (mg CaCO3/l)',
    'BICARBONATOS (mg CaCO3/l)',
    'DEMANDA BIOQUIMICA DE OXIGENO (mg O2/l)',
    'CLORUROS (mg Cl/l)',
    'DUREZA CALCICA (mg CaCO3/l)',
    'SODIO TOTAL (mg Na/l)',
    'DUREZA TOTAL (mg CaCO3/l)',
    'CALCIO (mg Ca/l)',
    'TURBIEDAD (UNT)',
    'SULFATOS (mg SO4/l)',
    'NITRATOS (mg N-NO3/l)',
    'pH',
    'SOLIDOS SUSPENDIDOS TOTALES (mg SS/l)',
    'SOLIDOS TOTALES (mg SST/l)'
]

def create_input_dataframe(data):
    return pd.DataFrame([data], columns=FEATURE_COLUMNS)