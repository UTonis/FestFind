from fastapi import APIRouter, Depends, HTTPException
from core.database import provide_session
from core.dependencies import verify_jwt, verify_password, create_jwt, hash_password
from core.models import UserModel
from .user_schema import UserDTO, LoginUserDTO
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
   prefix="/user",
   tags=["user"],
)

#################### 컨트롤러 부분
@router.post("/login")
async def login_user(lg_user: LoginUserDTO, db: AsyncSession = Depends(provide_session)):
    stmt = select(UserModel).where(UserModel.id == lg_user.id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        if verify_password(lg_user.pw, user.pw):
            token_data = {"sub": user.id}
            token = create_jwt(token_data)
            return {"msg": "로그인 성공", "access_token": token}
        else:
            raise HTTPException(status_code=401, detail="비밀번호 불일치")
    else:
        raise HTTPException(status_code=404, detail="아이디가 존재하지 않습니다.")

@router.post("/register")
async def register_user(user: UserDTO, db: AsyncSession = Depends(provide_session)):
    stmt = select(UserModel).where(UserModel.id == user.id)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다.")
    
    stmt = select(UserModel).where(UserModel.email == user.email)
    result = await db.execute(stmt)
    existing_email = result.scalar_one_or_none()
    if existing_email:
        raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")

    # 비밀번호 해싱
    hashed_password = hash_password(user.pw)
    
    # 새 사용자 생성
    db_user = UserModel(
        username=user.username,
        email=user.email,
        id=user.id,
        pw=hashed_password
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    
    return {"msg": "회원가입 성공"}