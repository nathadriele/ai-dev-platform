from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, User, TokenRefresh, TokenResponse
from typing import Dict

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> Dict:
    """Register a new user."""
    # Check if user exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": {"message": "User with this email already exists", "code": "USER_EXISTS"}},
        )

    result = await db.execute(select(User).where(User.username == user_data.username))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": {"message": "Username already taken", "code": "USERNAME_TAKEN"}},
        )

    # Create user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Generate tokens
    access_token = create_access_token(data={"sub": str(new_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(new_user.id)})

    return {
        "data": User.model_validate(new_user),
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
    }


@router.post("/login")
async def login_user(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Dict:
    """Authenticate user and return tokens."""
    # Find user
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"message": "Invalid email or password", "code": "INVALID_CREDENTIALS"}},
        )

    # Generate tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "data": User.model_validate(user),
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token_data: TokenRefresh) -> TokenResponse:
    """Refresh access token using refresh token."""
    payload = decode_token(token_data.refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"message": "Invalid or expired refresh token", "code": "INVALID_TOKEN"}},
        )

    access_token = create_access_token(data={"sub": payload["sub"]})
    return TokenResponse(access_token=access_token)
