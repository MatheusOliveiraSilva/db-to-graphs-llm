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

llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
llm_transformer = LLMGraphTransformer(llm=llm)

graph = Neo4jGraph(refresh_schema=True)

def initialize_db_graph_transformer():
    return LLMGraphTransformer(
        llm=llm,
        prompt=DB_GRAPH_PROMPT,
        allowed_nodes=["TABLE", "COLUMN"],
        allowed_relationships=["HAS_COLUMN", "FOREIGN_KEY_TO", "RELATES_TO"],
        #node_properties=[
        #    "table_name", "columns", "primary_key", "foreign_keys", "table_description",
        #    "column_name", "data_type", "is_nullable", "is_primary_key", "is_foreign_key", "column_description"
        #]
    )

def create_db_graph(db_schema, llm_transformer):
    langchain_documents = [Document(page_content=db_schema)]
    graph_from_docs = llm_transformer.convert_to_graph_documents(langchain_documents)
    return graph_from_docs

def send_to_neo4j(graph, kb):
    graph.add_graph_documents(kb, include_source=True)

if __name__ == "__main__":
    db_schema = MONDIAL_SCHEMA
    db_graph_builder = initialize_db_graph_transformer()
    kb = create_db_graph(db_schema, db_graph_builder)
    send_to_neo4j(graph, kb)
