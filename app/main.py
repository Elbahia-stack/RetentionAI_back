from .database import Base, engine,get_db
from . import models
from .models import PredictionHistory
from .schemas import UserRegistre,PredictionResponse,PredictRequest
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .security import hash_password, verify_password 
from .auth import create_access_token, verify_token
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
import joblib
import pandas as pd

Base.metadata.create_all(bind=engine)
model = joblib.load("best_model.pkl")

app=FastAPI()
origins = [
     "http://localhost:3000",
    "http://172.26.112.1:3000",
   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
OAuth2_scheme=OAuth2PasswordBearer(tokenUrl="/login")
@app.post("/register")
def regester(user:UserRegistre,db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")
    hashed = hash_password(user.password)

    new_user = models.User(username=user.username,  passwordhash=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
   
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.passwordhash):
        raise HTTPException(status_code=401, detail="Username ou password incorrect")

    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/predict",response_model=PredictionResponse)
def prediction( data: PredictRequest ,token=Depends(OAuth2_scheme),db: Session = Depends(get_db)):
    username = verify_token(token)

    
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur introuvable")
    features = pd.DataFrame([data.dict(exclude={"employee_id"})])
    probability = model.predict_proba(features)[0][1]

    
    prediction = PredictionHistory(
        user_id=user.id,
        employee_id=data.employee_id,
        probability=round(probability, 3)
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return {"churn_probability":probability}