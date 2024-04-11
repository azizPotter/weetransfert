from UTILS.firestore_utils import get_firestore_client
from google.cloud import firestore, storage

import os

class FileService:
    def __init__(self):
        self.firestore_client = get_firestore_client()
        self.file_collection_id = "file"
        self.firestore_instance = firestore.Client(database=os.getenv("FIRESTORE_DATABASE", ""))
        self.file_collection = self.firestore_instance.collection(self.file_collection_id)
        self.bucket = storage.Client(os.getenv("PROJECT_ID")).get_bucket(os.getenv("BUCKET_NAME", ""))
        
    def upload_csv_data(self, file_url):
        try:
    
            file_info = {"file_url": file_url}

            doc_ref = self.file_collection.add(file_info)
            print("FILE - Document ID :", doc_ref[1].id)
            
            return True, doc_ref  # Return Id of the created document
        except Exception as e:
            error_message = f"Error when adding data to Firestore : {str(e)}"
            return False, error_message

    def getUserLinkFrom(self, fromMail):
        try:
            data = []
            collection_ref = self.firestore_client.collection(self.file_collection_id)
            docs = collection_ref.where('from_email', '==', fromMail).stream()

            for doc in docs:
                doc_data = doc.to_dict()
                if 'file_url' in doc_data:
                    data.append(doc_data['file_url'])
        
            return data
        except Exception as e:
            error_message = f"Error when getting data to Firestore : {str(e)}"
            return False, error_message

    def getUserLinkTo(self, toMail):
        try:
            data = []
            collection_ref = self.firestore_client.collection(self.file_collection_id)
            docs = collection_ref.where('to_email', '==', toMail).stream()

            for doc in docs:
                doc_data = doc.to_dict()
                if 'file_url' in doc_data:
                    data.append(doc_data['file_url'])
        
            return data
        except Exception as e:
            error_message = f"Error when getting data to Firestore : {str(e)}"
            return False, error_message