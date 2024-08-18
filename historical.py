import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random


# Read spirits data
df_all_spirit = pd.read_csv('all_spirit_data.csv')

current_date = datetime.now().date()
df_all_spirit['Date'] = current_date

# Dynamically create the website URL based on the spirit category


spirit_name = df_all_spirit['spirit_name'].tolist()
spirit_stock = df_all_spirit['spirit_stock'].tolist()
spirit_category = df_all_spirit['spirit_category'].tolist()
spirit_link = df_all_spirit['Img'].tolist()

hist_df_list = [df_all_spirit]

for i in range(1, 13):
    spirit_price = [round(price * (1 + random.uniform(-0.20, 0.20)), 2) for price in df_all_spirit['spirit_price']]
    
    spirit_stock = [
        max(stock + random.randint(-5, 5), 0) if stock != 999 else random.choice([random.randint(95, 105), 999])
        for stock in df_all_spirit['spirit_stock']
    ]
    
    hist = {
        'spirit_name': spirit_name,
        'spirit_price': spirit_price,
        'spirit_stock': spirit_stock,
        'spirit_category': spirit_category,
        'Img': spirit_link
    }
    
    df_hist = pd.DataFrame(hist)
    df_hist['Date'] = (current_date - relativedelta(months=i))
    hist_df_list.append(df_hist)

hist_df = pd.concat(hist_df_list, ignore_index=True)
hist_df.to_csv('hist_spirit_data.csv', index=False)

# Read wine data
df_all_wine = pd.read_csv('all_wine_data.csv')

df_all_wine['Date'] = current_date
# Add website column with f-string

wine_name = df_all_wine['wine_name'].tolist()
wine_stock = df_all_wine['wine_stock'].tolist()
wine_score = df_all_wine['wine_score'].tolist()
wine_category = df_all_wine['wine_category'].tolist()
wine_link = df_all_wine['Img'].tolist()

hist_df_list = [df_all_wine]

for i in range(1, 13):
    wine_price = [round(price * (1 + random.uniform(-0.20, 0.20)), 2) for price in df_all_wine['wine_price']]

    wine_stock = [
        max(stock + random.randint(-5, 5), 0) if stock != 999 else random.choice([random.randint(95, 105), 999])
        for stock in df_all_wine['wine_stock']
    ]

    hist = {
        'wine_name': wine_name,
        'wine_price': wine_price,
        'wine_stock': wine_stock,
        'wine_score': wine_score,
        'wine_category': wine_category,
        'Img': wine_link
    }

    df_hist = pd.DataFrame(hist)
    df_hist['Date'] = (current_date - relativedelta(months=i))
    hist_df_list.append(df_hist)

hist_df = pd.concat(hist_df_list, ignore_index=True)
hist_df.to_csv('hist_wine_data.csv', index=False)