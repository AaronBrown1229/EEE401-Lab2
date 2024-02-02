import pickle
import os

class file:
    def __init__(self, name: bytes,comment: bytes, pub: bool, content_type: bytes):
        file_counter_file = open("file_counter.txt", "r")
        file_counter = int(file_counter_file.read())
        file_counter_file.close()
        file_counter_file = open("file_counter.txt", "r+")
        file_counter_file.write(str(file_counter + 1))
        file_counter_file.close
        self.id = file_counter
        self.name = name
        self.comment = comment
        self.pub = pub
        self.content_type = content_type

# The fallowing is an example of what POST_DATA looks like
# {b'file_data': [({b'content-type': b' text/plain', b'name': b'file_data', b'filename': b'test.txt'}, b'test\n')], b'comment': [({b'name': b'comment'}, b'hi')], b'pub_or_priv': [({b'name': b'pub_or_priv'}, b'Private')]}
def upload_data(POST_DATA: dict):
    # might want to consider if getting a post request that is not of exctype "multipart/form-data"

    # create the class to represent the file
    print(POST_DATA[b'file_data'][0][1])
    if POST_DATA[b'pub_or_priv'][0][0][b'name'] == b"Private":
        new_file = file(POST_DATA[b'file_data'][0][0][b'filename'], POST_DATA[b'comment'][0][1], False, POST_DATA[b'file_data'][0][0][b'content-type'])
    else:
        new_file = file(POST_DATA[b'file_data'][0][0][b'filename'], POST_DATA[b'comment'][0][1], True, POST_DATA[b'file_data'][0][0][b'content-type'])

    # put the data into a dir with a unique id
    return new_file
    # return the class created for the file

# This is not finished and just for testing
def save_data(new_file: file):
    # this is very unfinished as I am currently confused on what is happening but I will return tomorrow and finish it then
    if new_file.pub == True:
        jar = open('public.pickle', 'wb')
        jar.write(pickle.dumps(new_file))
    
    return "<p>Test</p>"
