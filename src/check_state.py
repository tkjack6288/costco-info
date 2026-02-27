import requests
from bs4 import BeautifulSoup
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.costco.com.tw/Health-Beauty/Supplements/Multi-Letter-Vitamins/Centrum-Advance-Women-200-Tablets/p/976579"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

scripts = soup.find_all('script', type='application/json')
for s in scripts:
    state_id = s.get('id', '')
    print(f"Found JSON script: {state_id}")
    if state_id == 'spartacus-app-state' or 'state' in state_id.lower():
        try:
            data = json.loads(s.string)
            print("Successfully loaded state JSON. Keys:", list(data.keys()))
            with open('debug_state.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("Saved debug_state.json")
        except Exception as e:
            print("Error parsing JSON:", e)

# If not in script tags, it might be in an __INITIAL_STATE__ variable.
import re
match = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});', response.text)
if match:
    print("Found __INITIAL_STATE__")
    
