"""

    The fallowing is an example of what POST_DATA looks like
    {b'file_data': [({b'content-type': b' text/plain', b'name': b'file_data', b'filename': b'test.txt'}, b'test\n')], b'comment': [({b'name': b'comment'}, b'hi')], b'pub_or_priv': [({b'name': b'pub_or_priv'}, b'Private')]}
    NOTE might want to consider if getting a post request that is not of exctype "multipart/form-data"

"""

import pickle
import os
import mimetypes
import time;
import bleach;
import magic


# --- Create the private and public uploaded file dicts ---


class file:

    def __init__(self, name: bytes, comment: bytes, pub: bool, file_data: bytes, file_extension: str):

        self.comment = sanitize(comment.decode())
        self.name = sanitize(name.decode()); 
        self.pub = pub                              # If true, is public. If false, private. 
        self.file_extension = sanitize(file_extension) if file_extension is not None else ""
        self.time_uploaded = time.time();
        try:
            self.file_data = sanitize(file_data.decode()).encode(); 
        except:
            self.file_data = file_data;
            print(self.name + " could not be sanitized");


def sanitize(input: str):
    """ Sanitizes the string inputted through the argments."""
    input = input.replace(f"<%%",f"&lt&#37&#37");
    input = input.replace(f"<%", f"&lt&#37");
    input = input.replace(f"%%>", f"&#37&#37&gt");
    input = input.replace(f"%>", "&#37&gt");
    
    # sanitizes bash commands
    input = input.replace(f"&", f"\&")
    input = input.replace(f"|", f"\|")
    input = input.replace(f";", f"\;")
    bleach.clean(input);
    return input;


def upload_data(POST_DATA: dict):
    """ This method is used to upload a file. It is ran by upload_service.html to handle the input of a form sent by upload.html.
    It will create an instance of the file class with all the information passed to it by the form about the file. It will then 
    save the file class as a pickle and finally write the file data to the correct directory depending on if it is public or 
    private. """

    # --- Create the in program "pickle jars" to store the data pulled-out from the pickle files 
    PICKLE_JAR = {};

    # Create the class to represent the file. NOTE the content type is [1:] because for some reason it gives a space before???
    name = POST_DATA[b'file_data'][0][0][b'filename'];
    comment = POST_DATA[b'comment'][0][1];
    public = False if POST_DATA[b'pub_or_priv'][0][1] == b'Private' else True;
    file_data = POST_DATA[b'file_data'][0][1];
    file_extension = mimetypes.guess_extension(magic.from_buffer(file_data, mime=True)) # magic library helps determine the file type depending on its data. 
    new_file = file(name, comment, public, file_data, file_extension);
    
    # Open the pickled files for public and private files. Put the uploaded file into the dictionary (pickle jar lol)
    try: 
        if public:
            pickle_file = open('html/pub_files.pickle', 'rb');
            PICKLE_JAR = pickle.loads(pickle_file.read());
            pickle_file.close();
        else:
            pickle_file = open('html/priv_files.pickle', 'rb');
            PICKLE_JAR = pickle.loads(pickle_file.read());
            pickle_file.close();
    except:
        print("\nCouldn't open [pub_files.pickle/priv_files.pickle]. Likely doesn't exist.")
    PICKLE_JAR[new_file.name] = new_file;

    # Put them pickles back in their jars (their pickle folders)
    pickled_files = pickle.dumps(PICKLE_JAR)
    if public:
        with open('html/pub_files.pickle', 'bw') as pickle_file:
            pickle_file.write(pickled_files);
    else:
        with open('html/priv_files.pickle', 'bw') as pickle_file:
            pickle_file.write(pickled_files);

    # Return certain html in response indicating status of upload
    if file_extension is None:
        return """
            <p>Your file has been uploaded but the type of the file was not found.</p>
            <a href="index.html">Go Home</a>
        """
    else: 
        return f"""
            <p>Success. Your file has been uploaded.</p>
            <a href="index.html">Go Home</a>
        """
