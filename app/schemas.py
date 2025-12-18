from pydantic import BaseModel

class UserRegistre(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
      username: str
      password: str

class PredictionResponse(BaseModel):
    churn_probability: float 

class PredictRequest(BaseModel):
    employee_id: str
    Age: int
    Education: int
    EnvironmentSatisfaction: int
    JobInvolvement: int
    JobLevel: int
    JobSatisfaction: int
    MonthlyIncome: float
    PerformanceRating: int
    TotalWorkingYears: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsWithCurrManager: int
    BusinessTravel: str
    Department: str
    EducationField: str
    Gender: str
    JobRole: str
    MaritalStatus: str
    OverTime: str
