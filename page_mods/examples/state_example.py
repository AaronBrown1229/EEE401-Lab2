import pickle

_STATE = {}

try:
    f = open('html/state.pickle','rb')
    _STATE = pickle.loads(f.read())
except:
    pass

def get_state():
    global _STATE
    return _STATE

def save_new_val(new_vals):
    global _STATE
    for key,val in new_vals.items():
        _STATE[key] = val
    if len(_STATE) == 0:
        _STATE[0] = 1
    else:
        int_keys = [i for i in _STATE.keys() if type(i) == int]
        if len(int_keys) == 0:
            next_key = 0
        else:
            next_key = max(int_keys)+1
        _STATE[next_key] = next_key +1
        
def save_state():
    global _STATE
    try:
        f = open('html/state.pickle','wb')
        f.write(pickle.dumps(_STATE))
    except Exception as e:
        print(f"couldn't save state, exception:{e}")
