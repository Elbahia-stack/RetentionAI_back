import google.genai as genai
import os
from pydantic import BaseModel, ValidationError

# Initialisation du client Gemini
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

# Schema attendu pour le JSON de sortie
class RetentionResponseJson(BaseModel):
    retention_plan: list[str]

def generate_retention_plan_gemini(employee_data: dict, churn_probability: float):
    prompt = f"""
Agis comme un expert RH.
RENVOIE STRICTEMENT UN JSON.

Voici les informations sur l’employé :
- Age : {employee_data['Age']}
- Département : {employee_data['Department']}
- Role : {employee_data['JobRole']}
- Niveau de satisfaction : {employee_data['JobSatisfaction']}
- Performance : {employee_data['PerformanceRating']}
- Equilibre vie professionnelle/personnelle : {employee_data['WorkLifeBalance']}

Contexte : ce salarié a un risque élevé de départ ({churn_probability*100:.1f}%).

Tâche : propose 3 actions concrètes et personnalisées pour le retenir dans l’entreprise, en tenant compte de son role, sa satisfaction, sa performance et son équilibre vie professionnelle/personnelle.

FORMAT ATTENDU :
{{
  "retention_plan": [
    "Action 1",
    "Action 2",
    "Action 3"
  ]
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": RetentionResponseJson.model_json_schema()
        }
    )

    try:
        result = RetentionResponseJson.model_validate_json(response.text)
        return result.retention_plan
    except ValidationError:
        # Valeur de retour par défaut en cas d'erreur
        return [
            "Proposer 2 jours de télétravail",
            "Réévaluer la charge de travail",
            "Plan de formation personnalisé"
        ]
