from core.database import Optional
from pydantic import BaseModel

class UserDTO(BaseModel):
    id: str 
    pw: str  
    email: str  
    username: str 

class LoginUserDTO(BaseModel):
    id: str
    pw: str
