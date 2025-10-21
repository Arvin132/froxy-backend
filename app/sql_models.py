from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False) # Should be hashed
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __str__(self):
        return f"User(id={self.id}, email='{self.email}', password='{self.password}')"
    
    def __repr__(self):
        return self.__str__()


class AnalysisRequest(Base):
    __tablename__ = "analysis_request"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.now())
    
    def __str__(self):
        return f"AnalysisRequest(id={self.id}, user='{self.user}', timestamp='{self.timestamp}')"
    
    def __repr__(self):
        return self.__str__()


class AnalysisResponse(Base):
    __tablename__ = "analysis_response"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    request_id = Column(String, ForeignKey("analysis_request.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.now())
    raw_response = Column(String)
    prompt = Column(String)
    success = Column(Boolean)
    model = Column(String(20))
    context_count = Column(Integer)
    
    def __str__(self):
        return (f"AnalysisResponse(id={self.id}, request_id='{self.request_id}', timestamp='{self.timestamp}', "
                f"raw_response='{self.raw_response}', prompt='{self.prompt}', success={self.success}, "
                f"model='{self.model}', context_count={self.context_count})")
    
    def __repr__(self):
        return self.__str__()