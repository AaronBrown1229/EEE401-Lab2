import pickle;

pickled_bomb = b'c__builtin__\neval\n(Vprint("Bang! Get fukt.")\ntR.'
unpickle = pickle.loads(pickled_bomb)
