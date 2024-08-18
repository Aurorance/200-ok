import pandas as pd
import pymongo
import random
import sys

def random_good_wine(wine_type):
    try:
        client = pymongo.MongoClient("mongodb+srv://issacchl2002:hackathon@200ok.oqe8x.mongodb.net/?retryWrites=true&w=majority&appName=200ok")
    except pymongo.errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
        sys.exit(1)

    db = client['wine']  
    collection = db['hist_wine']  
    
    cursor = collection.find()
    df_wine_data = pd.DataFrame(list(cursor))
    
    # Ensure 'Date' field is in the correct datetime format
    df_wine_data['Date'] = pd.to_datetime(df_wine_data['Date'])
    
    # Filter the DataFrame based on the given wine type
    df_wine_type = df_wine_data[df_wine_data['wine_category'] == wine_type]
    
    # Group by wine_name to analyze each wine individually
    grouped = df_wine_type.groupby('wine_name')
    
    # List to store wines that meet the criteria
    candidate_wines = []
    
    # Iterate over each group (each unique wine)
    for wine_name, group in grouped:
        # sort by date
        group = group.sort_values(by='Date')
        
        # recent - oldest
        price_trend = (group['wine_price'].iloc[-1] - group['wine_price'].iloc[0] < 0) and (group['wine_price'].iloc[-1] - group['wine_price'].iloc[-2] < 0)
        
        avg_price_last_year = group['wine_price'].mean()
        
        current_price = group['wine_price'].iloc[-1]
        
        # criteria 1 : price decrease & below mean
        price_criteria = price_trend or (current_price < 0.9 * avg_price_last_year)
        
        # recent - oldest
        stock_trend = group['wine_stock'].iloc[-1] - group['wine_stock'].iloc[-2]
        
        # criteria 2 : increasing demand
        demand_criteria = (stock_trend < 0)
        
        # candidate list if both criteria fits
        if price_criteria and demand_criteria:
            candidate_wines.append({"name": wine_name, "price":current_price, "stock":group['wine_stock'].iloc[-1]})
    
    # random one
    if candidate_wines:
        #print(len(candidate_wines))
        return random.choice(candidate_wines)
    else:
        return None
    
#%%
def random_good_spirit(spirit_type):
    try:
        client = pymongo.MongoClient("mongodb+srv://issacchl2002:hackathon@200ok.oqe8x.mongodb.net/?retryWrites=true&w=majority&appName=200ok")
    except pymongo.errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
        sys.exit(1)

    db = client['wine']  
    collection = db['hist_spirits']  
    
    cursor = collection.find()
    df_spirit_data = pd.DataFrame(list(cursor))
    
    df_spirit_data['Date'] = pd.to_datetime(df_spirit_data['Date'])
    
    df_spirit_type = df_spirit_data[df_spirit_data['spirit_category'] == spirit_type]
    
    grouped = df_spirit_type.groupby('spirit_name')
    
    candidate_spirits = []
    
    for spirit_name, group in grouped:
        group = group.sort_values(by='Date')
        
        price_trend = group['spirit_price'].iloc[-1] - group['spirit_price'].iloc[0]
        
        avg_price_last_year = group['spirit_price'].mean()
        
        current_price = group['spirit_price'].iloc[-1]
        
        price_trend = (group['spirit_price'].iloc[-1] - group['spirit_price'].iloc[0] < 0) and (group['spirit_price'].iloc[-1] - group['spirit_price'].iloc[-2] < 0)
        
        price_criteria = price_trend or (current_price < 0.9 * avg_price_last_year)
        stock_trend = group['spirit_stock'].iloc[-1] - group['spirit_stock'].iloc[-2]
        demand_criteria = (stock_trend < 0)
        
        if price_criteria and demand_criteria:
            candidate_spirits.append(candidate_spirits.append({"name": spirit_name, "price":current_price, "stock":group['spirit_stock'].iloc[-1]}))
    
    # random candidate
    if candidate_spirits:
        # print(len(candidate_spirits))
        return random.choice(candidate_spirits)
    else:
        return None

# #%%
# random_wine = random_good_wine('white-wine')
# if random_wine:
#     print(f"A good wine to buy is: {random_wine}")
# else:
#     print("No wine currently meet the criteria.")
# # %%
# random_spirit = random_good_spirit('whisky')
# if random_spirit:
#     print(f"A good spirit to buy is: {random_spirit}")
# else:
#     print("No spirits currently meet the criteria.")
