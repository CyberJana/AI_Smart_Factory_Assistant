from datetime import timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.core.security import create_token, hash_password, verify_password
from app.db import get_db
from app.models import AuditLog, User
from app.schemas import LoginRequest, TokenPair, UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])


def issue_tokens(user_id: str) -> TokenPair:
    settings = get_settings()
    return TokenPair(
        access_token=create_token(
            user_id, "access", timedelta(minutes=settings.access_token_expire_minutes)
        ),
        refresh_token=create_token(
            user_id, "refresh", timedelta(days=settings.refresh_token_expire_days)
        ),
    )


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    existing = db.scalar(select(User).where(User.email == payload.email.lower()))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email is already registered"
        )
    user = User(
        email=payload.email.lower(),
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.flush()
    db.add(
        AuditLog(user_id=user.id, action="user.registered", entity_type="user", entity_id=user.id)
    )
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenPair:
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )
    db.add(
        AuditLog(user_id=user.id, action="user.logged_in", entity_type="user", entity_id=user.id)
    )
    db.commit()
    return issue_tokens(user.id)


@router.post("/refresh", response_model=TokenPair)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)) -> TokenPair:
    try:
        payload = jwt.decode(
            refresh_token,
            get_settings().jwt_secret,
            algorithms=[get_settings().jwt_algorithm],
        )
    except jwt.PyJWTError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        ) from error
    if payload.get("type") != "refresh" or not db.get(User, payload.get("sub")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    return issue_tokens(payload["sub"])


@router.get("/me", response_model=UserOut)
def current_user_profile(current_user: User = Depends(get_current_user)) -> User:
    return current_user
