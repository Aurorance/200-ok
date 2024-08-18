import pandas as pd
import pymongo
import sys

# Function to read CSV and replace the collection in MongoDB
def replace_collection_from_csv(csv_file, db, collection_name):
    df = pd.read_csv(csv_file, encoding='utf-8')
    
    data = df.to_dict(orient='records')
    
    collection = db[collection_name]

    collection.drop()
    
    # Insert the new data
    collection.insert_many(data)
    
    print(f"Uploaded {len(data)} records to the '{collection_name}' collection in the '{db.name}' database.")

# Step 1: Connect to MongoDB
try:
    client = pymongo.MongoClient("mongodb+srv://issacchl2002:hackathon@200ok.oqe8x.mongodb.net/?retryWrites=true&w=majority&appName=200ok")
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)

db = client['wine']  # Connect to the 'wine' database

# Step 2: Replace the 'hist_spirits' collection with 'hist_spirit_data.csv'
replace_collection_from_csv('hist_spirit_data.csv', db, 'hist_spirits')

# Step 3: Replace the 'hist_wine' collection with 'hist_wine_data.csv'
replace_collection_from_csv('hist_wine_data.csv', db, 'hist_wine')