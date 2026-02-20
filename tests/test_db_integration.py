import logging
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import get_database_client
from src.models import Product

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_integration():
    logger.info("Starting Database Integration Test...")
    
    # Test cases: 'mongo', 'firestore', 'both'
    # For now, we test 'both' to cover everything
    db_type = "both"
    logger.info(f"Testing with DB_TYPE={db_type}")
    
    client = get_database_client(db_type)
    
    if not client:
        logger.error("Failed to get database client.")
        return

    # Create a dummy product
    test_product = Product(
        id="test_integration_001",
        name="Integration Test Product",
        price="888",
        stock_status="In Stock",
        images=["http://example.com/integration.jpg"],
        product_url="http://example.com/integration-product",
        description="Test product for dual DB write.",
        specifications="Dual DB Specs",
        last_updated=datetime.now().isoformat()
    )
    
    logger.info(f"Upserting product: {test_product.id}")
    client.upsert_product(test_product)
    
    logger.info("Upsert operation completed. Please check:")
    logger.info("1. MongoDB 'costco_db.products'")
    logger.info("2. Firestore 'products' collection")

if __name__ == "__main__":
    test_integration()
