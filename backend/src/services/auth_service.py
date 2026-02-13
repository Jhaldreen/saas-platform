from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from .models.user import User
from .schemas.user import UserCreate, UserOut
from ..database import get_db

class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = "your_secret_key"  # Replace with your actual secret key
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_user(self, user: UserCreate) -> UserOut:
        db_user = User(email=user.email, hashed_password=self.hash_password(user.password))
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return UserOut.from_orm(db_user)

    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.db.query(User).filter(User.email == email).first()
        if not user or not self.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        return user