from langchain_core.prompts import SystemMessagePromptTemplate, PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

DB_GRAPH_STRUCTURE = SystemMessagePromptTemplate.from_template("""
Your task is to construct a knowledge graph from the provided descriptive text about database tables. This graph must include only the elements and relationships explicitly described below. Do not create any additional nodes or relationships that are not part of this structure.

### Nodes
1. **TABLE**: Represents a database table.
   - **Node ID**: Use the table name as the ID.
   - **Attributes**:
     - `table_name`: The name of the table.
     - `columns`: A list of column names in the table.
     - `primary_key`: A list of column(s) that make up the primary key.
     - `foreign_keys`: A list of foreign keys and their referenced tables.
     - `table_description`: A brief description of the table's purpose.

2. **COLUMN**: Represents a column in a table.
   - **Node ID**: Use the format `table.column` as the ID.
   - **Attributes**:
     - `column_name`: The name of the column.
     - `data_type`: The data type of the column.
     - `is_nullable`: Whether the column allows NULL values (if not explicitly stated, assume nullable).
     - `is_primary_key`: Whether the column is part of the primary key.
     - `is_foreign_key`: Whether the column is a foreign key.
     - `column_description`: A brief description of the column's purpose.

### Relationships
1. **HAS_COLUMN**: Connects a `TABLE` node to its respective `COLUMN` nodes.
2. **FOREIGN_KEY_TO**: Connects a `COLUMN` node representing a foreign key to another `COLUMN` node in the referenced table.
3. **RELATES_TO**: Connects two `TABLE` nodes that have foreign key associations.

### Rules:
- Extract all relevant information from the descriptive text provided.
- Ensure that all nodes and relationships follow the specified structure exactly.
- If the text does not explicitly state certain attributes (e.g., `is_nullable`), assume default values where appropriate.
- Do not create any additional nodes or relationships beyond what is described above.

Now, based on the provided descriptive text, extract the elements and construct the graph in the required format.
""")

DB_GRAPH_STRUCTURE_TIP = HumanMessagePromptTemplate(
    prompt=PromptTemplate.from_template("""
Carefully extract information from the descriptive text and strictly adhere to the specified graph structure.
Remember:
- Only use the node types: TABLE, COLUMN.
- Only use the relationship types: HAS_COLUMN, FOREIGN_KEY_TO, RELATES_TO.
- Do not create any additional nodes or relationships beyond what is explicitly stated.
Provide the graph in the correct format based on this input: {input}
""")
)

DB_GRAPH_PROMPT = ChatPromptTemplate.from_messages([DB_GRAPH_STRUCTURE, DB_GRAPH_STRUCTURE_TIP])
