import requests
from bs4 import BeautifulSoup

def debug_homepage():
    url = "https://www.costco.com.tw/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for category links
        # Common patterns: navigation menus
        nav_links = soup.select('nav a')
        print(f"Found {len(nav_links)} links in nav")
        
        # specific known classes for menus in hybris/spartacus (common in Costco)
        # .navigation-node, .category-node
        messages = []
        messages.append(f"Found {len(nav_links)} links in nav")
        
        for a in nav_links:
            # Filter somewhat
            href = a.get('href', '')
            if href and ('/c/' in href or '/Category/' in href):
                messages.append(f"Nav Link: {a.get_text(strip=True)} -> {href}")

        # Look for "Shop All" or similar
        messages.append("\n--- Searching for 'Category' or 'Department' ---")
        for a in soup.select('a'):
            text = a.get_text(strip=True)
            if "所有商品" in text or "Category" in text or "Department" in text:
                 messages.append(f"Potential Category Link: {text} -> {a.get('href')}")

        with open('debug_output.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(messages))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_homepage()
