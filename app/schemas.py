from pydantic import BaseModel


class InsuranceRequest(BaseModel):
    date: str
    cargo_type: str
    declared_value: float
