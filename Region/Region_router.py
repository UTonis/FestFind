from fastapi import APIRouter, Depends
from core.database import provide_session
from sqlalchemy.ext.asyncio import AsyncSession
from Region.Region_crud import RegionCRUD

router = APIRouter(
   prefix="/region",
   tags=["region"],
)

@router.post("/add_regionCode")
async def add_regionCode(id: str, region: int, db: AsyncSession = Depends(provide_session)):
    crud = RegionCRUD(db)

    await crud.create_region(id, region)

@router.post("/get_regionCode_by_id")
async def get_regionCode(id: str, db: AsyncSession = Depends(provide_session)):
    crud = RegionCRUD(db)

    result =  await crud.get_by_id(id)

    return result

@router.delete("/delete_regionCode")
async def delete_regionCode(id: str, regionCode: int, db: AsyncSession = Depends(provide_session)):
    crud = RegionCRUD(db)

    await crud.delete_region(id, regionCode)