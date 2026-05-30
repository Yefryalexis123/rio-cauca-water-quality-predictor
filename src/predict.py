import joblib

MODEL_PATH = "models/water_quality_pipeline.joblib"

model = joblib.load(MODEL_PATH)


def predict_water_quality(df):
    return model.predict(df)[0]