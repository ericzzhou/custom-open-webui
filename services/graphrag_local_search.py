import os
import pandas as pd
import tiktoken
from graphrag.query.context_builder.entity_extraction import EntityVectorStoreKey
from graphrag.query.indexer_adapters import (
    read_indexer_covariates,
    read_indexer_entities,
    read_indexer_relationships,
    read_indexer_reports,
    read_indexer_text_units,
)
from graphrag.query.input.loaders.dfs import (
    store_entity_semantic_embeddings,
)
from graphrag.query.llm.oai.chat_openai import ChatOpenAI
from graphrag.query.llm.oai.embedding import OpenAIEmbedding
from graphrag.query.llm.oai.typing import OpenaiApiType
from graphrag.query.structured_search.local_search.mixed_context import (
    LocalSearchMixedContext,
)
from graphrag.query.structured_search.local_search.search import LocalSearch
from graphrag.vector_stores.lancedb import LanceDBVectorStore


class GraphRagLocalSearchEngine:
    def __init__(self, input_dir="./inputs/artifacts"):
        self.INPUT_DIR = input_dir
        self.LANCEDB_URI = f"{self.INPUT_DIR}/lancedb"

        self.COMMUNITY_REPORT_TABLE = "create_final_community_reports"
        self.ENTITY_TABLE = "create_final_nodes"
        self.ENTITY_EMBEDDING_TABLE = "create_final_entities"
        self.RELATIONSHIP_TABLE = "create_final_relationships"
        self.COVARIATE_TABLE = "create_final_covariates"
        self.TEXT_UNIT_TABLE = "create_final_text_units"
        self.COMMUNITY_LEVEL = 2

        self._load_data()
        self._initialize_vector_store()
        self._store_embeddings()
        self._initialize_llm_and_context_builder()
        self._initialize_search_engine()

    def _load_data(self):
        self.entity_df = pd.read_parquet(f"{self.INPUT_DIR}/{self.ENTITY_TABLE}.parquet")
        self.entity_embedding_df = pd.read_parquet(f"{self.INPUT_DIR}/{self.ENTITY_EMBEDDING_TABLE}.parquet")
        self.entities = read_indexer_entities(self.entity_df, self.entity_embedding_df, self.COMMUNITY_LEVEL)

        self.relationship_df = pd.read_parquet(f"{self.INPUT_DIR}/{self.RELATIONSHIP_TABLE}.parquet")
        self.relationships = read_indexer_relationships(self.relationship_df)

        self.covariate_df = pd.read_parquet(f"{self.INPUT_DIR}/{self.COVARIATE_TABLE}.parquet")
        self.covariates = {"claims": read_indexer_covariates(self.covariate_df)}

        self.report_df = pd.read_parquet(f"{self.INPUT_DIR}/{self.COMMUNITY_REPORT_TABLE}.parquet")
        self.reports = read_indexer_reports(self.report_df, self.entity_df, self.COMMUNITY_LEVEL)

        self.text_unit_df = pd.read_parquet(f"{self.INPUT_DIR}/{self.TEXT_UNIT_TABLE}.parquet")
        self.text_units = read_indexer_text_units(self.text_unit_df)

    def _initialize_vector_store(self):
        self.description_embedding_store = LanceDBVectorStore(collection_name="entity_description_embeddings")
        self.description_embedding_store.connect(db_uri=self.LANCEDB_URI)

    def _store_embeddings(self):
        store_entity_semantic_embeddings(self.entities, self.description_embedding_store)

    def _initialize_llm_and_context_builder(self):
        api_key = os.environ["GRAPHRAG_API_KEY"]
        llm_model = os.environ["GRAPHRAG_LLM_MODEL"]
        embedding_model = os.environ["GRAPHRAG_EMBEDDING_MODEL"]

        self.llm = ChatOpenAI(
            api_key=api_key,
            model=llm_model,
            api_type=OpenaiApiType.OpenAI,
            max_retries=20,
        )

        self.token_encoder = tiktoken.get_encoding("cl100k_base")

        self.text_embedder = OpenAIEmbedding(
            api_key=api_key,
            api_base=None,
            api_type=OpenaiApiType.OpenAI,
            model=embedding_model,
            deployment_name=embedding_model,
            max_retries=20,
        )

        self.context_builder_params = {
            "text_unit_prop": 0.5,
            "community_prop": 0.1,
            "conversation_history_max_turns": 5,
            "conversation_history_user_turns_only": True,
            "top_k_mapped_entities": 10,
            "top_k_relationships": 10,
            "include_entity_rank": True,
            "include_relationship_weight": True,
            "include_community_rank": False,
            "return_candidate_context": False,
            "embedding_vectorstore_key": EntityVectorStoreKey.ID,
            "max_tokens": 12_000,
        }

        self.context_builder = LocalSearchMixedContext(
            community_reports=self.reports,
            text_units=self.text_units,
            entities=self.entities,
            relationships=self.relationships,
            covariates=self.covariates,
            entity_text_embeddings=self.description_embedding_store,
            embedding_vectorstore_key=EntityVectorStoreKey.ID,
            text_embedder=self.text_embedder,
            token_encoder=self.token_encoder,
        )

    def _initialize_search_engine(self):
        self.llm_params = {
            "max_tokens": 2_000,
            "temperature": 0.0,
        }

        self.search_engine = LocalSearch(
            llm=self.llm,
            context_builder=self.context_builder,
            token_encoder=self.token_encoder,
            llm_params=self.llm_params,
            context_builder_params=self.context_builder_params,
            response_type="multiple paragraphs",
        )

    async def search(self, query):
        result = await self.search_engine.asearch(query)
        return result


if __name__ == "__main__":
    engine = GraphRagLocalSearchEngine()

    import asyncio

    # query_1 = "三体的故事脉络?"
    query_1 = "三体中谁遭到了什么迫害"
    query_1 = "三体中最悲惨的人是谁"
    query_1 = "庆余年这本书讲的什么?"
    result_1 = asyncio.run(engine.search(query_1))
    print(result_1.response)

    # query_2 = "Tell me about Dr. Jordan Hayes"
    # result_2 = asyncio.run(engine.search(query_2))
    # print(result_2)