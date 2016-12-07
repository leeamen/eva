#!/usr/bin/python
#coding:utf-8

import mylog
import logging
import os.path
import sys
import multiprocessing
reload(sys)
sys.setdefaultencoding('utf-8')

from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
    logger.setLevel(level=logging.INFO)

    logger.info("running %s" % ' '.join(sys.argv))
 
    # check and process input arguments
    if len(sys.argv) < 4:
        print globals()['__doc__'] % locals()
        sys.exit(1)

    #outp1:模型,outp2:模型转向量
    inp, outp1, outp2 = sys.argv[1:4]
    lines = LineSentence(inp), 
#    print lines

    model = Word2Vec(LineSentence(inp), size=2, window=5, min_count=2,
            workers=multiprocessing.cpu_count())

#    model.init_sims(replace=True)
    # trim unneeded model memory = use(much) less RAM
    #model.init_sims(replace=True)
    model.save(outp1)
    model.save_word2vec_format(outp2, binary=False)
#    model.similarity('蛋糕'.decode('utf8'), '饭店'.decode('utf8'))
#    #print model.index2word[10].decode('utf8')
#    print model.most_similar('蛋糕'.decode('utf8'))
