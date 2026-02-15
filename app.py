from flask import Flask, request
from flask import send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    file = request.files['file']
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return "File uploaded successfully"
    return "No file selected"

@app.route("/files")
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    
    output = "<h2>Uploaded Files</h2>"
    
    for file in files:
        output += f'''
        <p>
        <a href="/download/{file}">{file}</a> 
        | <a href="/delete/{file}">Delete</a>
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
        return f"{filename} deleted successfully"
    
    return "File not found"


if __name__ == "__main__":
    app.run(debug=True)