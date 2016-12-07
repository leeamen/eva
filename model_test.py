#!/usr/bin/python
#coding:utf-8 
import mylog
import myequation
import logging
import os.path
import sys
import multiprocessing
reload(sys)
sys.setdefaultencoding('utf8')

from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
    logger.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 2:
        print globals()['__doc__'] % locals()
        sys.exit(1)

    model_vector_file = sys.argv[1]
    logger.debug('文件名:%s', model_vector_file)
    model = Word2Vec.load_word2vec_format(model_vector_file, binary = False)
    print model.similarity('泡菜'.decode('utf8'), '蛋糕'.decode('utf8'))
    print model['泡菜'.decode('utf8')]
    print myequation.Cosine(model['泡菜'.decode('utf8')], model['蛋糕'.decode('utf8')])

