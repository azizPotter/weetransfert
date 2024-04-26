from flask import Flask, render_template

from API.file.file_api import file_upload_route
from API.file.get_file_api import get_file_path_decrypted
from API.front.front_api import upload_view_route, download_view_route, index_view_route

app = Flask(__name__, static_folder='./UTILS',)

#Route for upload file
app.register_blueprint(file_upload_route)

#Route for getting file
app.register_blueprint(get_file_path_decrypted)

#Definition of routes for views
app.register_blueprint(download_view_route)
app.register_blueprint(upload_view_route)
app.register_blueprint(index_view_route)


if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)