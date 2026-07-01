from fastapi import FastAPI
from database import collection
from models import Risk

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Risk Library API"}


@app.post("/risks")
def add_risk(risk: Risk):
    risk_data = risk.model_dump()
    collection.insert_one(risk_data)
    return {"message": "Risk added successfully"}


@app.get("/risks")
def get_risks():
    risks = []

    for risk in collection.find({}, {"_id": 0}):
        risks.append(risk)

    return risks