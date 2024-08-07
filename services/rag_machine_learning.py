class RAGMachineLearningService:
    def __init__(self, model_id):
        self.model_id = model_id

        # 全局变量，用于存储搜索引擎和问题生成器
        self.local_search_engine = None
        self.global_search_engine = None
        self.guestion_generator = None

    def run(self, prompt):
        return f"prompt:{prompt},面向所有人的机器学习科普知识库"
