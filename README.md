# Beginner Cloud Server – File Storage Backend

A backend project built with Python and Flask that simulates a simple cloud-based file storage system.

## Project Description

This project is a beginner-level backend system built using Python and Flask that simulates a simple cloud file storage service. Users can upload, download, view, and delete files through a web interface.

The goal of this project was to understand how backend systems handle file storage, metadata management, and HTTP request handling.


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
* HTML (basic interface)
* Git & GitHub


## Project Architecture

        Client (Browser)
              ↓
        Flask Backend
              ↓
    SQLite Database (file metadata)
              ↓
    Server Storage (uploads folder)


## Project Structure

cloud-file-storage/
│
├── app.py
├── uploads/
├── database/
│   └── files.db
├── README.md


## How to Run the Project

1. Clone the repository

git clone https://github.com/yash-kumar-26/beginner_cloud_server.git

2. Go to project folder

cd beginner_cloud_server

3. Install dependencies

pip install flask

4. Run the server

python app.py

5. Open in browser

http://127.0.0.1:5000


## Backend Concepts Implemented

* REST-style route handling
* File upload handling with Flask
* Secure file storage using unique filenames
* Database integration using SQLite
* Metadata management
* Server-side file operations (save, delete, retrieve)


## Learning Objectives

This project helped me understand:

* how backend servers handle file uploads
* how metadata and file storage are separated
* database operations using SQLite
* building REST endpoints in Flask
* designing a simple storage system architecture


## Future Improvements

* Add user authentication
* Store files in cloud storage such as Amazon S3
* Implement pagination for large file lists
* Add file size validation and security checks
* Improve frontend interface