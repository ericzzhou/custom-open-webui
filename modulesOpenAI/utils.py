# 模拟的聊天功能
import re
from modulesOpenAI.ChatCompletion import ChatCompletionRequest


def format_response(response):
    paragraphs = re.split(r"\n{2,}", response)
    formatted_paragraphs = []
    for para in paragraphs:
        if "```" in para:
            parts = para.split("```")
            for i, part in enumerate(parts):
                if i % 2 == 0:  # 代码块
                    parts[i] = f"\n```\n{part.strip()}\n```\n"
            para = "".join(parts)
        else:
            para = para.replace(". ", ".\n")

        formatted_paragraphs.append(para.strip())
    return "\n\n".join(formatted_paragraphs)


def load_user_prompt(request: ChatCompletionRequest):
    user_message_content = None
    for message in request.messages:
        if message.role == "user":
            user_message_content = message.content
            break
    return user_message_content

