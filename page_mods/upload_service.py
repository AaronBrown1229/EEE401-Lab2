import pickle
import os

class file:
    def __init__(self, name: str,comment: str,pub: bool):
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

def upload_data(POST_DATA):
    # put the data into a dir with a unique id
    print(POST_DATA)
    # return the class created for the file

def save_upload(new_file: file):
    # this is very unfinished as I am currently confused on what is happening but I will return tomorrow and finish it then
    if new_file.pub == True:
        jar = open('public.pickle', 'wb')
        jar.write(pickle.dumps(new_file))
