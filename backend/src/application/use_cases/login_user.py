from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository
from ...domain.services.auth_service import AuthenticationService
from ...domain.exceptions import EntityNotFoundError, InvalidCredentialsError


class LoginUserUseCase:
    """Use case: Login user"""
    
    def __init__(
        self,
        user_repository: UserRepository,
        auth_service: AuthenticationService
    ):
        self.user_repository = user_repository
        self.auth_service = auth_service
    
    async def execute(self, email: str, password: str) -> User:
        """
        Login user with email and password
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            Authenticated user
            
        Raises:
            InvalidCredentialsError: If credentials are invalid
        """
        # Get user by email
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise InvalidCredentialsError()
        
        # Authenticate
        authenticated_user = self.auth_service.authenticate_user(user, password)
        
        return authenticated_user
