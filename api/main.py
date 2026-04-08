from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from typing import Dict
import joblib

MODEL_FILEPATH = "best_model.pkl"

# classe pour passage json comme paramètre
class Reading(BaseModel):
    machine_id: str
    temperature_celsius: float
    temperature_celsius_mean_24h: float
    temperature_celsius_mean_48h: float
    vibration_mm_s: float
    vibration_mm_s_mean_24h: float
    vibration_mm_s_mean_48h: float
    power_consumption_kw: float
    pressure_bar: float
    age: int

# on charge le modèle
model = joblib.load(open(MODEL_FILEPATH, 'rb'))

# API
app = FastAPI(title="Machine Failure predictor")

@app.get("/")
async def health() -> Dict:
    return {"status":"ok"}

# Recupération des valeurs capteurs et information nécessaires
# faire la prédiction avec le modèle, retourner le résultat (0 ou 1) via
# un fichier json
@app.post("/predict")
async def predict_post(reading: Reading)-> Dict:
    data = {"machine_id": reading.machine_id,
            "vibration_mm_s": reading.vibration_mm_s,
            "vibration_mm_s_mean_24h": reading.vibration_mm_s_mean_24h,
            "pressure_bar": reading.pressure_bar,
            "temperature_celsius": reading.temperature_celsius,
            "vibration_mm_s_mean_48h": reading.vibration_mm_s_mean_48h,
            "temperature_celsius_mean_24h": reading.temperature_celsius_mean_24h,
            "age":reading.age,
            "power_consumption_kw": reading.power_consumption_kw,
            "temperature_celsius_mean_48h": reading.temperature_celsius_mean_48h
    }

    df_reading = pd.DataFrame.from_dict(data=data,orient='index').T
    df_reading = df_reading.drop(columns=['machine_id'])
    pred = int(model.predict(df_reading)[0])
    return {'prediction':pred}