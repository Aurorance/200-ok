import pandas as pd
import os
import pymongo
from dotenv import load_dotenv

# used for embedding
import json
from llama_index.core import Document
from llama_index.core.schema import MetadataMode
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch

# used for slack
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Config
load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
app = App(token=SLACK_BOT_TOKEN)

# Access data in mongoDB
myclient = pymongo.MongoClient("mongodb+srv://edison:edison8172@cluster0.kvogm.mongodb.net/")
wineDB = myclient["testchatbot"]
wineTable = wineDB["wines"]
data = pd.DataFrame(wineTable.find())

# Init embed model
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Prep the data for embedding
documents = data.to_json(default_handler=str, orient="records")
documents_list = json.loads(documents)
llama_documents = []
# Metadata to be embedded
for document in documents_list:
    print(document)
    document["wine_name"] = json.dumps(document["wine_name"])
    document["wine_price"] = json.dumps(document["wine_price"])
    document["wine_score"] = json.dumps(document["wine_score"])
    document["wine_category"] = json.dumps(document["wine_category"])
    # Create the documents to be embedded
    llama_document = Document(
    text=document["wine_name"],
    metadata=document,
    excluded_llm_metadata_keys=[],
    excluded_embed_metadata_keys=[],
    metadata_template="{key}=>{value}",
    text_template="Metadata: {metadata_str}\n-----\nContent: {content}",
    )
    # Add each to the list
    llama_documents.append(llama_document)

# test
print(
"\nThe LLM sees this: \n",
llama_documents[0].get_content(metadata_mode=MetadataMode.LLM),
)

print(
"\nThe Embedding model sees this: \n",
llama_documents[0].get_content(metadata_mode=MetadataMode.EMBED),
)
#test

#Embed the data
parser = SentenceSplitter()
nodes = parser.get_nodes_from_documents(llama_documents)
for node in nodes:
    node_embedding = embed_model.get_text_embedding(
        node.get_content(metadata_mode="all")
    )
    node.embedding = node_embedding

# Renew the database with embedded data
# wineTable.delete_many({})
vector_store = MongoDBAtlasVectorSearch(myclient, db_name="testchatbot", collection_name="wines", index_name="vector_index")
# vector_store.add(nodes)

# user_query = "Find highest price of white wine"
# query_embeddings = embedding_model.encode(user_query).tolist()
from llama_index.core import VectorStoreIndex, StorageContext

index = VectorStoreIndex.from_vector_store(vector_store)
from llama_index.core.response.notebook_utils import display_response

query_engine = index.as_query_engine(similarity_top_k=3)

query = "Find highest price of white wine"

response = query_engine.query(query)

print(response)

# some sample chat messages
# print(df.chat('Find price of wine name no'))
# print(df.chat('Find price of wine name why'))
# print(df.chat('Find price of wine name yes'))
# print(df.chat('Find all wine name with price 2'))
# print(df.chat('Find highest price'))
# print(df.chat('Find average price'))
# print(df.chat('What is the region of test1'))
# print(df.chat('What is the price of no'))

# @app.event("app_mention")
# def mention_handler(body, say):
#     try:
#         input = body.get('event').get('text')
#         start_index = input.find(" ")
#         input = input[start_index+1:]
#         output = df.chat(input)
#         print(output)
#         if (type(output) is not str):
#             output = str(output)
#         if(output == "error" or output == "Unknown query" or output.endswith("png")):
#             say("Error received when querying your request. Please try again in the following format: @Wine Bot [your query]")
#             return
#         say(output)
#     except:
#         say("Error received when querying your request. Please try again in the following format: @Wine Bot [your query]")

# if (__name__ == "__main__"):
#     handler = SocketModeHandler(app, SLACK_APP_TOKEN)
#     handler.start()