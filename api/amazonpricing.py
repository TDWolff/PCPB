import requests
import pandas as pd
import time
import re
from datetime import datetime

def check_price_and_name(asin, api_key):
    api_url = f'https://api.scrapingdog.com/amazon/product?api_key={api_key}&domain=com&asin={asin}'
    retries = 3
    
    for attempt in range(retries):
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            
            price_str = data['price']
            name = data['title']
            
            def extract_price(price_str):
                if not price_str:
                    return None
                price_str = price_str.replace(',', '').replace('$', '')
                if 'with' in price_str:
                    price_str = price_str.split('with')[0]
                price_match = re.search(r'\d+(\.\d+)?', price_str)
                if price_match:
                    return float(price_match.group())
                return None

            current_price = extract_price(price_str)
            
            if current_price is None:
                continue
                
            return current_price, name
            
        except requests.RequestException as e:
            print(f"Request error for {asin} (Attempt {attempt + 1}): {e}")
            if attempt == retries - 1:
                return None, None
            wait_time = (2 ** attempt) * 2
            print(f"Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)
            
        except Exception as e:
            print(f"Error processing {asin}: {e}")
            return None, None

def update_prices(file_path, api_key):
    print(f"\n[{datetime.now()}] Starting price update")
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    
    for index, row in df.iterrows():
        asin = row['asin']
        print(f"Checking ASIN: {asin}")
        
        current_price, name = check_price_and_name(asin, api_key)
        
        if current_price is not None and name is not None:
            if (df.at[index, 'current_price'] != current_price or 
                df.at[index, 'name'] != name):
                
                old_price = df.at[index, 'current_price']
                df.at[index, 'current_price'] = current_price
                df.at[index, 'name'] = name
                df.to_csv(file_path, index=False)
                print(f"Updated {asin}: ${current_price} (was ${old_price})")
        
        time.sleep(5)  # Rate limiting delay
    
    print(f"\n[{datetime.now()}] Price check completed!")

if __name__ == "__main__":
    api_key = "673147a734a4318291dc90e1"
    file_path = "/Users/torinwolff/Documents/GitHub/PCPB/volume/data.csv"
    update_prices(file_path, api_key)