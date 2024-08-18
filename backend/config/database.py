from pymongo import MongoClient

client = MongoClient("mongodb+srv://mark:hackathon@200ok.oqe8x.mongodb.net/?retryWrites=true&w=majority&appName=200ok")

db = client.wine
