from pathlib import Path
import joblib

ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = ROOT / "models" / "water_quality_pipeline.joblib"

model = joblib.load(MODEL_PATH)

def predict_water_quality(df):
    prediction = model.predict(df)
    return prediction[0]