from uuid import uuid4
from datetime import datetime

from ...domain.entities.user import User, UserRole
from ...domain.repositories.user_repository import UserRepository
from ...domain.services.auth_service import AuthenticationService
from ...domain.exceptions import EntityAlreadyExistsError


class RegisterUserUseCase:
    """Use case: Register a new user"""
    
    def __init__(
        self,
        user_repository: UserRepository,
        auth_service: AuthenticationService
    ):
        self.user_repository = user_repository
        self.auth_service = auth_service
    
    async def execute(self, email: str, password: str, role: UserRole = UserRole.MEMBER) -> User:
        """
        Register a new user
        
        Args:
            email: User email
            password: Plain text password
            role: User role
            
        Returns:
            Created user
            
        Raises:
            EntityAlreadyExistsError: If email already exists
        """
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise EntityAlreadyExistsError("User", "email", email)
        
        # Hash password
        password_hash = self.auth_service.hash_password(password)
        
        # Create user entity
        user = User(
            id=uuid4(),
            email=email,
            password_hash=password_hash,
            role=role,
            created_at=datetime.utcnow()
        )
        
        # Save to repository
        created_user = await self.user_repository.create(user)
        
        return created_user
