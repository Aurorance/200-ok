import pandas as pd
import os
import logging
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import good_to_buy

def notification():
    load_dotenv()
    SLACK_NOTE_BOT_TOKEN = os.environ["SLACK_NOTE_BOT_TOKEN"]
    client = WebClient(token=SLACK_NOTE_BOT_TOKEN)
    logger = logging.getLogger(__name__)

    text = ""
    # Check for each type of beverage and output a random of any good-time-to-buy beverage
    recommendation = good_to_buy.random_good_wine("white-wine")
    if recommendation is not None:
        text += "White wine: " + recommendation["name"] +  " with price of " + str(recommendation["price"]) + " with only " + str(recommendation["stock"]) + " left\n"

    recommendation = good_to_buy.random_good_wine("red-wines")
    if recommendation is not None:
        text += "Red wine: " + recommendation["name"] +  " with price of " + str(recommendation["price"]) + " with only " + str(recommendation["stock"]) + " left\n"

    recommendation = good_to_buy.random_good_wine("rose-wine")
    if recommendation is not None:
        text += "Rose wine: " + recommendation["name"] +  " with price of " + str(recommendation["price"]) + " with only " + str(recommendation["stock"]) + " left\n"

    recommendation = good_to_buy.random_good_spirit("bourbon")
    if recommendation is not None:
        text += "Bourbon: " + recommendation["name"] +  " with price of " + str(recommendation["price"]) + " with only " + str(recommendation["stock"]) + " left\n"
    
    recommendation = good_to_buy.random_good_spirit("gin")
    if recommendation is not None:
        text += "Gin: " + recommendation["name"] +  " with price of " + str(recommendation["price"]) + " with only " + str(recommendation["stock"]) + " left\n"
    
    recommendation = good_to_buy.random_good_spirit("liqueurs")
    if recommendation is not None:
        text += "Liqueurs: " + recommendation["name"] +  " with price of " + str(recommendation["price"]) + " with only " + str(recommendation["stock"]) + " left\n"

    recommendation = good_to_buy.random_good_spirit("rum")
    if recommendation is not None:
        text += "Rum: " + recommendation["name"] +  " with price of " + str(recommendation["price"]) + " with only " + str(recommendation["stock"]) + " left\n"
    
    recommendation = good_to_buy.random_good_spirit("tequila")
    if recommendation is not None:
        text += "Tequila: " + recommendation["name"] +  " with price of " + str(recommendation["price"]) + " with only " + str(recommendation["stock"]) + " left\n"

    recommendation = good_to_buy.random_good_spirit("sake")
    if recommendation is not None:
        text += "Sake: " + recommendation["name"] +  " with price of " + str(recommendation["price"]) + " with only " + str(recommendation["stock"]) + " left\n"

    recommendation = good_to_buy.random_good_spirit("whisky")
    if recommendation is not None:
        text += "Whisky: " + recommendation["name"] +  " with price of " + str(recommendation["price"]) + " with only " + str(recommendation["stock"]) + " left\n"

    recommendation = good_to_buy.random_good_spirit("vodka")
    if recommendation is not None:
        text += "Vodka: " + recommendation["name"] +  " with price of " + str(recommendation["price"]) + " with only " + str(recommendation["stock"]) + " left\n"

    # Final checking to ensure if none of the beverages is good, just output a message
    if (text != ""):
        text = "Here are some recommendations to look for:\n" + text
    else:
        text = "Unfortunately none of the beverages have a good price or demend right now"

    # Get channel info to post on
    channel_name = "notificationbot"
    conversation_id = None

    try:
        # Find the channel id by searching through the channel list
        for result in client.conversations_list():
            if conversation_id is not None:
                break
            for channel in result["channels"]:
                if channel["name"] == channel_name:
                    conversation_id = channel["id"]
                    print("conversation_id = ", conversation_id)
                    break
        # Post the message
        result = client.chat_postMessage(
            channel=conversation_id,
            text=text
        )
    except SlackApiError as e:
        print(f"API error found", e)

notification()