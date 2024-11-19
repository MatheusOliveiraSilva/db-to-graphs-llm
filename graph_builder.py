import os
import re
import requests
import urllib.parse
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from prompts.db_to_graphs_prompt_v1 import DB_GRAPH_PROMPT
from prompts.table_data_augmentation_v0 import DATA_AUGMENTATION_PROMPT
from schemas.mondial_schema import MONDIAL_SCHEMA

load_dotenv()

class DBToGraph:
    def __init__(self, schema):
        # Modify temperature and model_name experimentally if need some improvements.
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-4o")

        # To use the neo4j graph, need to run neo4j.sh script. (for more info see README.md)
        self.graph = Neo4jGraph(refresh_schema=True)

        # Initialize the LLMGraphTransformer with the DB_GRAPH_PROMPT and create KB, after this send for Neo4j.
        self.llm_transformer = self.initialize_db_graph_transformer()

        # Augment the table infos with the LLM model and make langchain documents about it.
        self.augmented_schema_chunks = self.transform_schema_to_langchain_documents(schema)

    def initialize_db_graph_transformer(self):
        return LLMGraphTransformer(
            llm=self.llm,
            prompt=DB_GRAPH_PROMPT,
            allowed_nodes=["TABLE", "COLUMN"],
            allowed_relationships=["IS_COLUMN_OF", "FOREIGN_KEY_OF"],
            node_properties=[
                "table_name", "columns", "primary_key", "foreign_keys", "table_description",
                "column_name", "data_type", "is_nullable", "is_primary_key", "is_foreign_key", "column_description"
            ]
        )

    def augment_table_infos(self, table_infos):
        chain = DATA_AUGMENTATION_PROMPT | self.llm | StrOutputParser()
        return chain.invoke({"input_schema": table_infos})

    def transform_schema_to_langchain_documents(self, schema):
        langchain_documents = []
        augmented_infos_path = "schemas/augmented_schema.txt"

        tables = schema.split("CREATE TABLE")

        if not os.path.exists(augmented_infos_path):
            print("No augmented infos found, creating new chunks...")
            # write augmented infos to file.
            with open(augmented_infos_path, "w") as file:
                for table in tables:
                    augmented_schema_chunk = self.augment_table_infos(f"CREATE TABLE {table}")
                    file.write(augmented_schema_chunk)
                    file.write("\n---new-table-chunk---\n")
                    langchain_documents.append(Document(page_content=augmented_schema_chunk))
        else:
            with open(augmented_infos_path, "r") as file:
                augmented_schema_chunk = file.read()
                chunks = augmented_schema_chunk.split("\n---new-table-chunk---\n")
                for chunk in chunks:
                    langchain_documents.append(Document(page_content=chunk))
        return langchain_documents

    def create_kg(self):
        for chunk in self.augmented_schema_chunks:
            print("Chunk:", chunk)
            graph_from_docs = self.llm_transformer.convert_to_graph_documents([chunk])
            self.graph.add_graph_documents(graph_from_docs, include_source=True)

if __name__ == "__main__":
    db_to_graph = DBToGraph(MONDIAL_SCHEMA)
    db_to_graph.create_kg()
    print("Graph created successfully!")
