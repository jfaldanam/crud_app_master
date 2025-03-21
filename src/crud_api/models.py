from pydantic import BaseModel

class Project(BaseModel):
    name: str
    time: int