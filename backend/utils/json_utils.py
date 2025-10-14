"""
JSON utilities for handling MongoDB ObjectId serialization
"""
from bson import ObjectId
from datetime import datetime
import json

def serialize_document(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    
    if isinstance(doc, list):
        return [serialize_document(item) for item in doc]
    
    if isinstance(doc, dict):
        serialized = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                serialized[key] = str(value)
            elif isinstance(value, datetime):
                serialized[key] = value.isoformat()
            elif isinstance(value, dict):
                serialized[key] = serialize_document(value)
            elif isinstance(value, list):
                serialized[key] = serialize_document(value)
            else:
                serialized[key] = value
        return serialized
    
    return doc

def json_response(data, status_code=200):
    """Create a JSON response with proper serialization"""
    serialized_data = serialize_document(data)
    return json.dumps(serialized_data), status_code, {'Content-Type': 'application/json'}
