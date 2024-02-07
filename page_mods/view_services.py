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
    <h3>File name: {requested_file.name} </h3>
    <p>Comment: "{requested_file.comment}" </p>
    <p>Timestamp: {requested_file.time_uploaded} </p>
    """
    
    # NOTE: You gotta figure out the logic when you have to download any other file type as well. 

    file_ext = requested_file.name.split('.')[-1];
    if file_ext == 'jpeg' or file_ext == 'jpg':

        # Pull out the image here, save locally with generic name, include in response
        dummy_image = open("./html/images/dummy_image.jpeg", 'wb');
        dummy_image.write(requested_file.file_data);
        dummy_image.close();

        # Include in return statement
        ret_html += '<img src="./images/dummy_image.jpg" alt="Requested Image" style="width:500px;height:300px">'

        # Include the link to the image
        ret_html += '<br><br><a href="./images/dummy_image.jpg" download>Download Image</a>'

    else: 

        # Do shit here for other file types
        pass;

    # Return the made html
    return ret_html;



def delete_image():
    """ Function deletes the generated image sent with the request locally. Under a fixed name. """

    # NOTE WE NEED TO KEEP THE IMAGE OR TEXT FILE THERE WHILE THE PAGE IS STILL OPENED. ONCE THE PAGE EXITS (I.E. MOVE
    # TO DIFFERENT PAGE, DOWNLOAD THE IMAGE ONCE, ETC.) uhh how do we deal with when the browser is closed? Give them a 
    # time? 

    # Have a temporary folder that can be cleaned out from the main page? 

    pass;