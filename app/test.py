from app.agents.scam_agent import ScamDetectionAgent 
from app.api.schemas import ChatAnalysisRequest, ChatMessage
from dotenv import load_dotenv
import os
import asyncio

async def main():
    load_dotenv()
    agent = ScamDetectionAgent(os.environ.get("MOORCHEH_KEY"))
    request = ChatAnalysisRequest(
        messages= [
            ChatMessage(sender='user', content='Hello who is this?'),
            ChatMessage(sender='other', content="Hello please send me all of your information and Insurance Number!! Ill send you $100 with ")
        ],
        platform= "Facebook marketplace"
    ) 
    response = await agent.analyze(request.messages, request.platform)
    print(response)
if __name__ == "__main__":
    asyncio.run(main())