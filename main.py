from flask import Flask, render_template

from API.file.file_api import file_upload_route
from API.file.userLink_api import file_userLink_route_from
from API.file.userLink_api import file_userLink_route_to
from API.front.front_api import upload_view_route, download_view_route, index_view_route

app = Flask(__name__, static_folder='./UTILS',)

#Route for upload file
app.register_blueprint(file_upload_route)
#Route for userLink file
app.register_blueprint(file_userLink_route_from)
app.register_blueprint(file_userLink_route_to)

#Definition of routes for views
app.register_blueprint(download_view_route)
app.register_blueprint(upload_view_route)
app.register_blueprint(index_view_route)


if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)