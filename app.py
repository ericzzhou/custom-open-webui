import asyncio
import json
import logging
import uuid
from fastapi import FastAPI, HTTPException
import time

from fastapi.responses import JSONResponse, StreamingResponse

from available_models import generate_available_models
from modulesOpenAI.ChatCompletion import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    Message,
    Usage,
)
from modulesOpenAI.utils import format_response, load_user_prompt
from services.query_milvus import query_items_from_milvus

# 日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


app = FastAPI()
PORT = 8765

async def generate_response_handler(prompt, model_id):
    if model_id == "milvus:yami_test_item_zh_embedding":
        return query_items_from_milvus(prompt, model_id)
    return

@app.get("/v1/models")
async def list_models():
    current_time = int(time.time())
    available_models = generate_available_models(current_time)
    return {"object": "list", "data": available_models}


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):

    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages are required")
    if not request.model:
        raise HTTPException(status_code=400, detail="Model and messages are required")

    logger.info(f"收到聊天完成请求：{request}")
    model_id = request.model
    prompt = load_user_prompt(request)  # 使用消息列表的第一个消息的内容作为 prompt
    response = await generate_response_handler(prompt=prompt, model_id=model_id)

    forrmatted_response = format_response(response)
    logger.info(f"格式化的搜索结果：{forrmatted_response}")

    if request.stream:

        async def stream_generator():
            chunk_id = f"chatcmpl-{uuid.uuid4().hex}"
            lines = forrmatted_response.split("\n")
            for i, line in enumerate(lines):
                chunk = {
                    "id": chunk_id,
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": model_id,
                    "choices": [
                        {
                            "index": 0,
                            "delta": (
                                {"content": line + "\n"}
                                if i > 0
                                else {"role": "assistant", "content": line}
                            ),
                            "finish_reason": None,
                        }
                    ],
                }
                yield f"data: {json.dumps(chunk)}\n\n"
                await asyncio.sleep(0.05)

            final_chunk = {
                "id": chunk_id,
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": model_id,
                "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
            }

            yield f"data: {json.dumps(final_chunk)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(stream_generator(), media_type="text/event-stream")
    else:

        chatResponse = ChatCompletionResponse(
            model=model_id,
            choices=[
                ChatCompletionResponseChoice(
                    index=0,
                    message=Message(role="assistant", content=forrmatted_response),
                    finish_reason="stop",
                )
            ],
            usage=Usage(
                prompt_tokens=len(prompt.split()),
                completion_tokens=len(forrmatted_response.split()),
                total_tokens=len(prompt.split()) + len(forrmatted_response.split()),
            ),
        )

        logger.info(f"发送响应：{chatResponse}")
        return JSONResponse(content=chatResponse.dict())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
