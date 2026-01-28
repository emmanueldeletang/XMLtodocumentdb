"""
Script to load XML file, convert to dict/JSON, and load into DocumentDB (MongoDB API)
Database: loto
Collection: configurable
Account: sbi6na5irt4te
"""

import xml.etree.ElementTree as ET
import json
from pymongo import MongoClient
from typing import Any, Dict, List, Union
import os


# MongoDB (Cosmos DB for MongoDB API) configuration - defaults
MONGO_CONNECTION_STRING = "mongodb+srv://user:password@account.mongo.cosmos.azure.com/..."
DATABASE_NAME = "your"


def get_collection_name_from_file(file_path: str) -> str:
    """Extract collection name from file name (without extension)."""
    base_name = os.path.basename(file_path)
    collection_name = os.path.splitext(base_name)[0]
    # Sanitize: replace spaces and special chars with underscores
    collection_name = collection_name.replace(" ", "_").replace("-", "_")
    return collection_name


def xml_to_dict(element: ET.Element) -> Union[Dict, str, None]:
    """
    Recursively convert an XML element to a dictionary.
    Handles attributes, text content, and nested elements.
    """
    result = {}
    
    # Add element attributes with '@' prefix
    if element.attrib:
        for key, value in element.attrib.items():
            result[f"@{key}"] = value
    
    # Process child elements
    children = list(element)
    
    if children:
        child_dict = {}
        for child in children:
            child_data = xml_to_dict(child)
            child_tag = child.tag
            
            # Handle multiple children with same tag (convert to list)
            if child_tag in child_dict:
                # Convert to list if not already
                if not isinstance(child_dict[child_tag], list):
                    child_dict[child_tag] = [child_dict[child_tag]]
                child_dict[child_tag].append(child_data)
            else:
                child_dict[child_tag] = child_data
        
        result.update(child_dict)
    
    # Handle text content
    text = element.text
    if text and text.strip():
        if result:
            # Has both attributes/children and text
            result["#text"] = text.strip()
        else:
            # Only text content
            return text.strip()
    
    return result if result else None


