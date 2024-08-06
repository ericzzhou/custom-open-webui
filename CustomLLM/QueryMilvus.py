import time
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
import uuid
from typing import Generator, Optional, List
import logging
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType
import requests

# 日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()
PORT = 8765


connections.connect(alias="default", host="44.236.217.101", port="19530")


def get_vector_embedding(keyword):
    # 定义请求的 URL 和参数
    url = f"https://bge.yamibuy.net/zh/bge/vector"
    params = {"keyword": keyword}

    try:
        # 发送 GET 请求
        response = requests.get(url, params=params)

        # 检查响应状态码
        response.raise_for_status()

        # 返回 JSON 数据
        return response.json()

    except requests.RequestException as e:
        # 处理请求异常
        print(f"请求错误: {e}")
        return None


def convert_string_to_float_array(embedding_str):
    """
    将包含浮点数的字符串转换为浮点数数组

    参数:
    embedding_str (str): 包含浮点数的字符串，每个浮点数由逗号分隔

    返回:
    List[float]: 转换后的浮点数数组
    """
    # 将字符串分割成列表
    embedding_list = embedding_str.split(",")

    # 将列表中的字符串转换为浮点数
    embedding_floats = [float(num) for num in embedding_list]

    return embedding_floats


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
            "id": "milvus:yami_test_item_zh_embedding",
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
    milvus_collection_name = model_id.split(":")[1].strip()

    db = Collection(name=milvus_collection_name)
    print("schema \n")
    print(db.schema)
    # 加载集合
    db.load()

    print(f"集合 {milvus_collection_name} 已加载")

    query_vector = get_vector_embedding(prompt)["data"]
    embedding_list = convert_string_to_float_array(query_vector)
    print("完成keyword向量化")
    search_param = {
        "metric_type": "COSINE",
        "index_type": "IVF_FLAT",
        "params": {"nprobe": 10},
    }

    results = db.search(
        data=[embedding_list],
        anns_field="embedding",  # 向量字段名称
        param=search_param,
        limit=10,
        expr=None,
        output_fields=["item_number"],
    )
    print("milvus 查询完成")
    items = []
    for result in results:
        for hit in result:
            goods_number = hit.entity.get("item_number")
            items.append(goods_number)
            print(goods_number)

    # 查询数据库

    # # 这里可以是一个复杂的生成逻辑，比如基于模型的回答
    # return f"Response from {model_id}: Echo: {prompt},Result:{results}"
    return " \n ".join(items)  # 或者使用其他合适的连接符号


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
