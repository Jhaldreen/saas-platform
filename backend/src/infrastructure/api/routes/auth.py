from fastapi import APIRouter, Depends, HTTPException, status

from ....application.dto import UserCreateDTO, UserLoginDTO, TokenResponseDTO, UserResponseDTO
from ....application.use_cases import RegisterUserUseCase, LoginUserUseCase
from ....domain.entities.user import UserRole
from ....domain.exceptions import EntityAlreadyExistsError, InvalidCredentialsError
from ...security.jwt import create_access_token
from ..dependencies import get_register_user_use_case, get_login_user_use_case, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponseDTO, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserCreateDTO,
    use_case: RegisterUserUseCase = Depends(get_register_user_use_case)
):
    """Register a new user"""
    try:
        user = await use_case.execute(
            email=data.email,
            password=data.password,
            role=UserRole(data.role)
        )
        
        # Generate tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_access_token({"sub": str(user.id)}, expires_days=7)
        
        return TokenResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponseDTO.from_orm(user)
        )
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponseDTO)
async def login(
    data: UserLoginDTO,
    use_case: LoginUserUseCase = Depends(get_login_user_use_case)
):
    """Login user"""
    try:
        user = await use_case.execute(
            email=data.email,
            password=data.password
        )
        
        # Generate tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_access_token({"sub": str(user.id)}, expires_days=7)
        
        return TokenResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponseDTO.from_orm(user)
        )
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=UserResponseDTO)
async def get_me(current_user = Depends(get_current_user)):
    """Get current user"""
    return UserResponseDTO.from_orm(current_user)
