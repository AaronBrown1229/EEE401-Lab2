
"""

Description:
    
    This module is dedicated to the testing of the private page of the web process.
    This is to be conducted using the python request library. 
    In short, this is used to confirm that private files are not available through the public view page. 


Author: OCdt Aaron Brown and OCdt Liethan Velasco
Date: 12 Feb 2024

"""

# --- Importing Libraries ---

import os;
import requests;


# --- Defining Global Variables ---

priv_file = "cooldude.jpeg"
nonexist_file = "amonguslol.txt"


# --- Main ---

if __name__ == "__main__":

    # Craft a query to the view private page for the squidward file named "cooldude.jpeg"
    priv_params = {'name' : priv_file}
    priv_resp = requests.get("http://127.0.0.1:8080/viewPrivate.html", params = priv_params);
    print(priv_resp.text);
    if "ERROR" not in priv_resp.text:
        print(f"\n>>> Confirmed file named {priv_file} exists in the private files.")
    else:
        print(f"\n>>> Private file {priv_file} does not exist in the private files!")

    # Craft a query to the private page for a file that does not exist
    priv_params = {'name' : nonexist_file}
    priv_resp = requests.get("http://127.0.0.1:8080/viewPrivate.html", params = priv_params);
    print(priv_resp.text);
    if "ERROR" in priv_resp.text:
        print(f"\n>>> Confirmed no file named {nonexist_file} exists in the private files.<<<");
    else:
        print(f"\n>>> The non-existent file {nonexist_file} exists in the private files?!<<<");

    # Craft a query to the view public page for the same squidward private file named "cooldude.jpeg"
    pub_params = {'name' : priv_file}
    pub_resp = requests.get("http://127.0.0.1:8080/viewPublic.html", params = pub_params);
    print(pub_resp.text);
    if "ERROR" not in pub_resp.text:
        print(f"\n>>> ERROR: The private file {priv_file} was accessible from the public page! <<<");
    else: 
        print(f"\n>>> Confirmed the private file {priv_file} is not accessible from public page. <<<");

