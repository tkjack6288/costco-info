import requests
from bs4 import BeautifulSoup

def debug_pagination():
    # A category that likely has multiple pages
    url = "https://www.costco.com.tw/c/1" # 3C 科技 usually has many items
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print(f"Title: {soup.title.string.strip() if soup.title else 'No Title'}")
        
        # Look for pagination - generic keyword search
        print(f"HTML len: {len(response.text)}")
        
        soup_text = response.text.lower()
        if 'pagination' in soup_text:
            print("Found 'pagination' string in HTML")
            
        if 'next' in soup_text:
            print("Found 'next' string in HTML")
            
        # Try to find elements with class containing 'page'
        for tag in soup.find_all(class_=lambda x: x and ('page' in x or 'pagination' in x)):
             print(f"Potential Pagination Tag: {tag.name} class={tag.get('class')}")
             # Print children text if short
             if len(tag.get_text()) < 100:
                  print(f"  Text: {tag.get_text(strip=True)}")

        # Check for query params in links
        cm = 0
        for a in soup.find_all('a', href=True):
             if '?page=' in a['href'] or '&page=' in a['href']:
                  print(f"Found link with page param: {a['href']}")
                  cm += 1
                  if cm > 5: break
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_pagination()
