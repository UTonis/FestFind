from sqlalchemy import Column, Integer, PrimaryKeyConstraint, String, ForeignKey
from core.database import Base

class UserModel(Base):
    __tablename__ = "users"
    
    pk = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(50), unique=True, nullable=False)
    pw = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    username = Column(String(50), nullable=False)

class RegionModel(Base):
    __tablename__ = "regions"
    
    region_id = Column(Integer, nullable=False)
    id = Column(String(50), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # 복합 기본 키 설정
    __table_args__ = (
        PrimaryKeyConstraint('region_id', 'id'),
    )