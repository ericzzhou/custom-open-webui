import os
import pandas as pd
import tiktoken

from graphrag.query.indexer_adapters import read_indexer_entities, read_indexer_reports
from graphrag.query.llm.oai.chat_openai import ChatOpenAI
from graphrag.query.llm.oai.typing import OpenaiApiType
from graphrag.query.structured_search.global_search.community_context import (
    GlobalCommunityContext,
)
from graphrag.query.structured_search.global_search.search import GlobalSearch


class GraphRagGlobalSearchEngine:
    def __init__(self, input_dir="./inputs/artifacts"):
        self.api_key = os.environ["GRAPHRAG_API_KEY"]
        self.llm_model = os.environ["GRAPHRAG_LLM_MODEL"]

        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model=self.llm_model,
            api_type=OpenaiApiType.OpenAI,  # OpenaiApiType.OpenAI or OpenaiApiType.AzureOpenAI
            max_retries=20,
        )

        self.token_encoder = tiktoken.get_encoding("cl100k_base")
        self.INPUT_DIR = input_dir
        self.COMMUNITY_REPORT_TABLE = "create_final_community_reports"
        self.ENTITY_TABLE = "create_final_nodes"
        self.ENTITY_EMBEDDING_TABLE = "create_final_entities"
        self.COMMUNITY_LEVEL = 2

        self._load_data()
        self._initialize_context_builder()
        self._initialize_search_engine()

    def _load_data(self):
        self.entity_df = pd.read_parquet(f"{self.INPUT_DIR}/{self.ENTITY_TABLE}.parquet")
        self.report_df = pd.read_parquet(f"{self.INPUT_DIR}/{self.COMMUNITY_REPORT_TABLE}.parquet")
        self.entity_embedding_df = pd.read_parquet(f"{self.INPUT_DIR}/{self.ENTITY_EMBEDDING_TABLE}.parquet")

        self.reports = read_indexer_reports(self.report_df, self.entity_df, self.COMMUNITY_LEVEL)
        self.entities = read_indexer_entities(self.entity_df, self.entity_embedding_df, self.COMMUNITY_LEVEL)

        print(f"Total report count: {len(self.report_df)}")
        print(f"Report count after filtering by community level {self.COMMUNITY_LEVEL}: {len(self.reports)}")
        self.report_df.head()

    def _initialize_context_builder(self):
        self.context_builder_params = {
            "use_community_summary": False,
            "shuffle_data": True,
            "include_community_rank": True,
            "min_community_rank": 0,
            "community_rank_name": "rank",
            "include_community_weight": True,
            "community_weight_name": "occurrence weight",
            "normalize_community_weight": True,
            "max_tokens": 12_000,
            "context_name": "Reports",
        }

        self.context_builder = GlobalCommunityContext(
            community_reports=self.reports,
            entities=self.entities,
            token_encoder=self.token_encoder,
        )

    def _initialize_search_engine(self):
        map_llm_params = {
            "max_tokens": 1000,
            "temperature": 0.0,
            "response_format": {"type": "json_object"},
        }

        reduce_llm_params = {
            "max_tokens": 2000,
            "temperature": 0.0,
        }

        self.search_engine = GlobalSearch(
            llm=self.llm,
            context_builder=self.context_builder,
            token_encoder=self.token_encoder,
            max_data_tokens=12_000,
            map_llm_params=map_llm_params,
            reduce_llm_params=reduce_llm_params,
            allow_general_knowledge=False,
            json_mode=True,
            context_builder_params=self.context_builder_params,
            concurrent_coroutines=32,
            response_type="multiple paragraphs",
        )

    async def search(self, query):
        result = await self.search_engine.asearch(query)
        return result.response


if __name__ == "__main__":
    engine = GraphRagGlobalSearchEngine()

    import asyncio

    async def main():
        query_1 = "三体的故事脉络?"
        # query_1 = "庆余年这本书讲的什么?"
        # query_1 = "怎么学好机器学习?"
        result_1 = await engine.search(query_1)
        print(result_1)

    asyncio.run(main())