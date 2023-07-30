from pydantic import BaseModel
from typing import List
from models.Skill import Skill
from models.Languaje import Languaje

class Developer(BaseModel):
    _id: str
    name: str
    age: int
    address: str
    skills: List[Skill]
    languages: List[Languaje]