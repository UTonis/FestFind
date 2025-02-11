from fastapi import APIRouter, Depends
from core.database import provide_session
from fevorites.fevorites_schema import fevoritesDTO
from fevorites.fevorites_crud import fevoritesCRUD
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
   prefix="/fevorites",
   tags=["fevorites"],
)

@router.post("/insert_fevorites")
async def insert_rating(fevorites: fevoritesDTO, db: AsyncSession = Depends(provide_session)):
   crud = fevoritesCRUD(db)
   fevorites = await crud.create_fevorites(fevorites.contentId, fevorites.contentTypeId, fevorites.user_id)
   
   return fevorites

@router.post("/get_rating_by_id")
async def get_rating_by_id(user_id: str, db: AsyncSession = Depends(provide_session)):
   crud = fevoritesCRUD(db)
   fevorites = await crud.get_fevorites_by_id(user_id)

   return fevorites
