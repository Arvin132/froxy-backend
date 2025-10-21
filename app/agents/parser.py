from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from .guards import ScamAnalysis
import json, re
        

class ScamAnalysisParser:
    
    def __init__(self):
        self.pydantic_parser = PydanticOutputParser(pydantic_object=ScamAnalysis)
    
    def parse(self, text: str) -> ScamAnalysis:
        
        try:    
            data = json.loads(text)
            return ScamAnalysis(**data)
        except:
            try:
                return self.pydantic_parser.parse(text)
            except Exception as e:
                return self._extract_and_parse(text)
    
    def _extract_and_parse(self, text: str) -> ScamAnalysis:
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            data = json.loads(json_str)
            return ScamAnalysis(**data)
        
        raise ValueError("Could not extract valid JSON from response")