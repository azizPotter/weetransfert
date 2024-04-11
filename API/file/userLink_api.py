from flask import request, jsonify, Blueprint
from google.cloud import storage
import json

from SERVICE.file.file_service import FileService

from UTILS.firestore_utils import get_firestore_client

import os

file_userLink_route_from = Blueprint("file_userLink_route_from", __name__)
file_userLink_route_to = Blueprint("file_userLink_route_to", __name__)

firestore_client = get_firestore_client()
file_service = FileService()


@file_userLink_route_from.route('/getUserLinkFrom/<fromMail>', methods=['GET'])
def get_files(fromMail):
    try:

        data = file_service.getUserLinkFrom(fromMail)
        return jsonify({'file_urls': data}), 200

    except Exception as e:
        return jsonify({'error': f'Error retrieving files: {str(e)}'}), 500


@file_userLink_route_to.route('/getUserLinkTo/<toMail>', methods=['GET'])
def get_files(toMail):
    try:

        data = file_service.getUserLinkTo(toMail)
        return jsonify({'file_urls': data}), 200

    except Exception as e:
        return jsonify({'error': f'Error retrieving files: {str(e)}'}), 500