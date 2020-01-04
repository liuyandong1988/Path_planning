#! /usr/bin/python

def randomIntList(size, seed=1, maxInt=2000000000):
    '''
    Return a list of random numbers

    Arguments:
        size - size of list to return
        seed - random seed - using default gives repeatable results
        maxInt - max int value to return (default is 2,000,000,000)
    Returns:
        list of 'size' random numbers between 0 and max
    '''
    import random

    intList = []

    # Seed the random number generator - mostly important to allow
    # caller to get identical lists repeatedly
    random.seed(seed)

    for i in range(size):
        intList.append(int(maxInt * random.random()))

    return intList  

