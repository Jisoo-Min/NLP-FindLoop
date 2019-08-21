import numpy
import time
import sys
import subprocess
import os
import random
import pprint
import numpy as np
sys.path.append(".")
from is13.data import load
from is13.data import load_mydata
from is13.rnn.elman import model
from is13.metrics.accuracy import conlleval
from is13.utils.tools import shuffle, minibatch, contextwin

##########################################################
#
# This code is from https://github.com/mesnilgr/is13
# It has custom changes
#
##########################################################


if __name__ == '__main__':


    # Settings for data, RNN, and training
    s = {'fold':3, # 5 folds 0,1,2,3,4
         'lr':0.0627142536696559,
         'verbose':1,
         'decay':False, # decay on the learning rate if improvement stops
         'win':7, # number of words in the context window
         'bs':9, # number of backprop through time steps
         'nhidden':100, # number of hidden units
         'seed':345,
         'emb_dimension':500, # dimension of word embedding, default:100
         'nepochs':5} #default: 50


    folder = os.path.basename(__file__).split('.')[0]
    if not os.path.exists(folder): os.mkdir(folder)
   

    # Set labels we use
    idx2label = {0: "B_2param", 1: "B_2param2", 2: "B_3param",  3: "B_param", 
                4: "B_param2",  5: "B_param3",  6: "I_2param",  7: "I_2param2", 
                8: "I_3param",  9: "I_param",   10: "I_param2", 11: "O"}

    # Load vacabulary set
    vocaset = load_mydata.get_voca()

    # Make (idx: word) sets from vocabulary set
    idx2word = { i : vocaset[i] for i in range(0, len(vocaset)) }


    # Load the dataset
    train_lex, train_y = load_mydata.get_data("train")
    valid_lex, valid_y = load_mydata.get_data("valid")
    test_lex,  test_y  = load_mydata.get_data("test")

    # Set vacabulary size, classes, and size of dataset
    vocasize = 1485
    nclasses = 12
    nsentences = len(train_lex)

    # Instanciate the model
    numpy.random.seed(s['seed'])
    random.seed(s['seed'])
    rnn = model(    nh = s['nhidden'],
                    nc = nclasses,
                    ne = vocasize,
                    de = s['emb_dimension'],
                    cs = s['win'] )

    # Train with early stopping on validation set
    best_f1 = -numpy.inf

    s['clr'] = s['lr']
    for e in range(s['nepochs']):
        # shuffle
        shuffle([train_lex, train_y], s['seed'])
        s['ce'] = e
        tic = time.time()
        for i in range(nsentences):
            cwords = contextwin(train_lex[i], s['win'])

            words  = map(lambda x: numpy.asarray(x).astype('int32'),\
                         minibatch(cwords, s['bs']))

            labels = train_y[i]

            for word_batch , label_last_word in zip(words, labels):
                rnn.train(word_batch, label_last_word, s['clr'])
                rnn.normalize()
            if s['verbose']:
                print ('[learning] epoch %i >> %2.2f%%'%(e,(i+1)*100./nsentences),'completed in %.2f (sec) <<\r'%(time.time()-tic),
                sys.stdout.flush())

        # Evaluation // back into the real world : idx -> words
        predictions_test = [ map(lambda x: idx2label[x], \
                             rnn.classify(numpy.asarray(contextwin(x, s['win'])).astype('int32')))\
                             for x in test_lex ]

        groundtruth_test = [ map(lambda x: idx2label[x], y) for y in test_y ]

        words_test = [ map(lambda x: idx2word[x], w) for w in test_lex]

        predictions_valid = [ map(lambda x: idx2label[x], \
                             rnn.classify(numpy.asarray(contextwin(x, s['win'])).astype('int32')))\
                             for x in valid_lex ]

        groundtruth_valid = [ map(lambda x: idx2label[x], y) for y in valid_y ]
        words_valid = [ map(lambda x: idx2word[x], w) for w in valid_lex]

        # Evaluation // compute the accuracy using conlleval.pl
        res_test  = conlleval(predictions_test, groundtruth_test, words_test, folder + '/current.test.txt')
        res_valid = conlleval(predictions_valid, groundtruth_valid, words_valid, folder + '/current.valid.txt')

        if res_valid['f1'] > best_f1:
            rnn.save(folder)
            best_f1 = res_valid['f1']
            if s['verbose']:
                print ('NEW BEST: epoch', e, 'valid F1', res_valid['f1'], 'best test F1', res_test['f1'], ' '*20)
            s['vf1'], s['vp'], s['vr'] = res_valid['f1'], res_valid['p'], res_valid['r']
            s['tf1'], s['tp'], s['tr'] = res_test['f1'],  res_test['p'],  res_test['r']
            s['be'] = e
            subprocess.call(['mv', folder + '/current.test.txt', folder + '/best.test.txt'])
            subprocess.call(['mv', folder + '/current.valid.txt', folder + '/best.valid.txt'])
        else:
            print ('')

        # Learning rate decay if no improvement in 10 epochs
        if s['decay'] and abs(s['be']-s['ce']) >= 10: s['clr'] *= 0.5
        if s['clr'] < 1e-5: break

    print ('BEST RESULT: epoch', e, 'valid F1', s['vf1'], 'best test F1', s['tf1'], 'with the model', folder)

