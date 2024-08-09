from services.graphrag_global_search import GraphRagGlobalSearchEngine
from services.graphrag_local_search import GraphRagLocalSearchEngine


class GraphRagService:
    def __init__(self, model_id):
        self.model_id = model_id
        # connections.connect(alias="default", host="44.236.217.101", port="19530")

    async def run_Fictio(self, prompt):

        print(f"prompt:{prompt},从 graph rag查询数据")
        global_search_engine = GraphRagGlobalSearchEngine(input_dir="./inputs/小说/artifacts")
        local_search_engine = GraphRagLocalSearchEngine(input_dir="./inputs/小说/artifacts")

        local_result = await local_search_engine.search(prompt)

        global_result = await global_search_engine.search(prompt)

        result = f"""
        # 🌏🌏🌏🌏🌏🌏全局搜索结果🌏🌏🌏🌏🌏🌏

        {global_result}

        # 🔍🔍🔍🔍🔍🔍精细搜索结果🔍🔍🔍🔍🔍🔍
        
        {local_result.response}
"""
        return result

    async def run_YamiCS(self, prompt):

        print(f"prompt:{prompt},从 graph rag查询数据")
        global_search_engine = GraphRagGlobalSearchEngine(input_dir="./inputs/Yami客服语料库/artifacts")
        local_search_engine = GraphRagLocalSearchEngine(input_dir="./inputs/Yami客服语料库/artifacts")

        local_result = await local_search_engine.search(prompt)

        global_result = await global_search_engine.search(prompt)

        result = f"""
        # 🌏🌏🌏🌏🌏🌏全局搜索结果🌏🌏🌏🌏🌏🌏

        {global_result}

        # 🔍🔍🔍🔍🔍🔍精细搜索结果🔍🔍🔍🔍🔍🔍
        
        {local_result.response}
"""
        return result
    
    async def run_YamiCSTuning(self, prompt):

        print(f"prompt:{prompt},从 graph rag查询数据")
        global_search_engine = GraphRagGlobalSearchEngine(input_dir="./inputs/Yami客服语料库微调版/artifacts")
        local_search_engine = GraphRagLocalSearchEngine(input_dir="./inputs/Yami客服语料库微调版/artifacts")

        local_result = await local_search_engine.search(prompt)

        global_result = await global_search_engine.search(prompt)

        result = f"""
        # 🌏🌏🌏🌏🌏🌏全局搜索结果🌏🌏🌏🌏🌏🌏

        {global_result}

        # 🔍🔍🔍🔍🔍🔍精细搜索结果🔍🔍🔍🔍🔍🔍
        
        {local_result.response}
"""
        return result