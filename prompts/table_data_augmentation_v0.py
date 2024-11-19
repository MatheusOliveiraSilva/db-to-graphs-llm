from langchain_core.prompts import ChatPromptTemplate

DATA_AUGMENTATION_PROMPT = ChatPromptTemplate.from_template("""
Your task is to transform database schema definitions into a concise, descriptive story in English. The goal is to describe the structure of the table and its columns in a way that conveys key technical details while remaining simple and easy to follow. Focus on creating an explanation that can be used to generate knowledge graph nodes and relationships, **explicitly detailing any foreign keys and their connections to other tables. Foreign keys must be identified explicitly, even if only implied by the schema**.

### Rules
1. Start with a brief description of the table, including its name and purpose.
2. Mention the primary key explicitly and describe how it uniquely identifies entries in the table.
3. For each column:
   - Mention its name, data type, and purpose, where applicable.
   - If the column is a foreign key, describe:
     - Which table and column it references.
     - Its role in establishing relationships.
4. Highlight all constraints (e.g., primary keys, foreign keys, or check constraints) in plain language.
5. **If a column can be interpreted as a foreign key based on its name (e.g., "Country" likely referencing the "country" table), treat it as a foreign key unless explicitly stated otherwise.**
6. Use concise sentences and avoid redundant or overly detailed explanations.

### Example Input
CREATE TABLE geo_river
(River VARCHAR(35),
 Country VARCHAR(4),
 Province VARCHAR(35),
 CONSTRAINT GRiverKey PRIMARY KEY (Province, Country, River));

### Example Output
The table Geo_River captures information about rivers and their geographical locations. Its primary key, GRiverKey, uniquely identifies each entry using a combination of the columns Province (VARCHAR(35)), Country (VARCHAR(4)), and River (VARCHAR(35)). The column Country (VARCHAR(4)) serves as a foreign key referencing the column Code in the Country table, linking each river to its respective country. Similarly, the column Province (VARCHAR(35)) serves as a foreign key referencing the column Name in the Province table, associating each river with a specific province within the country.

### Example Input
CREATE TABLE geo_sea
(Sea VARCHAR(35),
 Country VARCHAR(4),
 Province VARCHAR(35),
 CONSTRAINT GSeaKey PRIMARY KEY (Province, Country, Sea));

### Example Output
The table Geo_Sea stores data about seas and their geographical locations. Its primary key, GSeaKey, uniquely identifies each entry using the columns Province (VARCHAR(35)), Country (VARCHAR(4)), and Sea (VARCHAR(35)). The column Country (VARCHAR(4)) is a foreign key referencing the column Code in the Country table, linking each sea to its respective country. The column Province (VARCHAR(35)) is a foreign key referencing the column Name in the Province table, identifying the province associated with the sea.

### Task
Based on the following input, transform it into a concise story format as described above, making sure to explicitly identify all foreign keys and their relationships, even when implied by column names:
{input_schema}
""")
