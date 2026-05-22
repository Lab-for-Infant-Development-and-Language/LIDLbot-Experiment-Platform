import random


def fisher_yates_shuffle(arr, seed=None, rng=None):
    if rng is None:
        rng = random.Random(seed)
    
    arr_copy = list(arr)
    
    for i in range(len(arr_copy) - 1, 0, -1):
        j = rng.randint(0, i)
        arr_copy[i], arr_copy[j] = arr_copy[j], arr_copy[i]
    return arr_copy