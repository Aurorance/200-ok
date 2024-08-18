import pandas as pd
import os
import pymongo
from datetime import date
from dotenv import load_dotenv
from pandasai import SmartDataframe
from langchain_groq.chat_models import ChatGroq
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()
llm = ChatGroq(model_name = 'llama3-70b-8192',api_key = os.environ["GROQ_API_KEY"])
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
app = App(token=SLACK_BOT_TOKEN)

# some sample chat messages
# print(df.chat('Find price of wine name no'))
# print(df.chat('Find price of wine name why'))
# print(df.chat('Find price of wine name yes'))
# print(df.chat('Find all wine name with price 2'))
# print(df.chat('Find highest price'))
# print(df.chat('Find average price'))
# print(df.chat('What is the region of test1'))
# print(df.chat('What is the price of no'))

@app.event("app_mention")
def mention_handler(body, say):
    myclient = pymongo.MongoClient("mongodb+srv://edison:hackathon@200ok.oqe8x.mongodb.net/?retryWrites=true&w=majority&appName=200ok")
    wineDB = myclient["wine"]
    wineTable = wineDB["hist_wine"]
    spiritTable = wineDB["hist_spirits"]

    wineData = pd.DataFrame(wineTable.find({"Date":str(date.today())}))
    spiritData = pd.DataFrame(spiritTable.find({"Date":str(date.today())}))

    winedf = SmartDataframe(wineData,config = {'llm':llm})
    spiritdf = SmartDataframe(spiritData,config = {'llm':llm})

    try:
        # Receive input from chat
        input = body.get('event').get('text')
        # Extract the input by remove the @Wine Bot manually
        start_index = input.find(" ")
        input = input[start_index+1:]
        # Generate output and formatting
        if ("spirit" in input):
            output = spiritdf.chat(input)
        else:
            output = winedf.chat(input)
        if (type(output) is not str):
            output = str(output)
        if(output == "error" or output == "Unknown query" or output.endswith("png")):
            say("Error received when querying your request. Please try again in the following format: @Wine Bot [your query]")
            return
        # Send output to chat 
        say(output)
    except:
        say("Error received when querying your request. Please try again in the following format: @Wine Bot [your query]")

if (__name__ == "__main__"):
    # App init
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()