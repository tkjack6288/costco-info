import requests
from bs4 import BeautifulSoup
import sys
sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.costco.com.tw/Health-Beauty/Supplements/Multi-Letter-Vitamins/Centrum-Advance-Women-200-Tablets/p/976579"
headers = {
    # Fake Googlebot User-Agent
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}

response = requests.get(url, headers=headers)
print("Response Status:", response.status_code)
print("Response Length:", len(response.text))

if len(response.text) < 5000:
    print("Likely blocked by Akamai or returned empty CSR! Here is the response:")
    print(response.text)
else:
    print("Received large HTML. Checking for elements...")
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
        print("Found description length:", len(desc.get_text(separator=' ', strip=True)))
    else:
        print("Not found description")
