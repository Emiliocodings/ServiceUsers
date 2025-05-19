from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import re

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    role: str = Field(..., pattern=r"^(admin|user|guest)$")
    active: bool = True

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not 3 <= len(v) <= 50:
            raise ValueError('Username must be between 3 and 50 characters')
        return v

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError('Invalid email format')
        return v

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not 1 <= len(v) <= 50:
            raise ValueError('Name must be between 1 and 50 characters')
        return v

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in ['admin', 'user', 'guest']:
            raise ValueError('Role must be one of: admin, user, guest')
        return v

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    role: Optional[str] = Field(None, pattern=r"^(admin|user|guest)$")
    active: Optional[bool] = None

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not 3 <= len(v) <= 50:
            raise ValueError('Username must be between 3 and 50 characters')
        return v

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError('Invalid email format')
        return v

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not 1 <= len(v) <= 50:
            raise ValueError('Name must be between 1 and 50 characters')
        return v

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ['admin', 'user', 'guest']:
            raise ValueError('Role must be one of: admin, user, guest')
        return v

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 