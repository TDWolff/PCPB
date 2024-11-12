import requests

def check_price(asin):
    api_key = "673147a734a4318291dc90e1"
    api_url = f'https://api.scrapingdog.com/amazon/product?api_key={api_key}&domain=com&asin={asin}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        price = int(float(response.json()['price'].replace("$", "").replace(',', '')))

        print(f"Current price: {price}")

        if price < 2147:
            print(price)
    except requests.RequestException as e:
        print(f"Error fetching price: {e}")
        print(f"Response content: {response.content}")

if __name__ == "__main__":
    asin = input("Enter the ASIN of the item: ")
    check_price(asin)