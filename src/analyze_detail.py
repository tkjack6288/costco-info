import logging
import sys
import requests
from bs4 import BeautifulSoup

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_detail():
    # 1. First, parse debug_hot_buys.html to get a valid product URL
    try:
        with open('debug_hot_buys.html', 'r', encoding='utf-8') as f:
            list_html = f.read()
    except:
        with open('debug_hot_buys.html', 'r', encoding='cp950', errors='ignore') as f:
            list_html = f.read()

    soup = BeautifulSoup(list_html, 'html.parser')
    item = soup.select_one('.product-item') or soup.select_one('sip-product-list-item')
    
    if not item:
        print("No item found in debug file.")
        return

    link_elem = item.select_one('a')
    raw_href = link_elem.get('href')
    print(f"Raw href in list: {raw_href}")
    
    # Check if absolute
    if raw_href.startswith('http'):
        product_url = raw_href
    else:
        product_url = "https://www.costco.com.tw" + raw_href
        
    print(f"Target Product URL: {product_url}")

    # 2. Fetch Detail Page
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(product_url + "?lang=zh_TW", headers=headers, timeout=30)
        # Add lang param just in case
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch detail page: {e}")
        return

    detail_soup = BeautifulSoup(response.text, 'html.parser')
    
    # Dump simple structure to debug
    print(f"Detail Page Title: {detail_soup.title.string if detail_soup.title else 'No Title'}")

    # 3. Analyze Detail Page Structure
    print("\n--- Detail Page Analysis ---")
    
    # Heuristic: Find div with most text
    max_len = 0
    best_elem = None
    
    # Scan all divs
    print("Scanning for large text blocks...")
    for elem in detail_soup.select('div'):
        # Skip common headers/footers based on class names if possible, but raw scan is safer
        text_len = len(elem.get_text(strip=True))
        if text_len > 100 and text_len < 5000: # Ignore huge wrapper divs
            # Check if it's a leaf or close to leaf
            if len(elem.find_all('div')) < 3: # It doesn't have many div children
                print(f"Candidate Div: Class={elem.get('class')}, ID={elem.get('id')}, TextLen={text_len}")
                print(f"Sample: {elem.get_text(strip=True)[:50]}...")
                
    # Check specific specs tab
    print("\nChecking tabs...")
    for tab in detail_soup.select('ul.nav-tabs li'):
        print(f"Tab: {tab.get_text(strip=True)}")

    # Check for 'panel'
    for panel in detail_soup.select('.tab-pane'):
        print(f"Tab Pane: ID={panel.get('id')} Class={panel.get('class')}")
        print(f"Content: {panel.get_text(strip=True)[:50]}...")

    # Images (Multiple)
    print("\n--- Image Analysis ---")
    all_imgs = detail_soup.select('img')
    print(f"Total img tags: {len(all_imgs)}")
    
    for img in all_imgs:
        src = img.get('src') or img.get('data-src') or ""
        if 'medias' in src or 'product' in src.lower():
            # Check parent to see if it's in a gallery
            parent = img.parent
            print(f"Image: {src[:50]}... | Parent: {parent.name} {parent.get('class')}")

if __name__ == '__main__':
    analyze_detail()
