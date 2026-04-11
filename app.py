from flask import Flask, request
from flask import send_from_directory
import os
import time
import uuid
import sqlite3
from werkzeug.utils import secure_filename
from markupsafe import escape

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}

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
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
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
        | <a href="/delete/{escape(saved_name)}">Delete</a>
        </p>
        '''

    return output

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)

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
    app.run(debug=True)