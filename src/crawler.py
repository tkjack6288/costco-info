import logging
import time
from typing import List, Optional, Dict, Iterable
from src.models import Product
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)

class CostcoCrawler:
    BASE_URL = "https://www.costco.com.tw"
    
    def __init__(self, user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"):
        self.user_agent = user_agent
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    def _start_browser(self):
        """啟動 Playwright 瀏覽器並建立全域分頁"""
        if not self.playwright:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=True)
            self.context = self.browser.new_context(
                user_agent=self.user_agent,
                viewport={"width": 1280, "height": 800}
            )
            # 將分頁建立在此 Context 內，以共用 Cookie
            self.page = self.context.new_page()

    def _close_browser(self):
        """關閉瀏覽器與 Playwright"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
            self.playwright = None

    def crawl_all_products(self) -> Iterable[Product]:
        """
        從首頁開始，尋找所有分類並進行爬取。
        以產生器 (Generator) 方式逐一回傳商品，以便即時處理。
        """
        logger.info(f"開始從 {self.BASE_URL} 進行完整爬取")
        self._start_browser()
        
        try:
            self.page.goto(self.BASE_URL, wait_until="domcontentloaded")
            soup = BeautifulSoup(self.page.content(), 'html.parser')
            
            # 尋找所有分類連結
            category_links = set()
            nav_links = soup.select('nav a') + soup.select('.navigation-node a') + soup.select('a')
            
            for a in nav_links:
                href = a.get('href')
                if not href: continue
                
                if '/c/' in href or '/Category/' in href:
                    full_url = href if href.startswith('http') else self.BASE_URL + href
                    category_links.add(full_url)
            
            logger.info(f"找到 {len(category_links)} 個不重複分類。")
            
            for i, cat_url in enumerate(category_links):
                logger.info(f"正在處理分類 {i+1}/{len(category_links)}: {cat_url}")
                yield from self.crawl_category(cat_url)
                time.sleep(1) # 禮貌性延遲
                
        except Exception as e:
            logger.error(f"完整爬取期間發生錯誤: {e}")
        finally:
            self._close_browser()

    def crawl_category(self, category_url: str) -> Iterable[Product]:
        """
        爬取一個分類，處理分頁，並逐一 yield 商品。
        """
        page = 0
        while True:
            if page == 0:
                current_url = category_url
            else:
                if '?' in category_url:
                        current_url = f"{category_url}&page={page}"
                else:
                        current_url = f"{category_url}?page={page}"
            
            logger.info(f"  正在擷取第 {page} 頁...")
            products = self.fetch_products_from_page(current_url)
            
            if not products:
                logger.info("  未找到商品或已達頁面末尾。")
                break
                
            for product in products:
                yield product

            logger.info(f"  在第 {page} 頁找到 {len(products)} 個商品。")
            
            # 安全中斷：限制每個分類的頁數
            if page > 10: 
                logger.warning("  已達到安全頁數限制 (10)。")
                break
                
            page += 1
            time.sleep(0.5)

    def fetch_products_from_page(self, page_url: str) -> List[Product]:
        """
        爬取分類頁面並回傳包含完整詳細資訊的商品列表。
        """
        logger.info(f"正在從以下網址擷取商品: {page_url}")
        try:
            # 前往分類頁並等待商品列表出現
            self.page.goto(page_url, wait_until="domcontentloaded")
            try:
                self.page.wait_for_selector('.product-item, sip-product-list-item', timeout=10000)
            except Exception:
                logger.warning("等待商品列表(product-item)超時，可能無商品或頁面結構不同")
                pass

        except Exception as e:
            logger.error(f"擷取 {page_url} 失敗: {e}")
            return []

        soup = BeautifulSoup(self.page.content(), 'html.parser')
        products = []

        product_items = soup.select('.product-item') or soup.select('sip-product-list-item')
        logger.info(f"找到 {len(product_items)} 個項目。開始擷取詳細資訊...")

        for item in product_items:
            # 解析基本資訊以取得網址
            basic_info = self._parse_basic_info(item)
            if basic_info and basic_info['url']:
                # 擷取完整詳細資訊
                product = self._fetch_product_details(basic_info)
                if product:
                    products.append(product)
                # 禮貌性延遲
                time.sleep(0.5)
        
        return products

    def _parse_basic_info(self, item: BeautifulSoup) -> Optional[Dict]:
        try:
            name_elem = item.select_one('.lister-name') or item.select_one('.product-list-details .name') or item.select_one('a.name')
            if not name_elem: return None
            
            name = name_elem.get_text(strip=True)
            
            link_elem = item.select_one('a')
            raw_href = link_elem['href'] if link_elem and 'href' in link_elem.attrs else ""
            
            # Fix URL doubl-prefix issue
            if raw_href.startswith('http'):
                product_url = raw_href
            else:
                product_url = self.BASE_URL + raw_href

            product_id = product_url.split('/p/')[-1] if '/p/' in product_url else "unknown"

            # Price - Regex Parsing
            # Example: "$799$213.00 / 1包" -> "799"
            price_elem = item.select_one('.product-price') or item.select_one('.price-panel')
            price_text = price_elem.get_text(strip=True) if price_elem else None
            
            if not price_text:
                # 針對部分沒有特定 class 的價格標籤: <span class="notranslate ng-star-inserted">$509</span>
                for span in item.select('span.notranslate.ng-star-inserted'):
                    # 避免抓到非價格文字，確保裡面有 $
                    if '$' in span.get_text():
                        price_text = span.get_text(strip=True)
                        break

            price = None
            if price_text:
                import re
                match = re.search(r'\$\s*([\d,]+)', price_text)
                if match:
                    price = match.group(1).replace(',', '')
                else:
                    price = price_text # Fallback

            # Stock Status (simple check from list)
            stock_status = "In Stock"
            if "Out of Stock" in item.get_text() or "缺貨" in item.get_text():
                stock_status = "Out of Stock"
            
            return {
                "id": product_id,
                "name": name,
                "url": product_url,
                "price": price,
                "stock_status": stock_status
            }
        except Exception as e:
            logger.warning(f"Error parsing basic info: {e}")
            return None

    def _fetch_product_details(self, basic_info: Dict) -> Optional[Product]:
        url = basic_info['url']
        logger.info(f"正在讀取商品詳細頁面: {basic_info['name']} ({url})")
        
        try:
            # 使用 Playwright 前往詳細頁面，等待重要資訊區塊
            self.page.goto(url, wait_until="domcontentloaded")
            try:
                self.page.wait_for_selector('.product-details-content-wrapper, #product_details', timeout=15000)
            except Exception:
                logger.warning("等待商品詳細內容超時，仍嘗試拮取已下載內容")

            soup = BeautifulSoup(self.page.content(), 'html.parser')

            # Description
            # Based on analysis: .product-details-content-wrapper seems to hold the main text
            desc_elem = soup.select_one('.product-details-content-wrapper') or soup.select_one('.product-details-wrapper') or soup.select_one('#product-details')
            description = desc_elem.get_text(separator='\n', strip=True) if desc_elem else None
            
            # Specifications
            # Logic: Look for sip-product-classification table
            specs_data = []
            specs_table = soup.select_one('sip-product-classification table') or soup.select_one('#product_specs table')
            if specs_table:
                for tr in specs_table.select('tr'):
                    key_elem = tr.select_one('.attrib')
                    val_elem = tr.select_one('.attrib-val')
                    if key_elem and val_elem:
                        key = key_elem.get_text(strip=True)
                        val = val_elem.get_text(strip=True)
                        specs_data.append(f"{key}: {val}")
                specifications = "\n".join(specs_data)
            else:
                 # Fallback
                 specs_elem = soup.select_one('.product-classifications') or soup.select_one('#specifications')
                 specifications = specs_elem.get_text(separator='\n', strip=True) if specs_elem else None

            # Category (Breadcrumb)
            category = None
            breadcrumb_ol = soup.select_one('ol.breadcrumb')
            if breadcrumb_ol:
                cats = [a.get_text(strip=True) for a in breadcrumb_ol.select('a') if a.get_text(strip=True)]
                if cats:
                    category = " > ".join(cats)

            # Exclusive Flags
            is_online_exclusive = bool(soup.select_one('.online-exclusive-icon') or "Online Exclusive" in soup.get_text())
            is_warehouse_exclusive = bool(soup.select_one('img[src*="decal_WHS2"]'))

            # 圖片 - 擷取所有
            images = []
            seen_src = set()
            
            # 策略：尋找 picture > img（基於分析）或特定圖庫類別
            candidate_imgs = []
            
            # 1. 嘗試 picture 標籤（通常用於 Spartacus/SAP Commerce 的主要商品圖片）
            for picture in soup.select('picture'):
                img = picture.select_one('img')
                if img: candidate_imgs.append(img)
                
            # 2. 嘗試圖庫覆蓋層
            candidate_imgs.extend(soup.select('.gallery-image'))
            candidate_imgs.extend(soup.select('.product-image-gallery img'))
            
            # 3. 備案：路徑中包含 'medias' 但排除頁尾/圖示的所有圖片
            if not candidate_imgs:
                for img in soup.select('img'):
                    src = img.get('src', '')
                    if '/medias/' in src and 'icon' not in src.lower() and 'logo' not in src.lower():
                         candidate_imgs.append(img)

            for img in candidate_imgs:
                src = img.get('src') or img.get('data-src')
                if src:
                    # 如果可能，過濾掉小圖示或特定不需要的路徑
                    if 'footer' in src or 'icon' in src: continue
                    
                    if not src.startswith('http'):
                         src = self.BASE_URL + src
                    
                    if src not in seen_src:
                        images.append(src)
                        seen_src.add(src)

            return Product(
                id=basic_info['id'],
                name=basic_info['name'],
                price=basic_info['price'],
                stock_status=basic_info['stock_status'],
                images=images,
                product_url=url,
                category=category,
                description=description,
                specifications=specifications,
                is_online_exclusive=is_online_exclusive,
                is_warehouse_exclusive=is_warehouse_exclusive
            )

        except Exception as e:
            logger.error(f"Error parsing details for {basic_info['name']}: {e}")
            return None
