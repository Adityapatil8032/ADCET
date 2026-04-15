
from pydantic import BaseModel

class Worker(BaseModel):
    name: str
    skills: list
    experience: int
    location: str
