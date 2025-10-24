from .schemas import ChatMessage
from collections import defaultdict
import re

def parse_telegram_chat(content: str) -> ChatMessage:
    pattern = r'(?=^.+, \[.+\])'
    tokens = re.split(pattern, content, flags=re.MULTILINE)
    tokens = [message.strip() for message in tokens if message.strip() != ""]
    messages = []
    lengthTable = defaultdict(int)
    for token in tokens:
        try:
            parts = token.split('\n')
            header = parts[0].strip(); body = parts[1]
            headerParts = header.split(',')
            name = headerParts[0]
            lengthTable[name] += len(body)
            messages.append((name, body))
        except Exception:
            pass
    min_key = min(lengthTable, key=lengthTable.get)
    
    return [ChatMessage(sender="user" if name == min_key else "other", content=message) for name, message in messages]
    
    


def parse_whatsapp_chat(content: str) -> ChatMessage:
    pattern = r'(?=\[\d{1,2}:\d{2}\s(?:AM|PM),\s\d{1,2}/\d{1,2}/\d{4}\]\s[^:]+:\s)'
    messages = re.split(pattern, content)
    messages = [msg.strip() for msg in messages if msg.strip()]
    
    
    extraction_pattern = r'^\[.*?\]\s*([^:]+):\s*(.*)$'
    parsed_data = []
    lengthTable = defaultdict(int)
    for message in messages:
        match = re.match(extraction_pattern, message, re.DOTALL)
        if match:
            name = match.group(1).strip()
            body = match.group(2).strip()
            lengthTable[name] += len(body)
            parsed_data.append((name, body))
    min_key = min(lengthTable, key=lengthTable.get)
    
    return [ChatMessage(sender="user" if name == min_key else "other", content=message) for name, message in parsed_data]

def parse_default_chat(content: str) -> ChatMessage:
    
    return [
        ChatMessage(
            sender="other",
            content=content
        )
    ]


parser_table = {
    "telegram": parse_telegram_chat,
    "whatsapp": parse_whatsapp_chat,
    "plain": parse_default_chat
}


def parse_chat(chat_content: str, platform: str) -> list[ChatMessage]:
    parser_f = parser_table.get(platform, parse_default_chat)
    return parser_f(chat_content)

if __name__ == "__main__":
    content = """
    [2:25 PM, 8/27/2025] Behnaz: اره این گروه قبلی منه
    [2:25 PM, 8/27/2025] Behnaz: باید رزومتو بفرستی
    [6:25 AM, 9/5/2025] Behnaz: a29asgha@uwaterloo.ca

    ✅ 250 $

    E: Saman Mansour
    F: Behnaz Ahmadi ???

    Pass: saman
    [1:51 PM, 9/5/2025] Behnaz: a29asgha@uwaterloo.ca

    ✅ 288 $

    E: Mahdad Mohri
    F:Behnaz Ahmadi

    Pass: Nikan
    [10:39 PM, 9/5/2025] Behnaz: a29asgha@uwaterloo.ca

    ✅ 390 $

    E: Romina Zaree
    F: Behnaz Ahmadi
    """
    print(parse_whatsapp_chat(content))