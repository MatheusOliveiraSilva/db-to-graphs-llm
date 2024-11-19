from langchain_core.prompts import ChatPromptTemplate

DATA_AUGMENTATION_PROMPT = ChatPromptTemplate.from_template("""
Your task is to transform database schema definitions into a concise, descriptive story in English. The goal is to describe the structure of the table and its columns in a way that conveys key technical details while remaining simple and easy to follow. Focus on creating an explanation that can be used to generate knowledge graph nodes and relationships.

### Rules
1. Start with a brief description of the table, including its name and purpose.
2. Mention the primary key explicitly and describe how it uniquely identifies entries in the table.
3. Describe each column succinctly, mentioning its name, data type, and purpose, where applicable.
4. Highlight any relationships (e.g., foreign keys) and constraints in plain language.
5. Use concise sentences and avoid redundant or overly detailed explanations.

### Example Input
CREATE TABLE politics
(Country VARCHAR(4),
 Independence DATE,
 Dependent VARCHAR(4),
 Government VARCHAR(120),
 CONSTRAINT PoliticsKey PRIMARY KEY(Country));

### Example Output
The table Politics represents countries and their political attributes. Its primary key, PoliticsKey, uniquely identifies each entry using the column Country (a 4-character code, VARCHAR(4)). The table includes the following columns: Independence (DATE), which records the date of a country's independence; Dependent (VARCHAR(4)), indicating any dependency relationships; and Government (VARCHAR(120)), describing the type of government. The column Country also serves as a foreign key to connect with other tables.

### Example Input
CREATE TABLE river
(Name VARCHAR(35),
 River VARCHAR(35),
 Lake VARCHAR(35),
 Sea VARCHAR(35),
 Length FLOAT,
 SourceLongitude FLOAT,
 SourceLatitude FLOAT,
 Mountains VARCHAR(35),
 SourceAltitude FLOAT,
 EstuaryLongitude FLOAT,
 EstuaryLatitude FLOAT,
 CONSTRAINT RiverKey PRIMARY KEY(Name),
 CONSTRAINT RiverLength CHECK (Length >= 0),
 CONSTRAINT SourceCoord
     CHECK ((SourceLongitude >= -180) AND 
            (SourceLongitude <= 180) AND
            (SourceLatitude >= -90) AND
            (SourceLatitude <= 90)),
 CONSTRAINT EstCoord
     CHECK ((EstuaryLongitude >= -180) AND 
            (EstuaryLongitude <= 180) AND
            (EstuaryLatitude >= -90) AND
            (EstuaryLatitude <= 90)));

### Example Output
The table River represents rivers and their geographical attributes. Its primary key, RiverKey, uniquely identifies each entry using the column Name (VARCHAR(35)). It includes the following columns: River (VARCHAR(35)), related to another river; Lake (VARCHAR(35)), linked to a lake; Sea (VARCHAR(35)), associated with a sea; and Length (FLOAT), which specifies the river's length. Additional columns capture geographical data, such as SourceLongitude (FLOAT) and SourceLatitude (FLOAT) for the river's source, as well as EstuaryLongitude (FLOAT) and EstuaryLatitude (FLOAT) for its estuary. Constraints ensure valid data: RiverLength requires Length to be non-negative, SourceCoord ensures valid latitude and longitude for the source, and EstCoord ensures valid latitude and longitude for the estuary.

### Task
Based on the following input, transform it into a concise story format as described above:
{input_schema}
""")
