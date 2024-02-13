# EEE401-Lab2
This is a web application developed for the course EEE401 from RMC.
The goal of this lab is to develop a secure web application that can be used to upload and host different files

# Dependencies
* Uses the library mimetype to find the file extension of the uploaded file based on the http MIME
* Uses OS library
* Uses pickle library to store the file metadata
* bleach to sanitize inputs
* magic to check the type of file

# Directories to create
Must create private_files, private_pickle, public_files and, public_pickle directory within the application root directory.