from pydantic import BaseModel

class SearchDTO(BaseModel):
    numOfRows: int
    pageNo: int
    contentTypeId: int
    keyword: str

class festivalInfoDTO(BaseModel):
    contentId: int
    contentTypeId: int

class calendarDTO(BaseModel):
    Year: int
    Month: int