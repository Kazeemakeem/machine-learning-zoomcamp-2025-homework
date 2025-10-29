import pickle
from typing import Optional, Literal
from pydantic import BaseModel, Field
from fastapi import FastAPI
import uvicorn

class Customer(BaseModel):
    number_of_courses_viewed: int = Field(..., ge=0, le=9)
    annual_income: float = Field(..., ge=0.0, le=109899.0)
    lead_source: Optional[Literal["organic_search", "social_media", "paid_ads", "referral", "events"]] = Field(None)

class PredictResponse(BaseModel):
    conversion_probability: float
    convert: bool

app = FastAPI(title="customer-conversion-prediction")

# customer = {
#     "lead_source": "paid_ads",
#     "number_of_courses_viewed": 2,
#     "annual_income": 79276.0
# }

with open('pipeline_v2.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)

def predict_single(customer):
    result = pipeline.predict_proba(customer)[0, 1]
    return float(result)

@app.post("/predict")
def predict(customer: Customer) -> PredictResponse:
    prob = predict_single(customer.model_dump())

    return PredictResponse(
        conversion_probability=prob,
        convert=prob >= 0.5
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)


# if __name__ == "__main__":
#     prediction = predict_single(customer)
#     print(f"Predicted probability of purchase: {prediction:.4f}")