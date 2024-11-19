import os
import re
import requests
import urllib.parse
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from prompts.db_to_graphs_prompt_v0 import DB_GRAPH_PROMPT
from schemas.mondial_schema import MONDIAL_SCHEMA

load_dotenv()

class DBToGraph:
    def __init__(self, schema):
        # Modify temperature and model_name experimentally if need some improvements.
        self.llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o")

        # To use the neo4j graph, need to run neo4j.sh script. (for more info see README.md)
        self.graph = Neo4jGraph()

        # Chunk the schema into langchain documents for each "CREATE TABLE".
        self.schema_documents = self.transform_schema_to_langchain_documents(schema)

        # Initialize the LLMGraphTransformer with the DB_GRAPH_PROMPT and create KB, after this send for Neo4j.
        self.llm_transformer = self.initialize_db_graph_transformer()
        self.kb = self.create_db_graph()
        self.send_to_neo4j()

    def initialize_db_graph_transformer(self):
        return LLMGraphTransformer(
            llm=self.llm,
            prompt=DB_GRAPH_PROMPT,
            allowed_nodes=["TABLE", "COLUMN"],
            allowed_relationships=["HAS_COLUMN", "FOREIGN_KEY_TO", "RELATES_TO"],
            node_properties=[
                "table_name", "columns", "primary_key", "foreign_keys", "table_description",
                "column_name", "data_type", "is_nullable", "is_primary_key", "is_foreign_key", "column_description"
             ]
        )

    @staticmethod
    def transform_schema_to_langchain_documents(schema):
        langchain_documents = []

        tables = schema.split("CREATE TABLE")
        for table in tables:
            langchain_documents.append(Document(page_content=f"CREATE TABLE {table}"))
        return langchain_documents

    def create_db_graph(self):
        langchain_documents = self.schema_documents
        graph_from_docs = self.llm_transformer.convert_to_graph_documents(langchain_documents)
        return graph_from_docs

    def send_to_neo4j(self):
        self.graph.add_graph_documents(self.kb, include_source=True)

if __name__ == "__main__":
    db_to_graph = DBToGraph(MONDIAL_SCHEMA)
    print("Graph created successfully!")
