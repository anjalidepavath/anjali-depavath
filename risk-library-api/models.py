from pydantic import BaseModel
from datetime import datetime


class Risk(BaseModel):
    id: str
    name: str
    description: str
    category: str
    severity: str
    archetype: str
    trust_attribute: str
    created_at: datetime
    version: str