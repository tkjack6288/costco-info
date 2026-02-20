import re
from bs4 import BeautifulSoup

def test_price_parsing():
    raw_price = "$799$213.00 / 1包"
    print(f"Testing Price: {raw_price}")
    
    # Regex to find the first price: $ followed by digits (and commas)
    # The user wants "799" from "$799$213.00"
    match = re.search(r'\$\s*([\d,]+)', raw_price)
    if match:
        price = match.group(1).replace(',', '')
        print(f"Extracted: {price}")
    else:
        print("No match found")

def test_specs_parsing():
    html = """
    <div _ngcontent-storefront-c235="" class="product-classification-wrapper pdp-tab-content-body"><p _ngcontent-storefront-c235=""></p><sip-product-classification _ngcontent-storefront-c235="" _nghost-storefront-c234="" class="ng-star-inserted"><div _ngcontent-storefront-c234="" class="ng-star-inserted"><div _ngcontent-storefront-c234="" class="headline ng-star-inserted"></div><table _ngcontent-storefront-c234="" class="table ng-star-inserted"><tbody _ngcontent-storefront-c234=""><tr _ngcontent-storefront-c234="" class="ng-star-inserted"><td _ngcontent-storefront-c234="" class="attrib">品名</td><td _ngcontent-storefront-c234="" class="attrib-val">巧克力馬芬 6入</td></tr><!----><tr _ngcontent-storefront-c234="" class="ng-star-inserted"><td _ngcontent-storefront-c234="" class="attrib">內容量/入數</td><td _ngcontent-storefront-c234="" class="attrib-val">6入/ 盒</td></tr><!----><tr _ngcontent-storefront-c234="" class="ng-star-inserted"><td _ngcontent-storefront-c234="" class="attrib">商品重量</td><td _ngcontent-storefront-c234="" class="attrib-val">1084G</td></tr><!----></tbody></table></div></sip-product-classification></div>
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Try finding sip-product-classification table
    specs_data = {}
    table = soup.select_one('sip-product-classification table')
    if table:
        for tr in table.select('tr'):
            key_elem = tr.select_one('.attrib')
            val_elem = tr.select_one('.attrib-val')
            if key_elem and val_elem:
                key = key_elem.get_text(strip=True)
                val = val_elem.get_text(strip=True)
                specs_data[key] = val
    
    print("\nSpecs Parsed:")
    for k, v in specs_data.items():
        print(f"{k}: {v}")
    
    # Format as string
    specs_str = "\n".join([f"{k}: {v}" for k, v in specs_data.items()])
    print(f"\nSpecs String:\n{specs_str}")

if __name__ == '__main__':
    test_price_parsing()
    test_specs_parsing()
