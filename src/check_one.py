import logging
import sys
# Force UTF-8
sys.stdout.reconfigure(encoding='utf-8')

from src.crawler import CostcoCrawler
import json

logging.basicConfig(level=logging.INFO)

def main():
    crawler = CostcoCrawler()
    
    # Manually fetch one item
    # Since fetch_products returns a generator or list, we can just use internal methods for control
    
    # 1. Get List Page
    url = "https://www.costco.com.tw/c/hot-buys"
    import requests
    from bs4 import BeautifulSoup
    
    headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    print(f"Fetching {url}...")
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Find a product with a complex price if possible, or just the first one
    items = soup.select('.product-item') or soup.select('sip-product-list-item')
    
    if items:
        print(f"Found {len(items)} items. Scanning for a good candidate (e.g., Muffin)...")
        
        target_item = None
        for item in items:
            text = item.get_text()
            if "馬芬" in text or "Muffin" in text or "$" in text:
                target_item = item
                if "馬芬" in text: break # Prioritize Muffin as per user example
        
        if not target_item:
            print("No specific candidate found, using the second item if available...")
            target_item = items[1] if len(items) > 1 else items[0]

        # Parse Basic
        basic = crawler._parse_basic_info(target_item)
        if basic:
            print(f"Basic Info: {basic['name']}")
            print(f"Raw Price Parsed: {basic['price']}")
            
            # Parse Detail
            print("Fetching details...")
            product = crawler._fetch_product_details(basic)
            
            if product:
                print("\n=== Final Product Data ===")
                print(f"Name: {product.name}")
                print(f"Price: {product.price}")
                print(f"Specs: \n{product.specifications}")
                print(f"Images: {len(product.images)}")
                print("==========================")
            else:
                print("Failed to fetch details.")
        else:
            print("Failed to parse basic info.")
    else:
        print("No items found.")

if __name__ == '__main__':
    main()
