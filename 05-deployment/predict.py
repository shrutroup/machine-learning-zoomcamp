import pickle
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="lead scoring service")

with open("pipeline_v2.bin", 'rb') as f_in:
        pipeline = pickle.load(f_in)


class Customer(BaseModel):
    lead_source: str
    number_of_courses_viewed: int
    annual_income: float

@app.post("/predict")
def predict(customer: Customer):
    customer_dict = {
        "lead_source": customer.lead_source,
        "number_of_courses_viewed": customer.number_of_courses_viewed,
        "annual_income": customer.annual_income
    }
    prediction = pipeline.predict_proba(customer_dict)[0, 1]
    return {
        "lead conversion probability": float(prediction),
        "lead conversion": bool(prediction>=0.5)
    }
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)