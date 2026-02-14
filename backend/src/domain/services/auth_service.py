from passlib.context import CryptContext
from ..entities.user import User
from ..exceptions import InvalidCredentialsError


class AuthenticationService:
    """Domain service for authentication logic"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def authenticate_user(self, user: User, password: str) -> User:
        """
        Authenticate user with password
        Raises InvalidCredentialsError if authentication fails
        """
        if not self.verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        
        return user
