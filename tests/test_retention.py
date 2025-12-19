import pytest
from unittest.mock import patch
from app.main import create_retention_plan, PredictRequest

def test_create_retention_plan_mock():
    # Données fictives pour l'employé
    request = PredictRequest(
        employee_id="E001",
        Age=30,
        BusinessTravel="Travel_Rarely",
        Department="Sales",
        Education=3,
        EducationField="Marketing",
        EnvironmentSatisfaction=3,
        Gender="Male",
        JobInvolvement=3,
        JobLevel=2,
        JobRole="Sales Executive",
        JobSatisfaction=4,
        MaritalStatus="Single",
        MonthlyIncome=5000,
        OverTime="Yes",
        PerformanceRating=3,
        TotalWorkingYears=5,
        WorkLifeBalance=3,
        YearsAtCompany=3,
        YearsInCurrentRole=2,
        YearsWithCurrManager=2
    )

    # Mock de la fonction Gemini pour éviter l'appel réel à l'API
    with patch("app.main.generate_retention_plan_gemini") as mock_gemini:
        mock_gemini.return_value = ["Action 1", "Action 2", "Action 3"]

        # Appel de la fonction
        result = create_retention_plan(request)

        # Vérifications
        assert result.employee_id == "E001"
        assert isinstance(result.retention_plan, list)
        assert len(result.retention_plan) == 3
        assert result.retention_plan[0] == "Action 1"

        print("Test mocké réussi :", result)
