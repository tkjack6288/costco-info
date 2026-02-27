from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_fetch_detail():
    url = "https://www.costco.com.tw/p/111844"
    
    with sync_playwright() as p:
        # 啟動 Chromium
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("正在載入網頁與等待商品詳細內容出現...")
        # 取消 networkidle，改為明確等待主要商品資料區塊載入
        page.goto(url, wait_until="domcontentloaded")
        try:
            page.wait_for_selector('.product-details-content-wrapper, #product_details', timeout=15000)
        except Exception as e:
            print(f"等待商品內容區塊超時！錯誤: {e}")
        
        # 取得渲染完成的 HTML
        html_content = page.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        print("\n--- 擷取結果 ---")
        
        # 抓取分類
        breadcrumb = soup.select_one('ol.breadcrumb')
        if breadcrumb:
            cats = [a.get_text(strip=True) for a in breadcrumb.select('a') if a.get_text(strip=True)]
            print("【分類】:", " > ".join(cats))
        else:
            print("【分類】: 仍未找到")

        # 抓取說明
        desc = soup.select_one('.product-details-content-wrapper') or soup.select_one('#product_details')
        if desc:
            print(f"【說明】: 成功抓取！(長度 {len(desc.get_text(strip=True))} 字)")
        else:
            print("【說明】: 仍未找到")
            
        browser.close()

if __name__ == "__main__":
    test_fetch_detail()
