import requests
from bs4 import BeautifulSoup
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.costco.com.tw/Health-Beauty/Supplements/Multi-Letter-Vitamins/Centrum-Advance-Women-200-Tablets/p/976579"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

print("--- Category ---")
breadcrumb = soup.select_one('ol.breadcrumb')
if breadcrumb:
    print("Found ol.breadcrumb:", [a.get_text(strip=True) for a in breadcrumb.select('a')])
else:
    print("Not found ol.breadcrumb")

print("--- Description ---")
desc = soup.select_one('.product-details-content-wrapper') or soup.select_one('#product_details')
if desc:
    print("Found description length:", len(desc.get_text(separator='\n', strip=True)))
else:
    print("Not found description")

print("--- Specs ---")
specs = soup.select_one('sip-product-classification table') or soup.select_one('#product_specs')
if specs:
    print("Found specs length:", len(specs.get_text(separator='\n', strip=True)))
else:
    print("Not found specs")

# Let's search for keywords to see if they are in JSON
print("--- Raw Search ---")
if "克補" in response.text:
    print("Found product name in raw HTML")
else:
    print("Product name NOT in raw HTML")

