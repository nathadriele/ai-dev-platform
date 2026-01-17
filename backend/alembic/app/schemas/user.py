from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    full_name: str | None = Field(None, max_length=100)


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """User update schema."""
    full_name: str | None = Field(None, max_length=100)


class User(UserBase):
    """User response schema."""
    id: UUID
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserWithTokens(User):
    """User schema with tokens."""
    tokens: dict


class TokenRefresh(BaseModel):
    """Token refresh schema."""
    refresh_token: str


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
