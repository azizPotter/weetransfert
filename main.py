from flask import Flask

from API.file.file_api import file_upload_route

app = Flask(__name__, static_folder='./UTILS',)


#Route for upload file
app.register_blueprint(file_upload_route)

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)