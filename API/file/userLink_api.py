from flask import request, jsonify, Blueprint
from google.cloud import storage
import json
import requests
import stat

from SERVICE.file.file_service import FileService

from SERVICE.crypto.crypto_service import CryptoService

from UTILS.firestore_utils import get_firestore_client

import os

BUCKET_NAME = os.getenv("BUCKET_NAME", "")

get_password_link = Blueprint("get_password_link", __name__)
get_file_path_decrypted = Blueprint("get_file_path_decrpted", __name__)


bucket = storage.Client(os.getenv("PROJECT_ID")).get_bucket(BUCKET_NAME) 
firestore_client = get_firestore_client()
file_service = FileService()
crypto_service = CryptoService()

@get_file_path_decrypted.route('/getFilePath', methods=['POST'])
def get_files():
    try:

        from_email_crypted = request.form['from_email']
        to_email_crypted = request.form['to_email']

        crypted_file_path = request.form['crypted_file_path']

        file_path = crypto_service.decrypt_url(crypted_file_path, from_email_crypted, to_email_crypted)
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        os.chmod(downloads_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)

        password = request.form['password']
        password_crypted = crypto_service.hash_data(password)
        crypted_password = file_service.get_password_by_file_path(file_path)

        if password_crypted == crypted_password[0] : 
            return jsonify({'error': 'Wrong password'}), 400

     
        # Utilisez l'API REST de Firebase Storage pour obtenir un lien de téléchargement direct
      #  response = requests.get(file_path + "?alt=media")

        # Renvoyer l'URL de téléchargement direct si la demande est réussie
        #if response.status_code == 200:
          #  download_url = response.url
           # return jsonify({'download_link': download_url}), 200
       # else:
            #return jsonify({'error': 'Failed to generate download link'}), response.status_code
  
        blob = bucket.blob(file_path)
        blob.download_to_filename(downloads_path)

        data = file_path
        return jsonify({'decrypted_file_path': data}), 200

    except Exception as e:
        return jsonify({'error': f'Error retrieving files: {str(e)}'}), 500
