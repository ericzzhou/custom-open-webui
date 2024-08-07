from services.graphrag_global_search import GraphRagGlobalSearchEngine
from services.graphrag_local_search import GraphRagLocalSearchEngine


class GraphRagService:
    def __init__(self, model_id):
        self.model_id = model_id
        # connections.connect(alias="default", host="44.236.217.101", port="19530")

    async def run(self, prompt):

        print(f"prompt:{prompt},从elk里查询到数据")
        global_search_engine = GraphRagGlobalSearchEngine()
        local_search_engine = GraphRagLocalSearchEngine()

        local_result = await local_search_engine.search(prompt)

        global_result = await global_search_engine.search(prompt)

        result = f"""
        <h2>Global Search</h2>
        {global_result}

        <h2>Local Search</h2>
        {local_result.response}
"""
        return result
