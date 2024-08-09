from services.graphrag_global_search import GraphRagGlobalSearchEngine
from services.graphrag_local_search import GraphRagLocalSearchEngine
import os


class GraphRagService:
    def __init__(self, model_id):
        self.model_id = model_id
        # connections.connect(alias="default", host="44.236.217.101", port="19530")

    async def run_Fictio(self, prompt):

        print(f"prompt:{prompt},从 graph rag查询数据")
        global_search_engine = GraphRagGlobalSearchEngine(
            input_dir="./inputs/小说/artifacts"
        )
        local_search_engine = GraphRagLocalSearchEngine(
            input_dir="./inputs/小说/artifacts"
        )

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
        global_search_engine = GraphRagGlobalSearchEngine(
            input_dir="./inputs/Yami客服语料库/artifacts"
        )
        local_search_engine = GraphRagLocalSearchEngine(
            input_dir="./inputs/Yami客服语料库/artifacts"
        )

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
        global_search_engine = GraphRagGlobalSearchEngine(
            input_dir="./inputs/Yami客服语料库微调版/artifacts"
        )
        local_search_engine = GraphRagLocalSearchEngine(
            input_dir="./inputs/Yami客服语料库微调版/artifacts"
        )

        local_result = await local_search_engine.search(prompt)

        global_result = await global_search_engine.search(prompt)

        result = f"""
        # 🌏🌏🌏🌏🌏🌏全局搜索结果🌏🌏🌏🌏🌏🌏

        {global_result}

        # 🔍🔍🔍🔍🔍🔍精细搜索结果🔍🔍🔍🔍🔍🔍
        
        {local_result.response}
"""
        return result

    def is_directory_empty(self, directory_path):
        # 判断指定路径是否为空目录
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            return not os.listdir(directory_path)
        else:
            return True
            # raise FileNotFoundError(
            #     f"目录 '{directory_path}' 不存在或不是一个有效的目录。"
            # )

    async def runDynamicKnowledgeBase(self, prompt):

        # 知识库目录
        knowledgeDir = self.model_id.split(":")[1]

        print(f"从 {knowledgeDir}查询数据, 用户问题：{prompt}")

        knowledgeArtifacts = f"./inputs/{knowledgeDir}/artifacts"
        if self.is_directory_empty(knowledgeArtifacts):
            print(f"目录 '{knowledgeArtifacts}' 不存在或不是一个有效的目录。")
            return f"知识库文件目录 '{knowledgeDir}' 不存在，请先生成 '{knowledgeDir}' 的知识库"

        global_search_engine = GraphRagGlobalSearchEngine(input_dir=knowledgeArtifacts)
        local_search_engine = GraphRagLocalSearchEngine(input_dir=knowledgeArtifacts)

        local_result = await local_search_engine.search(prompt)

        global_result = await global_search_engine.search(prompt)

        result = f"""
        # 🌏🌏🌏🌏🌏🌏全局搜索结果🌏🌏🌏🌏🌏🌏

        {global_result}

        # 🔍🔍🔍🔍🔍🔍精细搜索结果🔍🔍🔍🔍🔍🔍
        
        {local_result.response}
"""
        return result
