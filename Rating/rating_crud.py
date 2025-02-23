from sqlalchemy.ext.asyncio import AsyncSession
from core.models import RatingModel
from sqlalchemy.future import select

class RatingCRUD:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_rating(self,contentId: int, contentTypeId: int, user_id: str, rating: int, title: str):
        new_rating = RatingModel(contentId=contentId, contentTypeId=contentTypeId, user_id=user_id, rating=rating, title=title)
        
        self._session.add(new_rating)
        await self._session.commit()

        return new_rating
    
    async def get_rating_by_id(self, user_id: int):
        result = await self._session.execute(select(RatingModel).filter(RatingModel.user_id == user_id))
        return result.scalar_one_or_none()
    
    async def get_rating_by_contentid(self, contentId: int):
        result = await self._session.execute(select(RatingModel).filter(RatingModel.contentId == contentId))
        return result.scalars().all()

    async def delete_rating(self, id: int): #아직 사용 X
        result = await self._session.execute(select(RatingModel).filter(RatingModel.id == id))
        post = result.scalar_one_or_none()
        if post:
            await self._session.delete(post)
            await self._session.commit()