from fastapi import FastAPI
import pickle
import numpy as np

app = FastAPI()

model = pickle.load(open("app/StockPrice.pkl", "rb"))

@app.get("/")
def home():
    return {"message": "Stock Prediction API Running 🚀"}

@app.post("/predict")
def predict(data: dict):
    price = data["price"]
    prediction = model.predict([[price]])
    return {"prediction": float(prediction[0])}