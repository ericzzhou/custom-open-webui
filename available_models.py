from enum import Enum
import os


class AvailableModels(Enum):
    QueryItemFromMilvus = "milvus:yami_test_item_zh_embedding"
    LogAnalysis = "elk:Log_analysis"
    GraphRAGFiction = "graphrag:fiction"
    # GraphRAGYamiCustomerService = "graphrag:Yami客服简单版"
    # GraphRAGYamiCustomerServiceTuning = "graphrag:Yami客服微调版"


def get_subdirectories(directory):
    """
    获取指定目录下的所有一级子目录。

    :param directory: 目标目录的路径
    :return: 一级子目录列表
    """
    try:
        # 列出目录中的所有项
        items = os.listdir(directory)

        # 过滤出所有的目录项
        subdirectories = [
            item for item in items if os.path.isdir(os.path.join(directory, item))
        ]

        return subdirectories
    except Exception as e:
        print(f"Error: {e}")
        return []


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
        # {
        #     "id": AvailableModels.GraphRAGFiction.value,
        #     "object": "model",
        #     "created": current_time - 100000,
        #     "owned_by": "yami@eric",
        #     "description": "Graph RAG demo ,包含4本书：面向所有人的机器学习科普大全、庆余年、三体、Christmas Carol",
        # },
        # {
        #     "id": AvailableModels.GraphRAGYamiCustomerService.value,
        #     "object": "model",
        #     "created": current_time - 100000,
        #     "owned_by": "yami@eric",
        #     "description": "Graph RAG 包含Yami 智能客服简单版语料库",
        # },
        # {
        #     "id": AvailableModels.GraphRAGYamiCustomerService.value,
        #     "object": "model",
        #     "created": current_time - 100000,
        #     "owned_by": "yami@eric",
        #     "description": "Graph RAG 包含Yami 智能客服微调版语料库",
        # },
    ]

    subdirs = get_subdirectories("./inputs")
    if subdirs:
        for subdir in subdirs:
            available_models.append(
                {
                    "id": f"知识库:{subdir}",
                    "object": "model",
                    "created": current_time - 100000,
                    "owned_by": "yami@eric",
                    "description": f"从 {subdir} 读取数据",
                }
            )
    else:
        print("inputs目录下没有子目录")

    return available_models
