import pymongo
import sys
from cellarmasterwines import dict_all_wine, dict_all_spirit


try:
    client = pymongo.MongoClient("mongodb+srv://issacchl2002:hackathon@200ok.oqe8x.mongodb.net/?retryWrites=true&w=majority&appName=200ok")
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)


db = client.wine

# Collections
wine_collection = db["wines"]
spirit_collection = db["spirits"]

def replace_or_insert_data(collection, data, unique_key):
    for item in data:
        filter_query = {unique_key: item[unique_key]}
        
        try:
            # replace or insert
            collection.replace_one(filter_query, item, upsert=True)
            print(f"Replaced/Inserted document with {unique_key}={item[unique_key]} in {collection.name}")
        except Exception as e:
            print(f"An error occurred while replacing/inserting data in {collection.name}: {e}")


replace_or_insert_data(wine_collection, dict_all_wine, "wine_name")

replace_or_insert_data(spirit_collection, dict_all_spirit, "spirit_name")  # Adjust the unique key as needed