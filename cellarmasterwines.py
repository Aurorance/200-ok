from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime

# Function to convert stock strings to integer values
def convert_stock_to_int(stock_str):
    if stock_str == '' or 'Delivery' in stock_str:
        return 999
    elif 'in stock' in stock_str:
        return int(stock_str.split()[0])
    elif 'available' in stock_str:
        return int(stock_str.split()[0])
    elif 'Last stocks' in stock_str:
        return int(stock_str.split()[-4])
    elif 'Out of stock' in stock_str:
        return 0
    else:
        return 999  # Default to 999 if format doesn't match

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    wine_list = ['white-wine', 'red-wines', 'rose-wine']
    spirit_list = ['bourbon', 'cognac', 'gin', 'liqueurs', 'rum', 'sake', 'tequila', 'whisky', 'vodka']
    
    all_wine_data = []
    all_spirit_data = []
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Scraping Wine Data
    for wine in wine_list:
        driver.get(f'https://cellarmasterwines.com/collections/{wine}')
        try:
            driver.find_element(By.XPATH,'//section[1]/div[1]/div[3]/a[1]').click()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[4]/div[1]/button[1]"))).click()
        except:
            pass
        
        while True:
            for i in range(1, 25):
                try:
                    name = driver.find_element(By.XPATH, f"//li[{i}]/div[1]/div[1]/div[2]/div[1]/div[1]/a[1]/h3[1]").text
                    price = driver.find_element(By.XPATH, f"//li[{i}]/div[1]/div[1]/div[2]/div[1]/div[3]/dl[1]/div[2]/div[1]/dd[1]/span[1]").text
                    stock = driver.find_element(By.XPATH, f"//li[{i}]/div[1]/div[1]/div[2]/div[1]/div[2]").text
                    score = driver.find_element(By.XPATH, f"//li[{i}]/div[1]/div[1]/div[1]/a[1]/div[2]/div[1]/span[2]").text
                    link = driver.find_element(By.XPATH, f"//li[{i}]/div[1]/div[1]/div[1]/a[1]/div[1]/div[1]/img[1]").get_attribute('src')

                    
                    wine_data = {
                        'wine_name': name,
                        'wine_price': int(price[3:].replace(',', '')),
                        'wine_stock': convert_stock_to_int(stock),
                        'wine_score': int(score),
                        'wine_category': wine,
                        'Img': link,
                        'Date': current_date 
                    }
                    all_wine_data.append(wine_data)
                except:
                    pass
            
            try:
                next_button = driver.find_element(By.XPATH, '//a[@aria-label="Next page"]')
                next_button.click()
            except:
                break
    
    # Convert wine data to DataFrame and save to CSV
    df_all_wine = pd.DataFrame(all_wine_data)
    df_all_wine.to_csv('all_wine_data.csv', index=False, encoding='utf-8')
    
    # Scraping Spirit Data
    for spirit in spirit_list:
        driver.get(f'https://cellarmasterwines.com/collections/{spirit}')
        
        while True:
            for i in range(1, 25):
                try:
                    name = driver.find_element(By.XPATH, f"//li[{i}]/div[1]/div[1]/div[2]/div[1]/div[1]/a[1]/h3[1]").text
                    price = driver.find_element(By.XPATH, f"//li[{i}]/div[1]/div[1]/div[2]/div[1]/div[3]/dl[1]/div[2]/div[1]/dd[1]/span[1]").text
                    stock = driver.find_element(By.XPATH, f"//li[{i}]/div[1]/div[1]/div[2]/div[1]/div[2]").text
                    link = driver.find_element(By.XPATH, f"//li[{i}]/div[1]/div[1]/div[1]/a[1]/div[1]/div[1]/img[1]").get_attribute('src')
                    spirit_data = {
                        'spirit_name': name,
                        'spirit_price': int(price[3:].replace(',', '')),
                        'spirit_stock': convert_stock_to_int(stock),
                        'spirit_category': spirit,
                        'Img': link,
                        'Date': current_date
                    }
                    all_spirit_data.append(spirit_data)
                except:
                    pass
            
            try:
                next_button = driver.find_element(By.XPATH, '//a[@aria-label="Next page"]')
                next_button.click()
            except:
                break
    
    # Convert spirit data to DataFrame and save to CSV
    df_all_spirit = pd.DataFrame(all_spirit_data)
    df_all_spirit.to_csv('all_spirit_data.csv', index=False, encoding='utf-8')

    # Convert DataFrames to dictionaries for MongoDB insertion
    dict_all_wine = df_all_wine.to_dict(orient='records')
    dict_all_spirit = df_all_spirit.to_dict(orient='records')

    print(len(dict_all_wine))
    print(len(dict_all_spirit))

finally:
    # Close the WebDriver
    driver.quit()