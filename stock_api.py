from fastapi import FastAPI 
import pickle 
import numpy as np 

app = FastAPI()

model = pickle.load(open("StockPrice.pkl","rb"))

@app.post("/predict")

def predict(data: dict):
    features = np.array([data["x1"], data["x2"]]).reshape(1,-1)
    prediction = model.predict(features)
    
    return {"prediction": float(prediction[0])}