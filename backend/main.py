from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import pandas as pd

# Initialize FastAPI app
app = FastAPI(title="AI-Powered Crop Yield & Recommendation System")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML Model (Yield Prediction)
ml_model = joblib.load("../ml_model.pk1")  # path to saved ML model

# Load NLP Model (Recommendation Generator)
model_name = "../crop_nlp_model"  # path to your trained NLP model
tokenizer = AutoTokenizer.from_pretrained(model_name)
nlp_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
nlp_pipeline = pipeline("text2text-generation", model=nlp_model, tokenizer=tokenizer)

# Request Schema
class CropInput(BaseModel):
    crop: str
    crop_year: int
    season: str
    state: str
    area: float
    annual_rainfall: float
    fertilizer: float
    pesticide: float
    production:float
    budget: float
    goal: str


# Endpoint: Predict yield + NLP recommendation
@app.post("/predict")
def predict_crop(input_data: CropInput):
    # Prepare ML input (without Production, since that's what we predict)
    ml_features = pd.DataFrame([{
        "Crop": input_data.crop,
        "Crop_Year": input_data.crop_year,
        "Season": input_data.season,
        "State": input_data.state,
        "Area": input_data.area,
        "Annual_Rainfall": input_data.annual_rainfall,
        "Fertilizer": input_data.fertilizer,
        "Pesticide": input_data.pesticide,
        "Production":input_data.production
    }])

    # ML Model prediction (Production/Yield)
    predicted_yield = ml_model.predict(ml_features)[0]

    # NLP Model input text
    text_input = (
        f"Crop: {input_data.crop}, Predicted Yield: {predicted_yield:.2f} t/ha, "
        f"Area: {input_data.area} ha, Budget: {input_data.budget} INR, Goal: {input_data.goal}"
    )

    # NLP Recommendation
    result = nlp_pipeline(
        text_input,
        max_new_tokens=80,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7
    )

    return {
        "predicted_yield": predicted_yield,
        "recommendation": result[0]['generated_text']
    }
