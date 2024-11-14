import requests
import pandas as pd
import os
import time
from datetime import datetime
from pathlib import Path

def download_product_image(asin, api_key, image_dir):
    api_url = f'https://api.scrapingdog.com/amazon/product?api_key={api_key}&domain=com&asin={asin}'
    retries = 3
    
    for attempt in range(retries):
        try:
            print(f"\n[{datetime.now()}] Getting image for ASIN: {asin} (Attempt {attempt + 1}/{retries})")
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            
            # Get first image URL
            images = data.get('images', [])
            if not images:
                print(f"No images found for ASIN {asin}")
                return False
                
            image_url = images[0]
            
            # Download image
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            # Save image
            image_path = os.path.join(image_dir, f"{asin}.jpg")
            with open(image_path, 'wb') as f:
                f.write(image_response.content)
                
            print(f"Downloaded image for {asin}")
            return True
            
        except requests.RequestException as e:
            print(f"Request error for {asin} (Attempt {attempt + 1}): {e}")
            if attempt == retries - 1:
                return False
            wait_time = (2 ** attempt) * 2
            print(f"Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)
            
        except Exception as e:
            print(f"Error processing {asin}: {e}")
            return False

def download_all_images(file_path, api_key, image_dir):
    # Create images directory if it doesn't exist
    Path(image_dir).mkdir(parents=True, exist_ok=True)
    
    print(f"\n[{datetime.now()}] Starting image downloads")
    
    # Read ASINs from CSV
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    
    total = len(df)
    success = 0
    
    for index, row in df.iterrows():
        asin = row['asin']
        if download_product_image(asin, api_key, image_dir):
            success += 1
        time.sleep(2)  # Rate limiting
        
    print(f"\n[{datetime.now()}] Download complete!")
    print(f"Successfully downloaded {success}/{total} images")

if __name__ == "__main__":
    api_key = "673147a734a4318291dc90e1"
    file_path = "/Users/torinwolff/Documents/GitHub/PCPB/volume/data.csv"
    image_dir = "/Users/torinwolff/Documents/GitHub/PCPB/volume/images"
    download_all_images(file_path, api_key, image_dir)