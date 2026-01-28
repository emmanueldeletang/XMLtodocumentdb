# XML to MongoDB Loader

A Python script to load XML files into Azure Cosmos DB for MongoDB (DocumentDB).

## Features

- 📂 **Parse XML files** - Reads any XML file and converts to JSON
- 📄 **One document per element** - Each child element of the XML root becomes a separate MongoDB document
- 🏷️ **Auto-naming** - Collection name is derived from the XML file name
- 💾 **JSON export** - Optionally saves the converted data as a JSON file
- 🔗 **Azure Cosmos DB** - Connects to Cosmos DB for MongoDB API

## Prerequisites

```bash
pip install pymongo
```

## Configuration

Edit the connection settings in `xml_to_mongodb.py`:

```python
MONGO_CONNECTION_STRING = "mongodb+srv://user:password@account.mongo.cosmos.azure.com/..."
DATABASE_NAME = "loto"
```

## Usage

### Basic Usage

```bash
python xml_to_mongodb.py <xml_file>
```

The collection name will be derived from the file name (e.g., `catalog.xml` → collection `catalog`).

### Examples

```bash
# Load catalog.xml into 'catalog' collection
python xml_to_mongodb.py catalog.xml

# Specify a custom collection name
python xml_to_mongodb.py data.xml --collection my_collection

# Specify output JSON file path
python xml_to_mongodb.py data.xml --json-output output/data.json

# Skip JSON file creation
python xml_to_mongodb.py data.xml --no-json
```

### Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `xml_file` | | Path to the XML file (required) |
| `--connection-string` | `-s` | MongoDB connection string |
| `--database` | `-d` | MongoDB database name (default: `loto`) |
| `--collection` | `-c` | MongoDB collection name (default: derived from file name) |
| `--json-output` | `-j` | Path for JSON output file |
| `--no-json` | | Skip saving JSON file |

### Examples

```bash
# Load catalog.xml into 'catalog' collection (using default connection)
python xml_to_mongodb.py catalog.xml

# Specify connection string and database
python xml_to_mongodb.py data.xml --connection-string "mongodb://user:pass@host:port" --database mydb

# Short form
python xml_to_mongodb.py data.xml -s "mongodb://user:pass@host:port" -d mydb -c mycollection

# Specify a custom collection name
python xml_to_mongodb.py data.xml --collection my_collection

# Specify output JSON file path
python xml_to_mongodb.py data.xml --json-output output/data.json

# Skip JSON file creation
python xml_to_mongodb.py data.xml --no-json
```

## How It Works

### XML to Documents Conversion

Given this XML file (`books.xml`):

```xml
<?xml version="1.0"?>
<catalog>
    <book id="1">
        <title>Python Programming</title>
        <author>John Doe</author>
        <price>29.99</price>
    </book>
    <book id="2">
        <title>MongoDB Guide</title>
        <author>Jane Smith</author>
        <price>39.99</price>
    </book>
</catalog>
```

The script creates **2 separate documents** in MongoDB:

```json
{
    "_type": "book",
    "@id": "1",
    "title": "Python Programming",
    "author": "John Doe",
    "price": "29.99"
}
```

```json
{
    "_type": "book",
    "@id": "2",
    "title": "MongoDB Guide",
    "author": "Jane Smith",
    "price": "39.99"
}
```

### Conversion Rules

| XML Feature | JSON Representation |
|-------------|---------------------|
| Element tag | `_type` field |
| Attributes | Prefixed with `@` (e.g., `@id`) |
| Text content | Direct value or `#text` if mixed |
| Nested elements | Nested objects |
| Repeated elements | Arrays |

## Output

```
============================================================
🚀 XML TO MONGODB LOADER
============================================================
📁 File: catalog.xml
📦 Collection: catalog
📂 Loading XML file: catalog.xml
   Root element: <catalog>
🔄 Converting XML to individual documents...
   Converted 12 documents!
💾 Saving to JSON file: catalog.json
   JSON file saved!
🔌 Connecting to MongoDB (DocumentDB)...
   Database: loto
   Collection: catalog
📤 Inserting document...
   Inserted 12 documents
   Connection closed.

============================================================
✅ PROCESS COMPLETE!
============================================================
```

## Project Structure

```
loto/
├── xml_to_mongodb.py      # Main script
├── README.md              # This file
├── catalog.xml            # Example XML file
└── catalog.json           # Generated JSON output
```

## License

MIT License
