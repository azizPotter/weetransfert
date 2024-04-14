from flask import jsonify
from UTILS.firestore_utils import get_firestore_client
from google.cloud import firestore, storage

from SERVICE.crypto.crypto_service import CryptoService

import os
import re
import base64

class FileService:
    def __init__(self):
        self.firestore_client = get_firestore_client()
        self.file_collection_id = "file"
        self.firestore_instance = firestore.Client(database=os.getenv("FIRESTORE_DATABASE", ""))
        self.file_collection = self.firestore_instance.collection(self.file_collection_id)
        self.bucket = storage.Client(os.getenv("PROJECT_ID")).get_bucket(os.getenv("BUCKET_NAME", ""))
        self.crypto_service = CryptoService()
        
    def upload_data(self, file_url, from_email, to_email):
        try:
            #Encrypted data
            encrypted_from_email = self.crypto_service.hash_data(from_email)
            encrypted_to_email = self.crypto_service.hash_data(to_email)
    
            file_info = {"file_url": file_url, "from_email": encrypted_from_email, "to_email": encrypted_to_email}

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
        
          
    def getUserLinkFrom(self, fromMail):
        try:
            #Encrypted data
            crypted_from_mail = self.crypto_service.hash_data(fromMail)
            
            data = []
            collection_ref = self.firestore_client.collection(self.file_collection_id)
            docs = collection_ref.where('from_email', '==', crypted_from_mail).stream()

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
            #Encrypted data
            crypted_to_mail = self.crypto_service.hash_data(toMail)
            
            data = []
            collection_ref = self.firestore_client.collection(self.file_collection_id)
            docs = collection_ref.where('to_email', '==', crypted_to_mail).stream()

            for doc in docs:
                doc_data = doc.to_dict()
                if 'file_url' in doc_data:
                    data.append(doc_data['file_url'])
        
            return data
        except Exception as e:
            error_message = f"Error when getting data to Firestore : {str(e)}"
            return False, error_message