from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import BaseService
from app.core.security import get_password_hash, verify_password


class UserService(BaseService[User, UserCreate, UserUpdate]):
    """Service for user operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def create(self, obj_in: UserCreate) -> User:
        """Create a new user with hashed password."""
        user_data = obj_in.model_dump()
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
        db_obj = User(**user_data)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, email: str, password: str
    ) -> Optional[User]:
        """Authenticate user by email and password."""
        user = await self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def is_active(self, user: User) -> bool:
        """Check if user is active."""
        return True  # Implement if you add is_active field
