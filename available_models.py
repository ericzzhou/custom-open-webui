from enum import Enum


class AvailableModels(Enum):
    QueryItemFromMilvus = "milvus:yami_test_item_zh_embedding"
    LogAnalysis = "elk:Log_analysis"
    GraphRAGDemo = "rag:graph_rag_demo"


def generate_available_models(current_time: int):
    available_models = [
        {
            "id": AvailableModels.QueryItemFromMilvus.value,
            "object": "model",
            "created": current_time - 100000,
            "owned_by": "yami@eric",
            "description": "从 Milvus 读取数据",
        },
        {
            "id": AvailableModels.LogAnalysis.value,
            "object": "model",
            "created": current_time - 100000,
            "owned_by": "yami@eric",
            "description": "从 elk 读取并分析日志",
        },
        {
            "id": AvailableModels.GraphRAGDemo.value,
            "object": "model",
            "created": current_time - 100000,
            "owned_by": "yami@eric",
            "description": "Graph RAG demo ,包含4本书：面向所有人的机器学习科普大全、庆余年、三体、Christmas Carol",
        },
    ]
    return available_models
