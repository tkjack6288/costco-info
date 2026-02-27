import requests
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

product_id = "976579"
api_url = f"https://www.costco.com.tw/rest/v2/taiwan/products/{product_id}?fields=FULL&lang=zh_TW"
# Try another common Spartacus pattern
api_url2 = f"https://www.costco.com.tw/occ/v2/costcotaiwan/products/{product_id}?fields=FULL&lang=zh_TW"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
}

print("Trying API 1:", api_url)
try:
    r1 = requests.get(api_url, headers=headers)
    print("Status 1:", r1.status_code)
    if r1.status_code == 200:
        data = r1.json()
        print("Success! Keys:", data.keys())
        print("Name:", data.get('name'))
        categories = data.get('categories', [])
        print("Categories:", [c.get('name') for c in categories])
except Exception as e:
    print("Error 1:", e)

print("\nTrying API 2:", api_url2)
try:
    r2 = requests.get(api_url2, headers=headers)
    print("Status 2:", r2.status_code)
    if r2.status_code == 200:
        data = r2.json()
        print("Success! Keys:", data.keys())
        print("Name:", data.get('name'))
        categories = data.get('categories', [])
        print("Categories:", [c.get('name') for c in categories])
except Exception as e:
    print("Error 2:", e)
    