def load_xml_file(file_path: str) -> ET.Element:
    """Load and parse XML file."""
    print(f"📂 Loading XML file: {file_path}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"XML file not found: {file_path}")
    
    tree = ET.parse(file_path)
    root = tree.getroot()
    print(f"   Root element: <{root.tag}>")
    
    return root


def convert_xml_to_dict(root: ET.Element) -> Dict:
    """Convert XML root element to dictionary (single document)."""
    print("🔄 Converting XML to dictionary...")
    
    result = {root.tag: xml_to_dict(root)}
    
    print("   Conversion complete!")
    return result


def convert_xml_to_documents(root: ET.Element) -> List[Dict]:
    """
    Convert each child element of the root into a separate document.
    Each child becomes one JSON document for MongoDB.
    """
    print("🔄 Converting XML to individual documents...")
    
    documents = []
    children = list(root)
    
    for child in children:
        doc = xml_to_dict(child)
        if doc is not None:
            # Add the element tag as a type identifier
            if isinstance(doc, dict):
                doc['_type'] = child.tag
            else:
                doc = {'_type': child.tag, 'value': doc}
            documents.append(doc)
    
    print(f"   Converted {len(documents)} documents!")
    return documents


def save_to_json(data: Dict, json_file_path: str) -> str:
    """Save dictionary to JSON file."""
    print(f"💾 Saving to JSON file: {json_file_path}")
    
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("   JSON file saved!")
    return json_file_path


def load_to_mongodb(data: Dict, collection_name: str, connection_string: str, database_name: str):
    """Load JSON data into MongoDB (DocumentDB)."""
    print(f"🔌 Connecting to MongoDB (DocumentDB)...")
    client = MongoClient(connection_string)
    
    db = client[database_name]
    collection = db[collection_name]
    
    print(f"   Database: {database_name}")
    print(f"   Collection: {collection_name}")
    
    # Insert the document
    print("📤 Inserting document...")
    
    # Handle if data is a list or single document
    if isinstance(data, list):
        result = collection.insert_many(data)
        print(f"   Inserted {len(result.inserted_ids)} documents")
    else:
        result = collection.insert_one(data)
        print(f"   Inserted document with ID: {result.inserted_id}")
    
    client.close()
    print("   Connection closed.")
    
    return result


def extract_items_from_dict(data: Dict, item_key: str = None) -> List[Dict]:
    """
    Extract list of items from nested dictionary.
    Useful when XML contains repeated elements that should be separate documents.
    """
    if item_key and item_key in data:
        items = data[item_key]
        if isinstance(items, list):
            return items
        else:
            return [items]
    return [data]


def process_xml_to_mongodb(
    xml_file_path: str,
    json_output_path: str = None,
    collection_name: str = None,
    connection_string: str = None,
    database_name: str = None,
    save_json: bool = True
):
    """
    Main function to process XML file and load into MongoDB.
    Each child element of the XML root becomes a separate document.
    
    Args:
        xml_file_path: Path to the XML file
        json_output_path: Optional path for JSON output file
        collection_name: MongoDB collection name (default: derived from file name)
        connection_string: MongoDB connection string (default: DEFAULT_CONNECTION_STRING)
        database_name: MongoDB database name (default: DEFAULT_DATABASE)
        save_json: Whether to save intermediate JSON file
    """
    # Use defaults if not provided
    connection_string = connection_string or DEFAULT_CONNECTION_STRING
    database_name = database_name or DEFAULT_DATABASE
    print("\n" + "="*60)
    print("🚀 XML TO MONGODB LOADER")
    print("="*60)
    
    # Derive collection name from file if not provided
    if not collection_name:
        collection_name = get_collection_name_from_file(xml_file_path)
    
    print(f"📁 File: {xml_file_path}")
    print(f"📦 Collection: {collection_name}")
    print(f"🗃️  Database: {database_name}")
    
    # Step 1: Load XML
    root = load_xml_file(xml_file_path)
    
    # Step 2: Convert each child element to a separate document
    documents = convert_xml_to_documents(root)
    
    # Step 3: Save to JSON (optional)
    if save_json:
        if not json_output_path:
            base_name = os.path.splitext(xml_file_path)[0]
            json_output_path = f"{base_name}.json"
        save_to_json(documents, json_output_path)
    
    # Step 4: Load to MongoDB
    if documents:
        load_to_mongodb(documents, collection_name, connection_string, database_name)
    else:
        print("⚠️  No documents to insert!")
    
    print("\n" + "="*60)
    print("✅ PROCESS COMPLETE!")
    print("="*60 + "\n")
    
    return documents


# Example usage and CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Load XML to MongoDB (DocumentDB)')
    parser.add_argument('xml_file', help='Path to the XML file')
    parser.add_argument('--connection-string', '-s', default=None,
                        help='MongoDB connection string (default: built-in connection string)')
    parser.add_argument('--database', '-d', default=None,
                        help=f'MongoDB database name (default: {DEFAULT_DATABASE})')
    parser.add_argument('--collection', '-c', default=None, 
                        help='MongoDB collection name (default: derived from XML file name)')
    parser.add_argument('--json-output', '-j', help='Path for JSON output file')
    parser.add_argument('--no-json', action='store_true', 
                        help='Skip saving JSON file')
    
    args = parser.parse_args()
    
    # Use file name as collection name if not specified
    collection_name = args.collection or get_collection_name_from_file(args.xml_file)
    
    process_xml_to_mongodb(
        xml_file_path=args.xml_file,
        json_output_path=args.json_output,
        collection_name=collection_name,
        connection_string=args.connection_string,
        database_name=args.database,
        save_json=not args.no_json
    )
