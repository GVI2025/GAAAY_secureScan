from pydantic import BaseModel, EmailStr
from typing import Optional

class AgentBase(BaseModel):
    nom: str
    email: EmailStr
    actif: Optional[bool] = True

class AgentCreate(AgentBase):
    pass

class AgentUpdate(AgentBase):
    pass

class AgentRead(AgentBase):
    id: str

    class Config:
        orm_mode = True
