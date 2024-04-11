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
        

        if 'from_email' not in request.form or 'to_email' not in request.form:
            return jsonify({'error': 'Please provide both from_email and to_email fields'}), 400
        
        from_email = request.form['from_email']
        to_email = request.form['to_email']

        # Email verification
        if not file_service.is_valid_email(from_email):
            return jsonify({'error': 'Invalid from_email format'}), 400

        if not file_service.is_valid_email(to_email):
            return jsonify({'error': 'Invalid to_email format'}), 400
        
        
        # Adds data to Firestore
        success, error_message = file_service.upload_data(file_url, from_email, to_email)

        if not success:
            return jsonify({'error': error_message}), 500

        return jsonify({'message': 'File sent successfully !', 'file_url': file_url}), 200

    except Exception as e:
        return jsonify({'error': f'Error sending file : {str(e)}'}), 500


# GET ALL METHOD - PAS SUR DE CETTE METHOD - JE LAISSE LA AU CAS OU
@file_upload_route.route('/getAllUserLink', methods=['GET'])
def get_files():
    try:
        #List object in the Cloud Storage Folder
        blobs = bucket.list_blobs(prefix=FOLDER)

        #Check if there is value
        if not blobs:
           return jsonify({'message': 'No files found'}), 200

        # Get files
        file_urls = [f'https://storage.googleapis.com/{BUCKET_NAME}/{blob.name}' for blob in blobs]

        #return all files
        return jsonify({'link': file_urls}), 200

    except Exception as e:
        return jsonify({'error': f'Error retrieving files: {str(e)}'}), 500


# GET SPECIFIC METHOD
@file_upload_route.route('/getUserLink/<filename>', methods=['GET'])
def get_file(filename):
    try:
        # Create file path
        file_path = f"{FOLDER}/{filename}"
        
        # Check if file reauested exist
        if not bucket.blob(file_path).exists():
            return jsonify({'error': 'File not found'}), 404

        # create file url
        file_url = f'https://storage.googleapis.com/{BUCKET_NAME}/{file_path}'

        #return data
        return jsonify({'userLink': file_url}), 200

    except Exception as e:
        return jsonify({'error': f'Error retrieving file: {str(e)}'}), 500