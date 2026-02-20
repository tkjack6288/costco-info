import logging
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import get_database_client
from src.models import Product

# Configure logging to file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_output.txt", mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def test_firestore_only():
    logger.info("Starting Firestore Only Integration Test...")
    
    client = get_database_client()
    
    if not client:
        logger.error("Failed to get database client.")
        return

    # Create a dummy product
    test_product = Product(
        id="test_mosodb_001",
        name="Mosodb Test Product",
        price="777",
        stock_status="In Stock",
        images=["http://example.com/moso.jpg"],
        product_url="http://example.com/moso-product",
        description="Test product for Firestore 'mosodb' collection.",
        specifications="Firestore Only Specs",
        last_updated=datetime.now().isoformat()
    )
    
    logger.info(f"Upserting product: {test_product.id}")
    client.upsert_product(test_product)
    
    logger.info("Upsert operation completed. Please check Firestore 'mosodb' collection.")

if __name__ == "__main__":
    test_firestore_only()
