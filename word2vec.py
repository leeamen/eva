#!/usr/bin/python
#coding:utf-8

import mybaselib
import logging
import os
import sys
import multiprocessing
import gensim
import jieba.analyse
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')

#from gensim.corpora import WikiCorpus
#from gensim.models import Word2Vec
#from gensim.models.word2vec import LineSentence

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

def word2vec(inp, outp1, outp2):
  sentences = gensim.models.word2vec.LineSentence(inp)
#  bigram_transformer = gensim.models.Phrases(sentences, delimiter = '')
#  model = gensim.models.Word2Vec(bigram_transformer[sentences], size=100, window=2, min_count=1,
#            workers=multiprocessing.cpu_count())
  model = gensim.models.Word2Vec(sentences, size=100, window = 2, min_count=1,
            workers=multiprocessing.cpu_count())
    #model.init_sims(replace=True)
    # trim unneeded model memory = use(much) less RAM
    #model.init_sims(replace=True)
  model.save(outp1)
  model.save_word2vec_format(outp2, binary=False)
  return model

def tfidf(inp):
  model = gensim.models.tfidfmodel.TfidfModel(corpus)
  logger.debug('%s', model)
  return model

if __name__ == '__main__':
  logger.info("running %s" % ' '.join(sys.argv))
 
  # check and process input arguments
  if len(sys.argv) < 4:
      logger.error('参数少')
      sys.exit(1)
  #inp:句子切词后的文件, outp1:模型,outp2:模型转向量
  inp, outp1, outp2 = sys.argv[1:4]
  model = word2vec(inp, outp1, outp2)
#  logger.debug('%f', model.similarity('蛋糕'.decode('utf8'), '饭店'.decode('utf8')))
  #print model.index2word[10].decode('utf8')

  #tfidf
#  inp = ''
#  tfidf_model = tfidf(inp)
#
