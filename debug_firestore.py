import os
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import firestore as google_firestore
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_firestore():
    cred_path = "service-account.json"
    database_id = "mosodb"
    logger.info(f"Checking for {cred_path}...")
    
    if os.path.exists(cred_path):
        logger.info(f"Found {cred_path}. Attempting to initialize with it.")
        try:
            cred = credentials.Certificate(cred_path)
            # Check if app is already init
            try:
                firebase_admin.get_app()
            except ValueError:
                firebase_admin.initialize_app(cred)
            
            # db = firestore.client() # Old way
            # Use google.cloud.firestore directly to specify database
            logger.info(f"Connecting to database: {database_id}")
            db = google_firestore.Client(credentials=cred.get_credential(), project=cred.project_id, database=database_id)
            
            logger.info("Firestore client initialized. Attempting write test...")
            
            # Write a test document
            doc_ref = db.collection("test_debug").document("ping")
            doc_ref.set({"message": "Hello from debug script", "timestamp": firestore.SERVER_TIMESTAMP})
            
            logger.info(f"Successfully wrote to 'test_debug/ping' in database '{database_id}'.")
            
        except Exception as e:
            logger.error(f"Error connecting/writing to Firestore with cert: {e}")
    else:
        logger.warning(f"{cred_path} not found. Trying ADC...")
        try:
            try:
                firebase_admin.get_app()
            except ValueError:
                firebase_admin.initialize_app()
            
            logger.info(f"Connecting to database: {database_id} using ADC")
            db = google_firestore.Client(database=database_id)
            
            doc_ref = db.collection("test_debug").document("ping_adc")
            doc_ref.set({"message": "Hello from ADC", "timestamp": firestore.SERVER_TIMESTAMP})
            logger.info(f"Successfully wrote to 'test_debug/ping_adc' using ADC in database '{database_id}'.")
            
        except Exception as e:
            logger.error(f"Error connecting/writing to Firestore with ADC: {e}")

if __name__ == "__main__":
    test_firestore()
