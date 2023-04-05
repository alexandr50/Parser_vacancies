from pydantic import BaseModel

class VacancyApi(BaseModel):
    name: str
    salary: str
    description: str
    company_name: str
    url: str
    description: str