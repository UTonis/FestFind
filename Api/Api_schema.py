from core.database import Optional
from pydantic import BaseModel

class SearchDTO(BaseModel):
    numOfRows: int
    pageNo: int
    keyword: str