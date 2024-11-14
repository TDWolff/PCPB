import csv

def extract_asin(url):
    try:
        # Find the position of /dp/ and the following ? or end of string
        dp_index = url.find('/dp/')
        if dp_index == -1:
            return None
        
        # Start after /dp/
        start = dp_index + 4
        
        # Find end position (either ? or end of string)
        end = url.find('?', start)
        if end == -1:
            end = len(url)
            
        # Extract ASIN
        asin = url[start:end]
        
        # Validate ASIN format (typically 10 characters)
        if len(asin) == 10:
            return asin
        return None
    
    except Exception:
        return None

def get_asins_from_string(urls_string):
    urls = urls_string.split()  # Split the string by spaces or newlines
    asins = []
    for url in urls:
        asin = extract_asin(url)
        if asin:
            asins.append(asin)
    return asins

def save_asins_to_csv(asins, filename='amazon_asins.csv'):
    # Write ASINs to CSV with header
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ASIN'])  # Header
        for asin in asins:
            writer.writerow([asin])


# Example usage
if __name__ == "__main__":
    urls_string = ""
    # run defs
    asins = get_asins_from_string(urls_string)
    save_asins_to_csv(asins)
    print(asins)
    