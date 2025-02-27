from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import RegionModel

class RegionCRUD:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_region(self, id: str, region_id: int):
        new_regionCode = RegionModel(id = id, region_id = region_id)
        
        self._session.add(new_regionCode)
        await self._session.commit()

        return new_regionCode
    
    async def get_by_id(self, id: str):
        stmt = select(RegionModel).where(RegionModel.id == id)
        result = await self._session.execute(stmt)
        return result.scalars().all()
    
    async def delete_region(self, id: str, regionCode: int):
        result = await self._session.execute(select(RegionModel).filter(RegionModel.id == id, RegionModel.region_id == regionCode))
        region = result.scalar_one_or_none()
        if region:
            await self._session.delete(region)
            await self._session.commit()