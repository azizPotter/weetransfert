from flask import request, jsonify, Blueprint
from google.cloud import storage
import json
import requests
import stat
import datetime

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
        crypted_file_path = request.form['crypted_file_path'].replace(" ", "+")

        file_path = crypto_service.decrypt_url(crypted_file_path, from_email_crypted, to_email_crypted)

        password = request.form['password']
        password_crypted = crypto_service.hash_data(password)
        crypted_password = file_service.get_password_by_file_path(file_path)

        expiration_date = file_service.get_expiration_date(file_path)
        is_downloadable = file_service.is_downloadable(file_path)

        if not is_downloadable[0]:
            return jsonify({'error': 'Connot download it'}), 400

        if password_crypted != crypted_password[0] : 
            return jsonify({'error': 'Wrong password'}), 400

        print(expiration_date[0])

        if not file_service.is_valid_expiration_date(expiration_date[0]) :
            file_service.update_download_boolean(file_path)
            return jsonify({'error': 'Obselete File'}), 400


        return jsonify({'file_path': file_path}), 200

    except Exception as e:
        return jsonify({'error': f'Error retrieving files: {str(e)}'}), 500
