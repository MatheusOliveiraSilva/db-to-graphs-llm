from langchain_core.prompts import SystemMessagePromptTemplate, PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

DB_GRAPH_STRUCTURE = SystemMessagePromptTemplate.from_template("""
# Knowledge Graph Construction Instructions for Database Tables

## 1. Overview
You are tasked with constructing a knowledge graph from descriptive information about database tables. Each table's information is provided in **chunks** separated by `---chunk---`. Your job is to extract and structure the data into a knowledge graph format. 

- The graph must be accurate and consistent with the information provided.
- **Nodes** should represent database elements such as TABLES and COLUMNS.
- **Relationships** should capture the connections between nodes, such as foreign key associations or columns belonging to tables.

---

## 2. Nodes and Their Attributes
1. **TABLE**: Represents a database table.
   - **Node ID**: Use the table name as the ID (e.g., "Country", "City").
   - **Attributes**:
     - `table_name`: The name of the table.
     - `columns`: A list of column names in the table.
     - `primary_key`: A list of column(s) that make up the primary key.
     - `foreign_keys`: A list of foreign keys and their referenced tables (if any).
     - `table_description`: A brief description of the table's purpose.

2. **COLUMN**: Represents a column in a table.
   - **Node ID**: Use the format `table.column` as the ID (e.g., "City.Name").
   - **Attributes**:
     - `column_name`: The name of the column.
     - `data_type`: The data type of the column (e.g., VARCHAR, FLOAT).
     - `is_nullable`: Whether the column allows NULL values (assume nullable if not explicitly stated).
     - `is_primary_key`: Whether the column is part of the primary key.
     - `is_foreign_key`: Whether the column is a foreign key.
     - `column_description`: A brief description of the column's purpose.

---

## 3. Relationships
1. **HAS_COLUMN**: Connects a `TABLE` node to its respective `COLUMN` nodes.
2. **FOREIGN_KEY_TO**: Connects a `COLUMN` node representing a foreign key to another `COLUMN` node in the referenced table.
3. **RELATES_TO**: Connects two `TABLE` nodes that have foreign key associations.

---

## 4. Input Structure
The input consists of multiple **chunks**, each describing a database table. The chunks are separated by `---chunk---`. Your job is to process each chunk independently and extract nodes and relationships as described.

---

## 5. Output Format
Provide the knowledge graph in the following format:

### Nodes
- Node ID: `<Node_ID>`
  - `attribute_1`: `<value>`
  - `attribute_2`: `<value>`
  - ...

### Relationships
- Relationship Type: `<Relationship_Type>`
  - Source: `<Source_Node_ID>`
  - Target: `<Target_Node_ID>`

---

## Example Input
---chunk---
The table Country represents countries and their key attributes. Its primary key, CountryKey, uniquely identifies each entry using the column Code (a 4-character code, VARCHAR(4)). The table includes the following columns: Name (VARCHAR(35)), which is a unique identifier for the country's name; Capital (VARCHAR(35)), indicating the capital city; Province (VARCHAR(35)), specifying a province within the country; Area (FLOAT), which records the total area of the country; and Population (INT), representing the number of inhabitants. Constraints ensure data validity: CountryArea requires the Area to be non-negative, and CountryPop ensures the Population is non-negative.
---chunk---

### Example Output
#### Nodes
- Node ID: `Country`
  - `table_name`: "Country"
  - `columns`: ["Code", "Name", "Capital", "Province", "Area", "Population"]
  - `primary_key`: ["Code"]
  - `foreign_keys`: []
  - `table_description`: "Represents countries and their key attributes."

- Node ID: `Country.Code`
  - `column_name`: "Code"
  - `data_type`: "VARCHAR(4)"
  - `is_nullable`: false
  - `is_primary_key`: true
  - `is_foreign_key`: false
  - `column_description`: "A 4-character code that uniquely identifies the country."

- Node ID: `Country.Name`
  - `column_name`: "Name"
  - `data_type`: "VARCHAR(35)"
  - `is_nullable`: true
  - `is_primary_key`: false
  - `is_foreign_key`: false
  - `column_description`: "A unique identifier for the country's name."

#### Relationships
- Relationship Type: `HAS_COLUMN`
  - Source: `Country`
  - Target: `Country.Code`

- Relationship Type: `HAS_COLUMN`
  - Source: `Country`
  - Target: `Country.Name`

---

## Task
Based on the descriptive chunks provided, construct the knowledge graph with nodes and relationships using the format above.
""")

DB_GRAPH_STRUCTURE_TIP = HumanMessagePromptTemplate(
    prompt=PromptTemplate.from_template("""
Ensure you extract all relevant information from each chunk and strictly adhere to the format and rules provided above. Focus on:
1. Identifying TABLE nodes with all attributes (`table_name`, `columns`, `primary_key`, etc.).
2. Identifying COLUMN nodes with their attributes (`column_name`, `data_type`, etc.).
3. Creating appropriate relationships (`HAS_COLUMN`, `FOREIGN_KEY_TO`, `RELATES_TO`).
Use consistent node and relationship naming conventions. Based on the input chunk below, construct the graph:
{input}
""")
)

DB_GRAPH_PROMPT = ChatPromptTemplate.from_messages([DB_GRAPH_STRUCTURE, DB_GRAPH_STRUCTURE_TIP])
