import logging
import time
import os
import sys

# 將專案根目錄加入 sys.path 以解決模組匯入問題
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.crawler import CostcoCrawler
from src.image_processor import NanoBanaProcessor
from src.database import get_database_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # 1. 初始化元件
    crawler = CostcoCrawler()
    image_processor = NanoBanaProcessor()
    
    # 初始化資料庫
    # 預設僅使用 Firestore (mosodb)
    logger.info("Initializing database (Firestore Only)...")
    
    db_client = get_database_client()
    if db_client:
        logger.info("Database client(s) initialized successfully.")
    else:
        logger.warning("No database client initialized. Data will not be saved.")

    # 2. 爬取資料
    # target_url = "https://www.costco.com.tw/c/hot-buys" 
    # 現在我們爬取整個網站（或從首頁開始）
    logger.info("開始完整網站爬取...")
    products = crawler.crawl_all_products()
    # logger.info(f"總共爬取了 {len(products)} 個商品。")
    logger.info("開始處理商品串流...")

    # 3. 處理與儲存
    # total_products = len(products) # products is now a generator
    for i, product in enumerate(products, 1):
        logger.info(f"[{i}] 正在處理商品: {product.name} (ID: {product.id})")
        # 處理圖片 (Mock Nano Bana)
        # 處理所有並可能將其保留在單獨的列表或更新中
        processed_images = []
        for img_url in product.images:
            processed = image_processor.process_image(img_url)
            processed_images.append(processed)
        
        # 使用處理後的圖片更新商品
        product.images = processed_images

        # 儲存至 DB
        if db_client:
            db_client.upsert_product(product)
        else:
            logger.info(f"[Mock DB] Validating product: {product.name} (Images: {len(product.images)})")

    logger.info("每日更新完成。")

if __name__ == '__main__':
    main()
