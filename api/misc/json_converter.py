from bson import ObjectId


def flatten_object_id(doc):
    if isinstance(doc, dict):
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                doc[key] = str(value)
            elif isinstance(value, dict):
                flatten_object_id(value)
            elif isinstance(value, list):
                for item in value:
                    flatten_object_id(item)
    return doc
