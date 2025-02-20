def serialize_doc(doc):
    """ Converts MongoDB document to JSON serializable format """
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc
