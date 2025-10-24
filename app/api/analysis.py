from fastapi import APIRouter, Depends, Request
from .schemas import ChatAnalysisReponse, ChatAnalysisRequest, ChatMessage
from .parser import parse_chat
from agents import ScamDetectionAgent, ScamAnalysis
from sqlalchemy.orm import Session
from database import get_db
from sql_models import AnalysisRequest, AnalysisResponse, User
from .auth import get_user
from typing import Union
import os

router = APIRouter()

def get_scam_agent(state):
    if not hasattr(state, 'scam_agent') or state.scam_agent is None:
        state.scam_agent = ScamDetectionAgent(os.environ.get("MOORCHEH_KEY"))
    return state.scam_agent
    

@router.get("/")
async def analyze_root():
    return {"message" : "This is analysis root"}


@router.post("/analyze", response_model=Union[ChatAnalysisReponse, dict])
async def analyze(
    request: Request,
    body: ChatAnalysisRequest,
    db: Session = Depends(get_db),
    cur_user: User = Depends(get_user)
):
    request_entry: AnalysisRequest = None
    try:
        request_entry = AnalysisRequest(
            user=cur_user.email
        )
        db.add(request_entry)
        db.commit()
        db.refresh(request_entry)
    except Exception:
        return {"success" : False, "reason": "There is already a response being processed for this request"}
    
    try:
        agent = get_scam_agent(request.app.state)
        messages: list[ChatMessage] = parse_chat(body.chat_content, body.platform.lower().strip())
        response = await agent.analyze(messages, body.platform)
        analysis: ScamAnalysis = response['analysis']
        
        response_entry = AnalysisResponse(
            request_id=request_entry.id,
            raw_response=response.get("raw_response"),
            success=response.get("success"),
            model=response.get("model"),
            prompt=response.get("prompt")
        )
        
        db.add(response_entry)
        db.commit()
        db.refresh(response_entry)
        
        return ChatAnalysisReponse(
            analysis_id=response_entry.id,
            score=analysis.risk_score,
            risk=analysis.risk_level,
            labels=[v.type for v in analysis.indicators],
            analysis_content=analysis.summary
        )
    except Exception as e:
        return {
            "success": False,
            "reason": "There was an error while trying to generate a response ",
            "detail": str(e),
            "request_id": request_entry.id
        }
        
    
    
    


