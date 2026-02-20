import logging
from src.crawler import CostcoCrawler
import json

logging.basicConfig(level=logging.INFO)

def main():
    crawler = CostcoCrawler()
    # Fetch list
    print("Fetching list...")
    # Just fetch the first item to verify details
    # We can reuse fetch_products but break early or mock
    # Let's manually call the internal methods to test one item
    
    # 1. Get List Page
    url = "https://www.costco.com.tw/c/hot-buys"
    import requests
    from bs4 import BeautifulSoup
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    item = soup.select_one('.product-item') or soup.select_one('sip-product-list-item')
    
    if item:
        print("Found item. Parsing basic info...")
        basic = crawler._parse_basic_info(item)
        print(f"Basic URL: {basic['url']}") # Verify URL fix
        
        print("Fetching details...")
        product = crawler._fetch_product_details(basic)
        
        if product:
            print("\n--- Verified Product Data ---")
            data = product.to_dict()
            # Truncate long text for display
            if data['description']: data['description'] = data['description'][:100] + "..."
            if data['specifications']: data['specifications'] = data['specifications'][:100] + "..."
            
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            print(f"\nImages Found: {len(product.images)}")
            for img in product.images:
                print(f"- {img}")
        else:
            print("Failed to fetch details.")
    else:
        print("No items found.")

if __name__ == '__main__':
    main()
