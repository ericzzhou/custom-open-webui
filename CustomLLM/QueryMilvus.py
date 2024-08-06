import time
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
import uuid
from typing import Optional, List
import logging

# 日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()
PORT = 8765


# 数据模型
class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    stop: Optional[List[str]] = None
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0


class ChatCompletionChoice(BaseModel):
    text: str
    index: int
    logprobs: Optional[dict] = None
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{uuid.uuid4().hex}")
    object: str = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[ChatCompletionChoice]
    usage: Usage
    system_fingerprint: Optional[str] = None


# @app.route("/v1/models", methods=["GET"])
@app.get("/v1/models")
async def list_models():
    current_time = int(time.time())
    available_models = [
        {
            "id": "milvus:yami_keyword_embedding",
            "object": "model",
            "created": current_time - 100000,
            "owned_by": "yami@eric",
            "description": "从 Milvus 读取数据",
        },
        {
            "id": "milvus:yami_image_embedding_vit",
            "object": "model",
            "created": current_time - 100000,
            "owned_by": "yami@eric",
            "description": "从 Milvus 读取数据",
        },
    ]
    return {"object": "list", "data": available_models}


# 模拟的聊天功能
def generate_response(prompt, model_id="mock-model-v1"):
    # 这里可以是一个复杂的生成逻辑，比如基于模型的回答
    return f"Response from {model_id}: Echo: {prompt}"


def load_user_prompt(request: ChatCompletionRequest):
    user_message_content = None
    for message in request.messages:
        if message.role == "user":
            user_message_content = message.content
            break
    return user_message_content


@app.post("/v1/chat/completions")
async def chat(request: ChatCompletionRequest):

    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages are required")
    if not request.model:
        raise HTTPException(status_code=400, detail="Model and messages are required")

    logger.info(f"收到聊天完成请求：{request}")
    model_id = request.model
    prompt = load_user_prompt(request)  # 使用消息列表的第一个消息的内容作为 prompt
    response = generate_response(prompt=prompt, model_id=model_id)

    return ChatCompletionResponse(
        model=model_id,
        choices=[
            ChatCompletionChoice(
                text=response,
                index=0,
                logprobs=None,
                finish_reason="length",
            )
        ],
        usage=Usage(
            prompt_tokens=len(prompt), completion_tokens=0, total_tokens=len(prompt)
        ),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
