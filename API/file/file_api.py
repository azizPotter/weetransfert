from flask import request, jsonify, Blueprint
from google.cloud import storage

from SERVICE.file.file_service import FileService

from UTILS.firestore_utils import get_firestore_client


import os

file_upload_route = Blueprint("file_upload_route", __name__)


BUCKET_NAME = os.getenv("BUCKET_NAME", "")
FOLDER = 'file'


#  Get client
firestore_client = get_firestore_client()

bucket = storage.Client(os.getenv("PROJECT_ID")).get_bucket(BUCKET_NAME) 

file_service = FileService()


# POST METHOD
@file_upload_route.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Verify if the folder is in the request
        if 'file' not in request.files:
            return jsonify({'error': 'Please provide the required files'}), 400

        file = request.files['file']

        # Check if the folder has a name
        if file.filename == '':
            return jsonify({'error': 'Files must have names'}), 400
        
        # Folder for store the file 
        file_bucket = bucket.blob(f'{FOLDER}/{file.filename}')
        file_bucket.upload_from_file(file)

        # File URL in GCS
        file_url = f'https://storage.googleapis.com/{BUCKET_NAME}/{FOLDER}/{file.filename}'
        
        from_email = request.form['from_email']
        to_email = request.form['to_email']
        expiration_date = request.form['expiration_date']
        password = request.form['password']

        # Adds data to Firestore
        success, error_message = file_service.upload_data(file_url, from_email, to_email, expiration_date, password)

        if not success:
            return jsonify({'error': error_message}), 500

        return jsonify({'message': 'File sent successfully !', 'file_url': file_url}), 200

    except Exception as e:
        return jsonify({'error': f'Error sending file : {str(e)}'}), 500