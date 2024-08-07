def generate_available_models(current_itme: int):
    available_models = [
        {
            "id": "milvus:yami_test_item_zh_embedding",
            "object": "model",
            "created": current_itme - 100000,
            "owned_by": "yami@eric",
            "description": "从 Milvus 读取数据",
        },
        # {
        #     "id": "milvus:yami_image_embedding_vit",
        #     "object": "model",
        #     "created": current_time - 100000,
        #     "owned_by": "yami@eric",
        #     "description": "从 Milvus 读取数据",
        # },
    ]
    return available_models
