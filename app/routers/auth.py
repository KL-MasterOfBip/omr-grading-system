from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, Token

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Đăng ký tài khoản mới.
    
    - **username**: tên đăng nhập (phải unique)
    - **email**: email (phải unique)
    - **password**: mật khẩu (sẽ được hash)
    - **full_name**: tên đầy đủ (tuỳ chọn)
    """
    repo = UserRepository(db)
    
    # Kiểm tra username đã tồn tại
    if repo.get_by_username(user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    
    # Kiểm tra email đã tồn tại
    if repo.get_by_email(user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Tạo user mới
    user = repo.create(
        username=user_in.username,
        email=user_in.email,
        password=user_in.password,
        full_name=user_in.full_name,
    )
    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Đăng nhập và nhận JWT access token.
    
    - **username**: tên đăng nhập
    - **password**: mật khẩu
    
    Trả về: `access_token` (dùng trong header `Authorization: Bearer <token>`)
    """
    repo = UserRepository(db)
    
    # Tìm user theo username
    user = repo.get_by_username(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Kiểm tra password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Kiểm tra user có active không
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    # Tạo access token
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(hours=24),
    )
    
    return {"access_token": access_token, "token_type": "bearer"}