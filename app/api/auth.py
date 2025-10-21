from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from sql_models import User
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from .schemas import Token, UserCreateRequest, UserResponse
import os
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACESS_TOKEN_EXPIRY=60 * 24 * 30

SECRET=os.environ.get("AUTH_SECRET_KEY")

def verify_pass(given_pass: str, hashed: str) -> bool:
    return pwd_context.verify(given_pass, hashed)

def hash_pass(given: str) -> str:
    return pwd_context.hash(given)

def create_token(id: str, expiry_delta: Optional[timedelta] = None):
    expiry_date = datetime.now() + expiry_delta if expiry_delta else datetime.now() + timedelta(minutes=ACESS_TOKEN_EXPIRY)
    return jwt.encode({"sub": id, "exp": expiry_date}, key=SECRET) #Algo = HS256

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET)
    except JWTError:
        return None
    


async def get_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    decoded = decode_token(token)
    if decoded is None or decoded.get("sub") is None:
        raise credentials_exception
    user = db.query(User).filter(User.id == decoded.get("sub")).first()
    if not user:
        raise credentials_exception

    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == form_data.username,
    ).first()
    
    if not user or not verify_pass(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return {
        "access_token": create_token(user.id),
        "token_type": "bearer"
    }
    
@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user_in: UserCreateRequest, db: Session = Depends(get_db)
):
    
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    user = User(
        email=user_in.email,
        password=hash_pass(user_in.password)
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }


@router.get("/me", response_model=UserResponse)
async def get_me(cur_user: User = Depends(get_user)):
    print(cur_user)
    return {
        "id": cur_user.id,
        "email": cur_user.email,
        "created_at": cur_user.created_at
    } 