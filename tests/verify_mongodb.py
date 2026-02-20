import logging
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import MongoDBClient
from src.models import Product

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_mongodb():
    logger.info("Testing MongoDB Connection...")
    try:
        client = MongoDBClient()
        
        # Create a dummy product
        test_product = Product(
            id="test_mongo_001",
            name="Test Product for MongoDB",
            price="999",
            stock_status="In Stock",
            images=["http://example.com/img.jpg"],
            product_url="http://example.com/product",
            description="This is a test product.",
            specifications="Test Specs",
            last_updated=datetime.now().isoformat()
        )
        
        logger.info(f"Attempting to upsert product: {test_product.id}")
        client.upsert_product(test_product)
        
        # Verify read back (optional, but good for verification)
        saved_doc = client.collection.find_one({"id": "test_mongo_001"})
        if saved_doc:
            logger.info(f"Verification Check: Successfully found document in MongoDB: {saved_doc['_id']}")
            logger.info("MongoDB migration verification PASSED.")
        else:
            logger.error("Verification Check: Document NOT found after upsert.")

    except Exception as e:
        logger.error(f"MongoDB test failed: {e}")
        # Hint for user if connection fails
        if "Connection refused" in str(e) or "Timeout" in str(e):
            logger.warning("請確認 MongoDB 是否已在本地啟動 (localhost:27017)。")

if __name__ == "__main__":
    test_mongodb()
