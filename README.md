# Beginner Cloud Server – File Storage Backend

A backend project built with Python and Flask that simulates a simple cloud-based file storage system.

## Project Description

This is a beginner-level backend project built to understand how real-world file storage systems work, including file handling, metadata management, database integration, and basic security practices.

Users can upload, download, and delete files through a web interface. The backend handles storage, metadata tracking, and maintains consistency between the file system and the database.


## Features

* Upload files through a web form
* Store files in a server directory
* Save file metadata (original name, stored name, upload time) in a SQLite database
* View all uploaded files
* Download files from the server
* Delete files and remove their metadata from the database


## Technologies Used

* Python
* Flask
* SQLite
* Werkzeug
* HTML (basic interface)
* Git & GitHub


## Project Architecture

```
        Client (Browser)
              ↓
        Flask Backend
              ↓
    SQLite Database (file metadata)
              ↓
    Server Storage (uploads folder)
```


## Project Structure

```
cloud-file-storage/
│
├── app.py
├── uploads/
├── database/
│   └── files.db
├── README.md
```


## How to Run the Project

1. Clone the repository
```
git clone https://github.com/yash-kumar-26/beginner_cloud_server.git
```
2. Go to project folder
```
cd beginner_cloud_server
```
3. Install dependencies
```
pip install flask
```
4. Run the server
```
python app.py
```
5. Open in browser
```
http://127.0.0.1:5000
```

## Technical Decisions

**Metadata stored in database, not folder:**
The uploads folder only stores the physical file. The original filename, stored filename, and upload time are kept in SQLite. This allows proper file listing, sorting, and future querying — scanning a folder directly is not scalable and loses the original filename after renaming.

**UUID for unique filenames:**
Each uploaded file is renamed using a UUID prefix before saving to disk. This prevents file collisions when two users upload files with the same name simultaneously — something a timestamp-based approach cannot guarantee.

**Database-driven file listing:**
The file list is fetched from the database rather than scanning the uploads folder with os.listdir(). This is more reliable, scalable, and allows displaying the original filename to users while using the internal stored name for operations.

**Consistency between storage and database:**
Every delete operation removes both the physical file and its database record together. If only one is removed, the system becomes inconsistent — either showing files that no longer exist or storing orphaned files that are invisible and wasting disk space.


## Security Considerations

These were deliberately implemented to reflect real backend security thinking:

* **Path traversal prevention**: secure_filename() strips dangerous characters like ../ from uploaded filenames that could otherwise overwrite server files

* **File type validation**: only whitelisted extensions are accepted (txt, pdf, png, jpg, jpeg, gif, docx). Extension-based validation is used with awareness of its limitations — MIME type checking is a planned improvement

* **XSS prevention**: all user-supplied data (filenames) is escaped before being inserted into HTML output, preventing malicious scripts from executing in the browser

* **Database connection safety**: try/finally blocks ensure database connections are always closed, even when errors occur, preventing connection leaks

* **Delete via POST**: the delete action uses a POST form instead of a GET link, preventing search engine crawlers or prefetch tools from accidentally triggering deletions

## Known Limitations

* No user authentication — all files are accessible to anyone
* No file size limit
* No cloud storage — files are stored locally, not on S3 or similar
* No pagination — all files are listed at once
* Extension-based file validation only — MIME type checking not yet implemented


## Future Improvements

* User authentication — isolate files per user, prevent unauthorized access
* Cloud storage (Amazon S3) — move file storage off the local server for scalability and reliability
* MIME type validation — check actual file content using python-magic, not just the extension
* File size limits — prevent large uploads from consuming server resources
* Pagination — load files in batches for performance at scale
* CSRF protection — add token-based protection to POST forms