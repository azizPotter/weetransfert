from UTILS.firestore_utils import get_firestore_client
from google.cloud import firestore, storage

from SERVICE.crypto.crypto_service import CryptoService

import os
import re
import datetime

class FileService:
    def __init__(self):
        self.firestore_client = get_firestore_client()
        self.file_collection_id = "file"
        self.firestore_instance = firestore.Client(database=os.getenv("FIRESTORE_DATABASE", ""))
        self.file_collection = self.firestore_instance.collection(self.file_collection_id)
        self.bucket = storage.Client(os.getenv("PROJECT_ID")).get_bucket(os.getenv("BUCKET_NAME", ""))
        self.crypto_service = CryptoService()
        
    def upload_data(self, file_url, from_email, to_email, expiration_date, password):
        try:
            # Check the validity of the email
            if not self.is_valid_email(from_email) or not self.is_valid_email(to_email):
                return False, "Invalid email address"
            
            # Check the validity of the expiration date
            if not self.is_valid_expiration_date(expiration_date):
                return False, "Invalid expiration date"
        
            #Encrypted data
            encrypted_from_email = self.crypto_service.hash_data(from_email)
            encrypted_to_email = self.crypto_service.hash_data(to_email)
            encrypted_password = self.crypto_service.hash_data(password)
    
            file_info = {
                "file_url": file_url, 
                "from_email": encrypted_from_email, 
                "to_email": encrypted_to_email,
                "expiration_date": expiration_date,
                "password": encrypted_password,
                "downloadable": True}

            doc_ref = self.file_collection.add(file_info)
            print("FILE - Document ID :", doc_ref[1].id)
            
            return True, doc_ref  # Return Id of the created document
        except Exception as e:
            error_message = f"Error when adding data to Firestore : {str(e)}"
            return False, error_message
        
    def is_valid_email(self, email):
        #Check format of the email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False
        return True
    
    def is_valid_expiration_date(self, expiration_date):
        # Check that date is in the future and have valid format
        try:
            expiration_date = datetime.datetime.strptime(expiration_date, '%d-%m-%Y')
            current_date = datetime.datetime.now()
            return expiration_date > current_date
        except ValueError:
            return False
        
          
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