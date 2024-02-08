""" 
Description:

    This file shall contain the python functions that will pull a requested file (public or private) 
    from the database and return the info regarding the requested information in html to the browsePublic.html 
    or browsePrivate.html pages. 

Author: OCdt Brown and OCdt Velasco
Date: 7 Feb 2024
"""

# --- Importing libraries ---

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
        return "<h2>ERROR: Requested file does not exist.</h3>"
    
    # Find the requested file by its name in public files, extract its data
    requested_file = PUB_FILES[requested_name];
    ret_html = f"""
    <p><b>File name</b>: {requested_file.name} </p>
    <p><b>Comment</b>: "{requested_file.comment}" </p>
    <p><b>Time Uploaded</b>: {time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(requested_file.time_uploaded))} </p>
    """

    # Pull the requested file from database, save it temporarily,  
    file_ext = requested_file.name.split('.')[-1];
    temp_name = f"downloaded-{requested_file.name}"
    temp_path = f"./html/temp_folder/{temp_name}"
    with open(temp_path, 'wb') as temp_file:
        temp_file.write(requested_file.file_data);
    
    # If file was an image, also embed an image link to it in html. 
    if file_ext == 'jpeg' or file_ext == 'jpg':
        ret_html += f'<img src="./temp_folder/{temp_name}" alt="Requested Image" style="width:500px;height:300px">'

    # Include a link to download it in the html.
    ret_html += f'<br><br><a href="./temp_folder/{temp_name}" download>Download File</a>'

    # Return the made html
    return ret_html;



def delete_image():
    """ Function deletes the generated image sent with the request locally. Under a fixed name. """

    # NOTE WE NEED TO KEEP THE IMAGE OR TEXT FILE THERE WHILE THE PAGE IS STILL OPENED. ONCE THE PAGE EXITS (I.E. MOVE
    # TO DIFFERENT PAGE, DOWNLOAD THE IMAGE ONCE, ETC.) uhh how do we deal with when the browser is closed? Give them a 
    # time? 

    # Have a temporary folder that can be cleaned out from the main page? 

    pass;