from fastapi import APIRouter, Depends
from core.database import provide_session
from Rating.rating_schema import WirteRatingDTO
from Rating.rating_crud import RatingCRUD
from User.user_crud import UserCRUD
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
   prefix="/ratings",
   tags=["ratings"],
)

@router.post("/WirteRating")
async def insert_rating(rate: WirteRatingDTO, db: AsyncSession = Depends(provide_session)):
   ex = UserCRUD(db)
   exist = await ex.get_user_by_id(rate.user_id)
   if exist is None:
      return {"message" : "id가 존재하지 않습니다."}
   
   crud = RatingCRUD(db)
   rating = await crud.create_rating(rate.contentId, rate.contentTypeId, rate.user_id, rate.rating, rate.title)
   
   return rating

@router.post("/get_rating_by_id")
async def get_rating_by_id(user_id: str, db: AsyncSession = Depends(provide_session)):
   ex = UserCRUD(db)
   exist = await ex.get_user_by_id(user_id)
   if exist is None:
      return {"message" : "id가 존재하지 않습니다."}
   
   crud = RatingCRUD(db)
   rating = await crud.get_rating_by_id(user_id)

   return rating

@router.post("/get_rating_by_contentId")
async def get_rating_by_contentId(contentId: int, db: AsyncSession = Depends(provide_session)):
   crud = RatingCRUD(db)
   rating = await crud.get_rating_by_contentid(contentId)

   return rating
