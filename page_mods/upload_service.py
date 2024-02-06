import pickle
import os
import mimetypes
import time;


# --- Create the private and public uploaded file dicts ---


class file:

    def __init__(self, name: bytes, comment: bytes, pub: bool, content_type: bytes, file_data: bytes, file_extension: str):

        # NOTE might want to make this a random number as then it is # even harder for an 
        # attacker to find their uploaded file on the server the actual file name.
        self.id = str(get_file_count()) + file_extension
        self.name = name
        self.comment = comment
        self.pub = pub                  # If true, is public. If false, private. 
        self.content_type = content_type
        self.file_data = file_data;
        self.time_uploaded = time.time();


def get_file_count():
    """ Returns the next file number to label the uploaded file. """

    file_counter = None;
    with open("file_counter.txt", "r") as open_file:
        file_counter = int(open_file.read());
    with open("file_counter.txt", "r+") as write_file:
        write_file.write(str(file_counter + 1));
    return file_counter;

# The fallowing is an example of what POST_DATA looks like
# {b'file_data': [({b'content-type': b' text/plain', b'name': b'file_data', b'filename': b'test.txt'}, b'test\n')], b'comment': [({b'name': b'comment'}, b'hi')], b'pub_or_priv': [({b'name': b'pub_or_priv'}, b'Private')]}
# NOTE might want to consider if getting a post request that is not of exctype "multipart/form-data"


def upload_data(POST_DATA: dict):
    """ This method is used to upload a file. It is ran by upload_service.html to handle the input of a form sent by upload.html.
    It will create an instance of the file class with all the information passed to it by the form about the file. It will then 
    save the file class as a pickle and finally write the file data to the correct directory depending on if it is public or 
    private. """

    # TODO - need to create a way that overwrites the old one if uploading with the same name. 

    # --- Create the in program "pickle jars" to store the data pulled-out from the pickle files 
    PUB_FILES = {};
    PRIV_FILES = {};

    # Open the pickled files for public and private files and populate our python dicts
    try: 
        pub_pickle = open('html/pub_files.pickle', 'rb');
        PUB_FILES = pickle.loads(pub_pickle.read());
        pub_pickle.close();
    except:
        print("\nCouldn't open [pub_files.pickle]. Likely doesn't exist.")
    try: 
        priv_pickle = open('html/priv_files.pickle', 'rb');
        PRIV_FILES = pickle.loads(priv_pickle.read());
        priv_pickle.close();
    except:
        print("\nCouldn't open [priv_files.pickle]. Likely doesn't exist.")

    # Create the class to represent the file. NOTE the content type is [1:] because for some reason it gives a space before???
    file_extension = mimetypes.guess_extension(POST_DATA[b'file_data'][0][0][b'content-type'][1:].decode());
    name = POST_DATA[b'file_data'][0][0][b'filename'];
    comment = POST_DATA[b'comment'][0][1];
    content_type = POST_DATA[b'file_data'][0][0][b'content-type'][1:];
    public = False if POST_DATA[b'pub_or_priv'][0][1] == b'Private' else True;
    file_data = POST_DATA[b'file_data'][0][1];
    new_file = file(name, comment, public, content_type, file_data, file_extension);

    # Put the uploaded file into the appropriate dictionary (pickle jar lol)
    if public:
        PUB_FILES[name] = new_file;
    else:
        PRIV_FILES[name] = new_file;

    # Put them pickles back in their jars (their pickle folders)
    pickled_pub_files = pickle.dumps(PUB_FILES)
    with open('html/pub_files.pickle', 'bw') as pickle_file:
        pickle_file.write(pickled_pub_files);
    pickled_priv_files = pickle.dumps(PRIV_FILES)
    with open('html/priv_files.pickle', 'bw') as pickle_file:
        pickle_file.write(pickled_priv_files);

    # Return certain html in response indicating status of upload
    if file_extension is None:
        return """
            <p>Your file has been uploaded but the type of the file was not found.</p>
            <a href="index.html">Go Home</a>
        """
    else: 
        return f"""
            <p>success. Your file has been uploaded.</p>
            <a href="index.html">Go Home</a>
        """