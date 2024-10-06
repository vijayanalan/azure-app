from flask import Flask, render_template, request, redirect, url_for
from azure.storage.blob import BlobServiceClient
import os

app = Flask(_name_)

# Initialize Blob Service Client
connection_string = "YOUR_CONNECTION_STRING"  # Replace with your connection string
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "YOUR_CONTAINER_NAME"  # Replace with your container name

@app.route('/')
def index():
    blob_list = blob_service_client.get_container_client(container_name).list_blobs()
    return render_template('index.html', blobs=blob_list)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
            blob_client.upload_blob(file.read(), overwrite=True)
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/download/<blob_name>')
def download_file(blob_name):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    with open(blob_name, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())
    return redirect(url_for('index'))

if _name_ == '_main_':
    app.run(debug=True) 
