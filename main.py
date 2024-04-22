from flask import Flask, render_template

from API.file.file_api import file_upload_route
from API.file.userLink_api import file_userLink_route_from
from API.file.userLink_api import file_userLink_route_to


app = Flask(__name__, static_folder='./UTILS',)

#Route for upload file
app.register_blueprint(file_upload_route)
#Route for userLink file
app.register_blueprint(file_userLink_route_from)
app.register_blueprint(file_userLink_route_to)


#Definition of routes for views
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload')
def upload():
    return render_template('upload.html')
@app.route('/download')
def download():
    return render_template('download.html')

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)