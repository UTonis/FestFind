from pydantic import BaseModel

class WirteRatingDTO(BaseModel):
    contentId: int
    contentTypeId: int
    user_id: str
    rating: int
    title: str