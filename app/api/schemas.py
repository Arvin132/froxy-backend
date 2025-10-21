from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Literal
from enum import Enum
from datetime import datetime

class RiskLevel(Enum):
    LOW=0,
    MEDIUM=1,
    HIGH=2,
    EXTREME=3

class ChatMessage(BaseModel):
    sender: Literal["user", "other"]
    content: str    

class ChatAnalysisRequest(BaseModel):
    messages: list[ChatMessage]
    platform: str

class ChatAnalysisReponse(BaseModel):
    analysis_id: str
    score: float = Field(..., ge=0.0, le=100.0)
    risk: str
    labels: list[str]
    analysis_content: str
    

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None
    
    
class UserBase(BaseModel):
    email: EmailStr

class UserCreateRequest(UserBase):
    password: str = Field(..., min_length=8)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: str
    created_at: datetime