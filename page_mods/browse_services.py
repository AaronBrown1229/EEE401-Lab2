
"""

Description: 

    Uhh sup y'all I don't exactly know how I'm going to use this file yet but lmfao
    I guess we'll just set it up here for now. 

Author: OCdt Brown and OCdt Velasco
Date: 7 Feb 2024

"""


# --- Import Libraries ---

import pickle
import os
import mimetypes
import time;


# --- Define Functions ---

def pull_public_files():
    """ This function pulls the public files stored in the pub_files.pickle file. """

    # Create temporary solution of returning a large string with the uploaded file info 
    ret_html = "";

    # Open the pickled file for public files and populate our python dict
    PUB_FILES = {};
    try: 
        pub_pickle = open('html/pub_files.pickle', 'rb');
        PUB_FILES = pickle.loads(pub_pickle.read());
        pub_pickle.close();
    except Exception as e:
        print(f"\nCouldn't open pickle path. Likely doesn't exist. {e}")

    # Iterate through pulled public files and return links to browsePublic.html for them to press and view the file in question. 
    for file_name, file_data in PUB_FILES.items():
        ret_html += f"<a href='viewPublic.html?name={file_name}'>{file_name}</a><br>"
        
    # Return the html
    return ret_html;


def pull_private_files():
    """ This function pulls the private files stored in the priv_files.pickle file. """

    # Create temporary solution of returning a large string with the uploaded file info 
    ret_html = "";

    # Open the pickled file for public files and populate our python dict
    PRIV_FILES = {};
    try: 
        priv_pickle = open('html/priv_files.pickle', 'rb');
        PRIV_FILES = pickle.loads(priv_pickle.read());
        priv_pickle.close();
    except Exception as e:
        print(f"\nCouldn't open pickle path. Likely doesn't exist. {e}")

    # Iterate through pulled public files and return links to browsePublic.html for them to press and view the file in question. 
    for file_name, file_data in PRIV_FILES.items():
        ret_html += f"<a href='viewPrivate.html?name={file_name}'>{file_name}</a><br>"
        
    # Return the html
    return ret_html;


# --- MAIN for testing ---
if __name__ == "__main__":
    pass;
