from UTILS.firestore_utils import get_firestore_client
from google.cloud import firestore, storage

import os
import re

class FileService:
    def __init__(self):
        self.firestore_client = get_firestore_client()
        self.file_collection_id = "file"
        self.firestore_instance = firestore.Client(database=os.getenv("FIRESTORE_DATABASE", ""))
        self.file_collection = self.firestore_instance.collection(self.file_collection_id)
        self.bucket = storage.Client(os.getenv("PROJECT_ID")).get_bucket(os.getenv("BUCKET_NAME", ""))
        
    def upload_data(self, file_url, from_email, to_email):
        try:
    
            file_info = {"file_url": file_url, "from_email": from_email, "to_email": to_email}

            doc_ref = self.file_collection.add(file_info)
            print("FILE - Document ID :", doc_ref[1].id)
            
            return True, doc_ref  # Return Id of the created document
        except Exception as e:
            error_message = f"Error when adding data to Firestore : {str(e)}"
            return False, error_message
        
    def is_valid_email(self, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False
        return True