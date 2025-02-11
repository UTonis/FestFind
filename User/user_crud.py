from sqlalchemy.ext.asyncio import AsyncSession
from core.models import UserModel
from core.dependencies import hash_password
from sqlalchemy import select

class UserCRUD:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_by_id(self, user_id: str):
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str):
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, username: str, email: str, user_id: str, password: str):
        hashed_password = hash_password(password)
        new_user = UserModel(username=username, email=email, id=user_id, pw=hashed_password)
        
        self._session.add(new_user)
        await self._session.commit()

        return new_user