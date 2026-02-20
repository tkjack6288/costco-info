import logging
import os
from src.database import FirestoreClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialize Firestore Client
    # Try to find credential file
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "service-account.json")
    if os.path.exists(cred_path):
        db_client = FirestoreClient(cred_path)
    else:
        try:
            db_client = FirestoreClient() # Try ADC
        except Exception as e:
            logger.error(f"Failed to initialize Firestore: {e}")
            print("請確保已設定 service-account.json 或 GOOGLE_APPLICATION_CREDENTIALS，否則無法讀取真實資料庫。")
            return

    # Fetch Documents
    collection_ref = db_client.db.collection(db_client.collection_name)
    docs = collection_ref.stream()

    print(f"\n--- Firestore Collection: {db_client.collection_name} ---\n")
    count = 0
    for doc in docs:
        count += 1
        data = doc.to_dict()
        print(f"ID: {doc.id}")
        print(f"Name: {data.get('name')}")
        print(f"Price: {data.get('price')}")
        print(f"Stock: {data.get('stock_status')}")
        print(f"Images: {len(data.get('images', []))} files")
        print(f"URL: {data.get('product_url')}")
        print(f"Desc Len: {len(data.get('description', '') or '')}")
        print(f"Specs Len: {len(data.get('specifications', '') or '')}")
        print(f"Updated: {data.get('crawled_at')}")
        print("-" * 30)
    
    if count == 0:
        print("No documents found in the collection.")
    else:
        print(f"\nTotal Documents: {count}")

if __name__ == '__main__':
    main()
