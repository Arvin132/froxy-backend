from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate


SCAM_DETECTION_SYSTEM = """You are an expert scam detection AI assistant. Your job is to analyze 
conversations and identify potential fraud or scam attempts.

You have access to a knowledge base of known scam patterns and tactics through the context provided.

When analyzing conversations, you should:
1. Look for urgency and pressure tactics
2. Identify requests for money or sensitive information
3. Check for impersonation attempts
4. Evaluate if offers seem too good to be true
5. Consider the overall context and flow of the conversation

Provide your analysis in the following JSON format:
{{
    "risk_score": <0-100>,
    "risk_level": "<safe|low|medium|high|critical>",
    "is_likely_scam": <true|false>,
    "indicators": [
        {{
            "type": "<indicator_type>",
            "severity": "<low|medium|high|critical>",
            "description": "<description>",
            "evidence": "<quote from conversation>"
        }}
    ],
    "summary": "<brief summary>",
    "recommendations": ["<recommendation1>", "<recommendation2>"]
}}

Be thorough but objective. Explain your reasoning clearly."""


SCAM_EXAMPLES = [
    {
        "conversation": """User: Hello
Other: Hi! I'm calling from Microsoft. Your computer has a virus.
Other: You need to give me remote access immediately to fix it.
Other: Also send $299 via gift card for the security software.""",
        "analysis": """{{
    "risk_score": 95,
    "risk_level": "critical",
    "is_likely_scam": true,
    "indicators": [
        {{
            "type": "impersonation",
            "severity": "critical",
            "description": "Claims to be from Microsoft (common tech support scam)",
            "evidence": "I'm calling from Microsoft"
        }},
        {{
            "type": "urgency",
            "severity": "high",
            "description": "Creating false urgency about computer virus",
            "evidence": "Your computer has a virus... immediately"
        }},
        {{
            "type": "payment_request",
            "severity": "critical",
            "description": "Requesting payment via gift card (major red flag)",
            "evidence": "send $299 via gift card"
        }}
    ],
    "summary": "Classic tech support scam with impersonation, false urgency, and suspicious payment method",
    "recommendations": [
        "Do NOT provide remote access to your computer",
        "Do NOT send any money or gift cards",
        "Hang up immediately and report to FTC",
        "Microsoft does not make unsolicited calls"
    ]
}}"""
    },
    {
        "conversation": """User: Hey, are we still on for coffee tomorrow?
Other: Yes! Looking forward to it. 2pm at the usual place?
User: Perfect, see you then!""",
        "analysis": """{{
    "risk_score": 0,
    "risk_level": "safe",
    "is_likely_scam": false,
    "indicators": [],
    "summary": "Normal friendly conversation about meeting up. No suspicious indicators.",
    "recommendations": [
        "This conversation appears safe",
        "Continue as normal"
    ]
}}"""
    }
]

example_prompt = PromptTemplate(
    input_variables=["conversation", "analysis"],
    template="Conversation:\n{conversation}\n\nAnalysis:\n{analysis}"
)

few_shot_prompt = FewShotPromptTemplate(
    examples=SCAM_EXAMPLES,
    example_prompt=example_prompt,
    prefix=SCAM_DETECTION_SYSTEM + "\n\nHere are some examples:\n",
    suffix="\n\nNow analyze this conversation:\n\nConversation:\n{conversation}\n\nAnalysis:",
    input_variables=["conversation"]
)
