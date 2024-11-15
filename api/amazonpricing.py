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
            print(f"Attempting to fetch data for ASIN: {asin} (Attempt {attempt + 1})")
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            print(f"Received data for ASIN: {asin}: {data}")
            
            if 'error' in data:
                print(f"API error for ASIN {asin}: {data['error']}")
                if 'rate limit' in data['error'].lower() or 'token' in data['error'].lower():
                    print("Rate limit or token exhaustion detected. Stopping further requests.")
                    return None, None
            
            price_str = data.get('price', '')
            name = data.get('title', '')
            print(f"Extracted price string: {price_str}, name: {name}")
            
            def extract_price(price_str):
                if not price_str:
                    print("Price string is empty or None")
                    return None
                price_str = price_str.replace(',', '').replace('$', '')
                if 'with' in price_str:
                    price_str = price_str.split('with')[0]
                price_match = re.search(r'\d+(\.\d+)?', price_str)
                if price_match:
                    print(f"Extracted price: {price_match.group()}")
                    return float(price_match.group())
                print("Failed to match price pattern")
                return None

            current_price = extract_price(price_str)
            
            if current_price is None:
                print(f"Failed to extract price for ASIN: {asin}")
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
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()
        print(f"Loaded CSV file: {file_path}")
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return
    
    for index, row in df.iterrows():
        asin = row['asin']
        current_price = row['current_price']
        name = row['name']
        print(f"Processing row {index}: ASIN={asin}, current_price={current_price}, name={name}")
        
        # check if the 2nd column is empty, if so fill in the data for that asin
        if pd.isna(current_price) or pd.isna(name):
            print(f"Checking ASIN: {asin}")
            
            current_price, name = check_price_and_name(asin, api_key) # get the current price and name of the product
            
            if current_price is not None and name is not None: # if the current price and name are not None, update the csv file
                df.at[index, 'current_price'] = current_price
                df.at[index, 'name'] = name
                try:
                    df.to_csv(file_path, index=False)
                    print(f"Updated {asin}: ${current_price}")
                except Exception as e:
                    print(f"Error saving CSV file: {e}")
            elif current_price is None and name is None:
                print("Stopping further updates due to API rate limit or token exhaustion.")
                break
        
        time.sleep(5)  # Rate limiting delay
    
    print(f"\n[{datetime.now()}] Price check completed!")

if __name__ == "__main__":
    api_key = "67356de984273be2da088d98"
    file_path = "/Users/torinwolff/Documents/GitHub/PCPB/volume/data.csv"
    update_prices(file_path, api_key)