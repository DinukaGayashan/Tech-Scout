import pymongo
import json
from datetime import datetime

def retrieve(collection):
    documents = collection.find()
    docs_list = list(documents)
    for doc in docs_list:
        doc['_id'] = str(doc['_id'])
    return docs_list

def retrieve_all(collection_names):

    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['TechScoutRelational']

    data_dict = {}

    for collection_name in collection_names:
        collection = db[collection_name]
        data_dict[collection_name] = retrieve(collection)

    json_data = json.dumps(data_dict, indent=4)
    
    return json_data

categories = ["CPU", "VideoCard", "Memory", "Motherboard", "Monitor", "Keyboard"]


