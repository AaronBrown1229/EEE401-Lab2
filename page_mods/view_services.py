""" 
Description:

    This file shall contain the python functions that will pull a requested file (public or private) 
    from the database and return the info regarding the requested information in html to the browsePublic.html 
    or browsePrivate.html pages. 

Author: OCdt Brown and OCdt Velasco
Date: 7 Feb 2024
"""

# --- Importing libraries ---

import subprocess;
import os; 
import pickle;
import time;


# The fallowing is an example of what POST_DATA looks like
# {b'file_data': [({b'content-type': b' text/plain', b'name': b'file_data', b'filename': b'test.txt'}, b'test\n')], b'comment': [({b'name': b'comment'}, b'hi')], b'pub_or_priv': [({b'name': b'pub_or_priv'}, b'Private')]}

# --- Defining Functions ---

def pull_public_data(QUERY_VARS):
    """ Function returns in HTML the requested file information through the POST_DATA. """

    # Pull the name from the query 
    requested_name = QUERY_VARS['name'][0];

    # Open the pickled file for public files and populate our python dict
    PUB_FILES = {};
    try: 
        pub_pickle = open('html/pub_files.pickle', 'rb');
        PUB_FILES = pickle.loads(pub_pickle.read());
        pub_pickle.close();
    except Exception as e:
        print(f"\nCouldn't open pickle path. Likely doesn't exist. {e}")

    # Check if file exists. Print error accordingly
    if requested_name not in PUB_FILES.keys():
        return "<h2>ERROR: Requested file does not exist.</h3>";
    
    # Find the requested file by its name in public files, extract its data
    requested_file = PUB_FILES[requested_name];
    cowsay_comment = subprocess.run(f"cowsay {requested_file.comment}", shell = True, capture_output = True).stdout.decode();
    ret_html = f"""
    <p><b>File name</b>: {requested_file.name} </p>
    <p><b>Time Uploaded</b>: {time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(requested_file.time_uploaded))} </p>
    <p><b>Comment</b>:{requested_file.comment}<br></p> 
    <p><pre>{cowsay_comment}</pre><br></p> 
    """

    # Pull the requested file from database, save it temporarily,  
    file_ext = requested_file.name.split('.')[-1];
    temp_name = f"downloaded-{requested_file.name}";
    temp_path = f"./html/temp_folder/{temp_name}";
    with open(temp_path, 'wb') as temp_file:
        temp_file.write(requested_file.file_data);
    
    # If file was an image, also embed an image link to it in html. 
    if file_ext == 'jpeg' or file_ext == 'jpg':
        ret_html += f'<img src="./temp_folder/{temp_name}" alt="Requested Image" style="width:500px;height:300px">'

    # Include a link to download it in the html.
    ret_html += f'<br><br><a href="./temp_folder/{temp_name}" download>Download File</a>'

    # Return the made html
    return ret_html;


def pull_private_data(QUERY_VARS):
    """ Function returns in HTML the requested file information through the POST_DATA.
    
    "I'm making a private version of this to make development for future labs more convenient. Also because
    it gives us a way to know to pull from the priv_files.pickle file. We could probably do some refactoring.

    """

    # Pull the name from the query 
    requested_name = QUERY_VARS['name'][0];

    # Open the pickled file for public files and populate our python dict
    PRIV_FILES = {};
    try: 
        priv_pickle = open('html/priv_files.pickle', 'rb');
        PRIV_FILES = pickle.loads(priv_pickle.read());
        priv_pickle.close();
    except Exception as e:
        print(f"\nCouldn't open pickle path. Likely doesn't exist. {e}")

    # Check if file exists. Print error accordingly
    if requested_name not in PRIV_FILES.keys():
        return "<h2>ERROR: Requested file does not exist.</h3>";
    
    # Find the requested file by its name in public files, extract its data
    requested_file = PRIV_FILES[requested_name];
    cowsay_comment = subprocess.run(f"cowsay {requested_file.comment}", shell = True, capture_output = True).stdout.decode();
    ret_html = f"""
    <p><b>File name</b>: {requested_file.name} </p>
    <p><b>Time Uploaded</b>: {time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(requested_file.time_uploaded))} </p>
    <p><b>Comment</b>:{requested_file.comment}<br></p> 
    <p><pre>{cowsay_comment}</pre><br></p> 
    """

    # Pull the requested file from database, save it temporarily,  
    file_ext = requested_file.name.split('.')[-1];
    temp_name = f"downloaded-{requested_file.name}";
    temp_path = f"./html/temp_folder/{temp_name}";
    with open(temp_path, 'wb') as temp_file:
        temp_file.write(requested_file.file_data);
    
    # If file was an image, also embed an image link to it in html. 
    if file_ext == 'jpeg' or file_ext == 'jpg':
        ret_html += f'<img src="./temp_folder/{temp_name}" alt="Requested Image" style="width:500px;height:300px">'

    # Include a link to download it in the html.
    ret_html += f'<br><br><a href="./temp_folder/{temp_name}" download>Download File</a>'

    # Return the made html
    return ret_html;



def flush_temp_folder():
    """ This function flushes out the temp_folder of all files when called. Is called in every page."""

    # NOTE This is a good solution when there is a small amount of pages in the web application, i.e. in a dynamic 
    # website. This becomes a concern however once the number of pages scale up, because that means this function
    # has to included in each new webpage created, introducing another hassle. I can't seem to find a way to call it 
    # automatically without having to modify demowww.py. 
    # NOTE OOP, THIS DOESN'T GET CALLED WHEN THE 'GO BACK PAGE' BUTTON IS PRESSED. NEED A BETTER SOLUTION. 

    for this_file in os.listdir('./html/temp_folder'):
        os.remove('./html/temp_folder/' + str(this_file));
