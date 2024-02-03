import pickle
import os
import mimetypes

class file:
    def __init__(self, name: bytes,comment: bytes, pub: bool, content_type: bytes):
        # NOTE might want to make this a random number as then it is even harder for an attacker to find their uploaded file on the server
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
    # NOTE the content type is [1:] because for some reason it gives a space before???
    print(POST_DATA[b'pub_or_priv'][0][1])
    if POST_DATA[b'pub_or_priv'][0][1] == b'Private':
        new_file = file(POST_DATA[b'file_data'][0][0][b'filename'], POST_DATA[b'comment'][0][1], False, POST_DATA[b'file_data'][0][0][b'content-type'][1:])
    else:
        new_file = file(POST_DATA[b'file_data'][0][0][b'filename'], POST_DATA[b'comment'][0][1], True, POST_DATA[b'file_data'][0][0][b'content-type'][1:])

    file_extension = mimetypes.guess_extension(new_file.content_type.decode())
    # TODO handle NONE cases

    # put the data into a dir with a unique id
    if new_file.pub:
        file_path = "public_files/" + str(new_file.id) + file_extension
        pickle_path = "public_pickle" + str(new_file.id) + ".pickle"
    else:
        file_path = "private_files/" + str(new_file.id) + file_extension
        pickle_path = "private_pickle" + str(new_file.id) + ".pickle"

    pickled_object = pickle.dumps(new_file)
    # Creates and saves the pickle
    with open(pickle_path, 'bw') as A5:
        A5.write(pickled_object)

    # calling linux open command
    file_obj = os.open(file_path, os.O_WRONLY | os.O_CREAT, 0o600)
    # writing to file
    with open(file_obj,'wb') as A6:
        A6.write(POST_DATA[b'file_data'][0][1])