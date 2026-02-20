import logging
import os
from typing import Optional, Protocol
from google.cloud import firestore
from google.oauth2 import service_account
import firebase_admin
from firebase_admin import credentials, firestore as admin_firestore

from src.models import Product

logger = logging.getLogger(__name__)

class DatabaseClient(Protocol):
    def upsert_product(self, product: Product) -> None:
        ...

class FirestoreClient:
    def __init__(self, cred_path: Optional[str] = "service-account.json"):
        # 依需求將 Collection 名稱設為 product_info
        self.collection_name = "product_info"
        self.database_id = "mosodb"
        
        try:
            # 優先嘗試使用 service account 檔案
            if cred_path and os.path.exists(cred_path):
                logger.info(f"使用憑證檔案初始化 Firestore: {cred_path} (Database: {self.database_id})")
                cred = credentials.Certificate(cred_path)
                try:
                    firebase_admin.get_app()
                except ValueError:
                    firebase_admin.initialize_app(cred)
                
                # 使用 google.cloud.firestore.Client 直接指定資料庫
                # 取得 project_id
                project_id = cred.project_id
                self.db = firestore.Client(credentials=cred.get_credential(), project=project_id, database=self.database_id)

            else:
                # 使用 Application Default Credentials (ADC)
                logger.info(f"未找到憑證檔案或未指定，嘗試使用 ADC 初始化 Firestore (Database: {self.database_id})...")
                self.db = firestore.Client(database=self.database_id)
                
            logger.info(f"Firestore client initialized successfully. Database: {self.database_id}, Collection: {self.collection_name}")
            
        except Exception as e:
            logger.error(f"Firestore 初始化失敗: {e}")
            raise

    def upsert_product(self, product: Product):
        try:
            doc_ref = self.db.collection(self.collection_name).document(product.id)
            doc_ref.set(product.to_dict(), merge=True)
            logger.info(f"已更新/新增商品 {product.id} 至 Firestore ({self.collection_name})。")
        except Exception as e:
            logger.error(f"寫入 Firestore 失敗 Product {product.id}: {e}")

def get_database_client(db_type: str = "firestore") -> Optional[DatabaseClient]:
    """
    回傳 Firestore Client。
    忽略 db_type 參數，強制使用 Firestore (mosodb)。
    """
    try:
        return FirestoreClient()
    except Exception as e:
        logger.error(f"無法初始化 Firestore Client: {e}")
        return None
