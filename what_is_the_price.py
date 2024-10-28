import argparse
import requests

# Config property location and property type
LOCATION_MACGREGOR = "macgregor-qld-4109"
LOCATION_MANSFIELD = "mansfield-qld-4122"
PROPERTY_TYPE = "free-standing"

parser = argparse.ArgumentParser(description="A tool to find upper marketing range of a property in domain.co.au")
parser.add_argument("-t", "--text", 
                    help="Any keyword you wan to search for on the page, eg property address", 
                    required=True, type=str)

args = vars(parser.parse_args())
target_text = args['text']

# Generate a price list, 700K to 10M
BASE_PRICE_100K = 100000
price_list = [x * BASE_PRICE_100K  for x in range(9, 100)] 

def parse_text_from(url: str, text: str) -> bool:
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    # print("Downloading webpage...")
    respond = requests.get(url=url, headers=headers, timeout=10)
    if respond.status_code == 200:
        # print("Downloading successed")
        if text.strip().lower() in respond.text.lower():
            return True
    else:
        # print("Download failed")
        pass

    return False

upper_limit = 0
for price in price_list:
    # We are only looking at the first two pages
    url1 = f"https://www.domain.com.au/sale/{LOCATION_MACGREGOR}/{PROPERTY_TYPE}/?price={price}-any&page=1"
    url2 = f"https://www.domain.com.au/sale/{LOCATION_MACGREGOR}/{PROPERTY_TYPE}/?price={price}-any&page=2"
    url3 = f"https://www.domain.com.au/sale/{LOCATION_MANSFIELD}/{PROPERTY_TYPE}/?price={price}-any&page=1"
    url4 = f"https://www.domain.com.au/sale/{LOCATION_MANSFIELD}/{PROPERTY_TYPE}/?price={price}-any&page=2"

    price_in_millions = price /  1000000
    
    if parse_text_from(url1, target_text) or parse_text_from(url2, target_text) or parse_text_from(url3, target_text) or parse_text_from(url4, target_text):
        print(f"Found at price point: {price_in_millions}m")
        upper_limit = price_in_millions
    else:
        # We can't find it at this price point. Now we know our upper limit is the previous price
        print(f"Marketing price is up to: {upper_limit}m for {target_text}")
        break
