from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    google_id: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class UserInDB(UserBase):
    id: int
    google_id: str
    preferences: Dict[str, Any] = {}
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDB):
    pass


class UserProfile(BaseModel):
    id: int
    email: str
    name: str
    preferences: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True