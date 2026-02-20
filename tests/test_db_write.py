
import logging
import os
import sys

# 將專案根目錄加入 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import get_database_client
from src.models import Product

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_db_write():
    logger.info("開始測試 Firestore 寫入...")
    
    db_client = get_database_client()
    if not db_client:
        logger.error("無法初始化資料庫客戶端！")
        return

    # 建立測試產品
    test_product = Product(
        id="test_product_001",
        name="測試商品 (Test Product)",
        price="999",
        product_url="https://www.costco.com.tw/test",
        stock_status="In Stock",
        images=["https://www.costco.com.tw/medias/test.jpg"],
        description="這是一個測試商品，用於驗證資料庫寫入功能。",
        specifications="測試: 通過"
    ) 

    logger.info(f"嘗試寫入測試商品: {test_product.id}")
    try:
        db_client.upsert_product(test_product)
        logger.info("測試寫入完成，請檢查 Firestore (Database: mosodb, Collection: product_info) 是否有 id 為 'test_product_001' 的文件。")
    except Exception as e:
        logger.error(f"寫入測試失敗: {e}")

if __name__ == "__main__":
    test_db_write()
