from flask import Flask, render_template, Blueprint

upload_view_route = Blueprint("upload_view_route", __name__)
download_view_route = Blueprint("download_view_route", __name__)
index_view_route=Blueprint("index_view_route",__name__)

@upload_view_route.route('/upload_view')
def upload_view():
    return render_template('upload.html')

@download_view_route.route('/download_view')
def download_view():
    return render_template('download.html')

@index_view_route.route('/')
def index_view():
    return render_template('index.html')

