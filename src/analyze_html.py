from bs4 import BeautifulSoup

def analyze():
    # Use utf-8 by default, fallback to cp950 (Big5)
    try:
        with open('debug_hot_buys.html', 'r', encoding='utf-8') as f:
            html = f.read()
    except UnicodeDecodeError:
        with open('debug_hot_buys.html', 'r', encoding='cp950', errors='ignore') as f:
            html = f.read()

    print(f"HTML length: {len(html)}")
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Try different selectors
    items = soup.select('.product-item')
    print(f"Found {len(items)} items with .product-item")
    
    if items:
        item = items[0]
        print("--- Text Content ---")
        print(item.get_text(separator='\n', strip=True))
        
        print("\n--- Links ---")
        for a in item.select('a'):
            print(a.get('href'))
            
        print("\n--- Images ---")
        for img in item.select('img'):
            print(img.get('src'))
    else:
        print("No items found.")

if __name__ == '__main__':
    analyze()
