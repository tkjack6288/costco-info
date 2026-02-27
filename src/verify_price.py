import re
from bs4 import BeautifulSoup

def test_new_price_logic():
    html_content = """
    <div class="product-item">
        <span class="product-price"></span>
        <span class="notranslate ng-star-inserted">$509</span>
    </div>
    """
    
    soup = BeautifulSoup(html_content, 'html.parser')
    item = soup.select_one('.product-item')
    
    price_elem = item.select_one('.product-price') or item.select_one('.price-panel')
    
    # Simulate empty price if the element exists but text is empty
    if price_elem and not price_elem.get_text(strip=True):
         price_elem = None
         
    if not price_elem:
        for span in item.select('span.notranslate.ng-star-inserted'):
            if '$' in span.get_text():
                price_elem = span
                break

    price_text = price_elem.get_text(strip=True) if price_elem else None
    price = None
    if price_text:
        match = re.search(r'\$\s*([\d,]+)', price_text)
        if match:
            price = match.group(1).replace(',', '')
        else:
            price = price_text # Fallback

    print(f"Extracted Price: {price}")
    assert price == "509", "Price extraction failed"

if __name__ == "__main__":
    test_new_price_logic()
    print("Success")
