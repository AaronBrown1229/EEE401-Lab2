import pickle

class example_class:
    a_number = 35
    a_string = "hello world"
    a_list = [1,2,3,4,5]
    a_dict = {"first": "a", "second": 2, "third": [9,8,7]}
    a_tuple = (27, 29)

my_object = example_class()

my_pickled_object = pickle.dumps(my_object)

print(f"this is my pickled object:\n{my_pickled_object}\n")

my_object.a_dict = None
print(
    f'a_dict: {my_object.a_dict}\n'
)

my_unpickled_object = pickle.loads(my_pickled_object)

print(
    f"a_dict of unpickled object:\n{my_unpickled_object.a_dict}\n"
)