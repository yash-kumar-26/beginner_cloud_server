from flask import Flask, request, send_file
import os
import time
import uuid
import sqlite3
from werkzeug.utils import secure_filename
from markupsafe import escape
from google.cloud import storage
import io

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}

#GCS Configuration
GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 'yash-file-uploads')
storage_client = storage.Client()
bucket = storage_client.bucket(GCS_BUCKET_NAME)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return '''
     <h2>File Upload</h2>
    <form method="POST" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    <br><br>
<a href="/files">View Uploaded Files</a>
    '''


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file or file.filename == '':
        return "No file uploaded", 400
    
    if not allowed_file(file.filename):
        return "File type not allowed", 400

    unique_id = str(uuid.uuid4())
    new_filename = unique_id + "_" + secure_filename(file.filename)
    blob = bucket.blob(new_filename)
    blob.upload_from_file(file, content_type=file.content_type)
    conn = None
    try:
        conn = sqlite3.connect('database/files.db')
        cursor = conn.cursor()

        cursor.execute(
        "INSERT INTO files (original_name, saved_name, upload_time) VALUES (?, ?, ?)",
        (file.filename, new_filename, str(int(time.time())))
        )

        conn.commit()
    finally:
        if conn:
            conn.close()
    return "File uploaded successfully"
 
@app.route("/files")
def list_files():
    conn = None
    try:
        conn = sqlite3.connect('database/files.db')
        cursor = conn.cursor()

        cursor.execute("SELECT original_name, saved_name FROM files")
        files = cursor.fetchall()
    
    finally:
        if conn:
            conn.close()

    output = "<h2>Uploaded Files</h2>"
    
    for file in files:
        original_name = file[0]
        saved_name = file[1]

        output += f'''
        <p>
        {escape(original_name)}
        | <a href="/download/{escape(saved_name)}">Download</a>
        | <form method="POST" action="/delete/{escape(saved_name)}">
        <button type="submit">Delete</button>
        </form>
        </p>
        '''

    return output

@app.route('/download/<filename>')
def download_file(filename):
    blob = bucket.blob(filename)
    file_data = blob.download_as_bytes()
    return send_file(io.BytesIO(file_data), download_name=filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    blob = bucket.blob(filename)
    
    if blob.exists():
        blob.delete()

        conn = None
        try:
            conn = sqlite3.connect('database/files.db')
            cursor = conn.cursor()

            cursor.execute("DELETE FROM files WHERE saved_name = ?", (filename,))
            conn.commit()
        finally:
            if conn:
                conn.close()
        return f"{filename} deleted successfully"
    
    return "File not found"

def init_db():
    conn = None
    try:
        conn = sqlite3.connect('database/files.db')
        cursor = conn.cursor()
    
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_name TEXT,
                saved_name TEXT,
                upload_time TEXT
            )
        ''')
    
        conn.commit()
    finally:
        if conn:
            conn.close()

init_db()


if __name__ == "__main__":
    #host='0.0.0.0' allows external connection, required for cloud deployment
    app.run(host='0.0.0.0', debug=True)