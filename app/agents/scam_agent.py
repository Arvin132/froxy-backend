from moorcheh_sdk import MoorchehClient
from .prompts import few_shot_prompt, SCAM_DETECTION_SYSTEM
from .guards import InputGuardrail, OutputGuardrail, ScamAnalysis
from .parser import ScamAnalysisParser


class ScamDetectionAgent:
    """
    LangChain-powered agent that uses Moorcheh for LLM calls
    """
    
    def __init__(self, moorcheh_key: str, namespace: str = "scam_detection"):
        self.moorcheh = MoorchehClient(moorcheh_key)
        self.namespace = namespace    
        self.input_guard = InputGuardrail()
        self.output_guard = OutputGuardrail()
        self.parser = ScamAnalysisParser()
        
    def _format_message(self, m):
        return f"{m.sender} : {m.content}"
    
    async def analyze(self, messages: list, platform) -> ScamAnalysis:
        try:    
            self.input_guard.validate_messages(messages)
            conversation = '\n'.join([self._format_message(m) for m in messages])
            
            prompt = ("Platform:  %s \n\n" % platform) + few_shot_prompt.format(conversation=conversation)
            response = self.moorcheh.get_generative_answer(
                namespace=self.namespace,
                query=prompt,
                temperature=0.2
            )
            
            answer = response.get('answer', {})
            
            answer_parsed = self.parser.parse(text=answer)
            self.output_guard.ensure_safety(answer_parsed)
            
            return {
                "success": True,
                "analysis": answer_parsed,
                "raw_response": answer,
                "prompt": prompt,
                "model": response['model']
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e) 
            }
        