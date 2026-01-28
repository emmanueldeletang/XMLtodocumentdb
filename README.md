# XML to MongoDB Loader & Exporter

A Python script to import XML files into Azure Cosmos DB for MongoDB (DocumentDB) and export collections back to XML.

## Features

- 📂 **Import XML files** - Reads any XML file and loads into MongoDB
- 📤 **Export to XML** - Export MongoDB collections back to XML files
- 📄 **One document per element** - Each child element of the XML root becomes a separate MongoDB document
- 🏷️ **Auto-naming** - Collection name is derived from the XML file name
- 🔗 **Azure Cosmos DB** - Connects to Cosmos DB for MongoDB API

## Prerequisites

```bash
pip install pymongo
```

## Usage

### Import XML to MongoDB

```bash
python xml_to_mongodb.py import <xml_file> [options]
```

**Examples:**

```bash
# Import catalog.xml into 'catalog' collection
python xml_to_mongodb.py import catalog.xml

# Specify database and collection
python xml_to_mongodb.py import data.xml -d mydb -c my_collection

# Specify connection string
python xml_to_mongodb.py import data.xml -s "mongodb://user:pass@host:port"

# Skip JSON file creation
python xml_to_mongodb.py import data.xml --no-json
```

**Import Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `xml_file` | | Path to the XML file (required) |
| `--connection-string` | `-s` | MongoDB connection string |
| `--database` | `-d` | MongoDB database name (default: `loto`) |
| `--collection` | `-c` | MongoDB collection name (default: derived from file name) |
| `--json-output` | `-j` | Path for JSON output file |
| `--no-json` | | Skip saving JSON file |

### Export MongoDB to XML

```bash
python xml_to_mongodb.py export <collection> [options]
```

**Examples:**

```bash
# Export 'catalog' collection to catalog.xml
python xml_to_mongodb.py export catalog

# Specify output file
python xml_to_mongodb.py export catalog --output backup.xml

# Specify database and connection
python xml_to_mongodb.py export catalog -d mydb -s "mongodb://..."

# Custom root tag
python xml_to_mongodb.py export catalog --root-tag catalog
```

**Export Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `collection` | | MongoDB collection name (required) |
| `--output` | `-o` | XML output file path (default: collection_name.xml) |
| `--connection-string` | `-s` | MongoDB connection string |
| `--database` | `-d` | MongoDB database name (default: `loto`) |
| `--root-tag` | `-r` | Root element tag name (default: `root`) |

## How It Works

### XML to Documents Conversion (Import)

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

### Documents to XML Conversion (Export)

When exporting, the documents are converted back to XML:
- `_type` field determines the element tag name
- `@` prefixed fields become XML attributes
- Other fields become child elements

### Conversion Rules

| XML Feature | JSON Representation |
|-------------|---------------------|
| Element tag | `_type` field |
| Attributes | Prefixed with `@` (e.g., `@id`) |
| Text content | Direct value or `#text` if mixed |
| Nested elements | Nested objects |
| Repeated elements | Arrays |

## Output Examples

### Import Output

```
============================================================
🚀 XML TO MONGODB LOADER
============================================================
📁 File: catalog.xml
📦 Collection: catalog
🗃️  Database: loto
📂 Loading XML file: catalog.xml
   Root element: <catalog>
🔄 Converting XML to individual documents...
   Converted 12 documents!
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

### Export Output

```
============================================================
📤 MONGODB TO XML EXPORTER
============================================================
📦 Collection: catalog
🗃️  Database: loto
📁 Output: catalog.xml
🔌 Connecting to MongoDB (DocumentDB)...
   Database: loto
   Collection: catalog
📥 Fetching documents...
   Fetched 12 documents
   Connection closed.
🔄 Converting to XML...
💾 Saving XML file: catalog.xml
   XML file saved!

============================================================
✅ EXPORT COMPLETE!
============================================================
```

## Project Structure

```
loto/
├── xml_to_mongodb.py      # Main script
├── README.md              # This file
├── catalog.xml            # Example XML file
└── backup.xml             # Exported XML file
```

## License

MIT License
