import pytest
import joblib
import pandas as pd

# Charger le modèle ML
model = joblib.load("ml/best_model.pkl")

def test_model_prediction_shape():
    # Exemple de features similaires à PredictRequest
    data = pd.DataFrame([{
        "Age": 35,
        "Education": 3,
        "EnvironmentSatisfaction": 4,
        "JobInvolvement": 3,
        "JobLevel": 2,
        "JobSatisfaction": 3,
        "MonthlyIncome": 5000,
        "PerformanceRating": 4,
        "TotalWorkingYears": 10,
        "WorkLifeBalance": 3,
        "YearsAtCompany": 5,
        "YearsInCurrentRole": 3,
        "YearsWithCurrManager": 2,
        "BusinessTravel": "Travel_Rarely",
        "Department": "Sales",
        "EducationField": "Marketing",
        "Gender": "Female",
        "JobRole": "Sales Executive",
        "MaritalStatus": "Single",
        "OverTime": "Yes"
    }])
    prob = model.predict_proba(data)[0][1]
    
    # Vérifier que la probabilité est bien entre 0 et 1
    assert 0 <= prob <= 1
