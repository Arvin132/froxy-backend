from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
import sql_models as models
import os
import json

router = APIRouter()


@router.get("/user")
async def test_user(
    request: Request,
    db: Session = Depends(get_db)
):
    new_user = models.User(
        email="asgharianarvin@gmail.com",
        password="arvin123"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    
    return {
        "message": "success",
        "user_id": new_user.id
    }

@router.get("/allUser")
async def all_user(
    request: Request,
    db: Session = Depends(get_db)
):
    users = db.query(models.User).all()
    return {
        "message": "success",
        "users": [str(u) for u in users]
    }

@router.get("/allAnalysisRequests")
async def all_user(
    request: Request,
    db: Session = Depends(get_db)
):
    requests = db.query(models.AnalysisRequest).all()
    return {
        "message": "success",
        "requests": [str(u) for u in requests]
    }

@router.get("/allAnalysisResponses")
async def all_user(
    request: Request,
    db: Session = Depends(get_db)
):
    responses = db.query(models.AnalysisResponse).all()
    return {
        "message": "success",
        "responses": [str(u) for u in responses]
    }

