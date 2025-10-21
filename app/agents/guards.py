from pydantic import BaseModel, Field, model_validator
from typing import List, Literal
import json


class ScamIndicator(BaseModel):
    """Structured scam indicator"""
    type: str
    severity: Literal["low", "medium", "high", "critical"]
    description: str
    evidence: str


class ScamAnalysis(BaseModel):
    """Structured analysis output"""
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: Literal["safe", "low", "medium", "high", "critical"]
    is_likely_scam: bool
    indicators: List[ScamIndicator]
    summary: str
    recommendations: List[str]
    
    @model_validator(mode="after")
    def check_score_vs_level(self):
        if self.risk_score >= 75 and self.risk_level not in ["high", "critical"]:
            raise ValueError("High risk_score should have high/critical level")
        return self


class InputGuardrail:
    """Validate and sanitize input before sending to LLM"""
    
    @staticmethod
    def validate_messages(messages: list) -> bool:
        """Check if messages are valid"""
        if not messages or len(messages) < 1:
            raise ValueError("At least 1 message required")
        
        if len(messages) > 100:
            raise ValueError("Too many messages (max 100)")
        
        for msg in messages:
            if (
                not hasattr(msg, 'content') or len(msg.content) > 5000
                or not hasattr(msg, 'sender') or msg.sender not in ['user', 'other']
            ):
                raise ValueError("Message content invalid or too long")
        
        return True
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Sanitize input text"""
        # Remove excessive÷ ÷    whitespace
        text = ' '.join(text.split())
        
        # Truncate if too long
        if len(text) > 10000:
            text = text[:10000] + "..."
        
        return text


class OutputGuardrail:
    """Validate and fix LLM output"""
    
    @staticmethod
    def parse_and_validate(response: str) -> ScamAnalysis:
        """Parse LLM response and validate structure"""
        try:
            # Try to parse JSON
            data = json.loads(response)
            
            # Validate with Pydantic
            analysis = ScamAnalysis(**data)
            return analysis
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}")
        except Exception as e:
            raise ValueError(f"Invalid analysis structure: {e}")
    
    @staticmethod
    def ensure_safety(analysis: ScamAnalysis) -> ScamAnalysis:
        """Ensure output doesn't contain harmful content"""
        # Remove any potential PII from evidence
        for indicator in analysis.indicators:
            # Redact potential phone numbers, emails, etc.
            indicator.evidence = OutputGuardrail._redact_pii(indicator.evidence)
        
        return analysis
    
    @staticmethod
    def _redact_pii(text: str) -> str:
        """Redact PII from text"""
        import re
        # Redact emails
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        # Redact phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
        # Redact SSN
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)
        return text