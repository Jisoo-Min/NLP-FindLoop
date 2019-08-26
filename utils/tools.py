import random


##########################################################
#
# This code is from https://github.com/mesnilgr/is13
#
##########################################################



'''suffle
@lol : list of list as input
@ seed : seed the shuffling

shuffle inplace each list in the same order
'''
def shuffle(lol, seed):
    for l in lol:
        random.seed(seed)
        random.shuffle(l)



"""minibatch
@l : list of word idxs
@bs : batch size

return a list of minibatches of indexes
which size is equal to bs
border cases are treated as follow:
eg: [0,1,2,3] and bs = 3
will output:
[[0],[0,1],[0,1,2],[1,2,3]]
"""
def minibatch(l, bs):
    out  = [l[:i] for i in range(1, min(bs,len(l)+1) )]
    out += [l[i-bs:i] for i in range(bs,len(l)+1) ]
    assert len(l) == len(out)
    return out



"""contextwin
@win : int corresponding to the size of the window 
       given a list of indexes composing a sentence
@l : list of word idxs

return a list of list of indexes corresponding
to context windows surrounding each word in the sentence

"""
def contextwin(l, win):

    
    assert (win % 2) == 1
    assert win >=1
    l = list(l)
    
 
    lpadded = int(win/2) * [-1] + l + int(win/2) * [-1]
    out = [ lpadded[i:i+win] for i in range(len(l)) ]

    assert len(out) == len(l)
    return out


