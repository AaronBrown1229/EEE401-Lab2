
"""

Description: 

    This file contains the python logic that retrieves the links to the public and private
    uploaded files from the pickle jar and returns html links to them to the calling web
    page. 


Author: OCdt Brown and OCdt Velasco
Date: 7 Feb 2024

"""


# --- Import Libraries ---

import pickle
import os
import mimetypes
import time;


# --- Define Functions ---

def retrieve_file_links(public):
    """ This function returns links to the private/public files in the database. """

    # Create temporary solution of returning a large string with the uploaded file info 
    ret_html = "";
    PICKLE_JAR = {}; 

    if public: 

        try: 
            pub_pickle = open('html/pub_files.pickle', 'rb');
            PICKLE_JAR = pickle.loads(pub_pickle.read());
            pub_pickle.close();
        except Exception as e:
            print(f"\nCouldn't open pickle path. Likely doesn't exist. {e}")

    else: 

        try: 
            priv_pickle = open('html/priv_files.pickle', 'rb');
            PICKLE_JAR = pickle.loads(priv_pickle.read());
            priv_pickle.close();
        except Exception as e:
            print(f"\nCouldn't open pickle path. Likely doesn't exist. {e}")
    
    # Check if the pickle jar was empty
    if len(PICKLE_JAR) == 0: 
        return "<p>There are currently no uploaded files here.";

    # Iterate through pulled files and return links to appropriate html page 
    # for the user to view the links from. 
    for file_name, file_data in PICKLE_JAR.items():
        if public: 
            ret_html += f"<a href='viewPublic.html?name={file_name}'>{file_name}</a><br>"
        else: 
            ret_html += f"<a href='viewPrivate.html?name={file_name}'>{file_name}</a><br>"

    # return the HTML
    return ret_html; 

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


