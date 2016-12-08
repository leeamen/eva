#!/usr/bin/python
#coding:utf-8 
import mylog
import myequation
import logging
import os.path
import sys
import numpy as np
import multiprocessing
import gen_entity_cluster as mygen_entity_cluster
import jieba
reload(sys)
sys.setdefaultencoding('utf8')

from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

class Word(object):
  def __init__(self, word, vector):
    self.word = word
    self.vector = vector
  def GetVector(self):
    return self.vector
  def GetWord(self):
    return self.word

class EntityCluster(object):
  def __init__(self, name):
    self.words = []
    #向量
    self.centroid = None
    self.name = name
  def GetName(self):
    return self.name
  def CalcCentroid(self):
    logger.debug('%s 中词的个数:%d', self.name, len(self.words))
    total = None
    if len(self.words) > 0:
      word = self.words[0]
      total = np.zeros(word.GetVector().shape[0], dtype = word.GetVector().dtype)
    else:
      logger.debug('%s 中没有词', self.name)
      return None
    for word in self.words:
      total += word.GetVector()
    self.centroid = np.array(total/len(self.words))
    return self.centroid
  def Add1Word(self, word):
    self.words.append(word)
  def GetCentroid(self):
    return self.centroid
  def GetSize(self):
    return len(self.words)

#获取实体类cluster
def Gen1Cluster(model, all_data, cluster_name):
  cluster = EntityCluster(cluster_name)
  words_list = all_data[cluster_name].keys()
  for word in words_list:
#    logger.debug('%s', word)
    if word.decode('utf8') in model:
  #    logger.debug('%s', word)
      cluster.Add1Word(Word(word, model[word.decode('utf8')]))
  #计算中心
  cluster.CalcCentroid()
  logger.debug('%s 中心:%s', cluster.GetName(), str(cluster.GetCentroid()))
  return cluster

def most_similar(word, model, clusters):
  if word.decode('utf8') not in model:
    return None,None
  similarity = -1
  cluster_name = None
  for cluster in clusters:
    if cluster.GetSize() <= 0:
      continue
    simi = myequation.Cosine(model[word.decode('utf8')], cluster.GetCentroid())
    logger.debug('相似度:%f', simi)
    if similarity <= simi:
      similarity = simi
      cluster_name = cluster.GetName()
  return cluster_name, similarity

def GenAnswer(sentence, model, clusters):
  final_parameters = {}
  threashold = 0.6
  cut_list = jieba.lcut(sentence, cut_all = False)
  logger.debug('%s', '|'.join(cut_list))
  for word in cut_list:
    cluster_name, similarity = most_similar(word, model, clusters)
    if similarity >= threashold:
      logger.debug('word:%s most_similar:%s %f', word, cluster_name, similarity)
      final_parameters[cluster_name] = word
  #结果
  logger.debug('%s ', sentence)
  for key in final_parameters.keys():
    logger.debug('%s=%s', key, final_parameters[key])

if __name__ == '__main__':
  program = os.path.basename(sys.argv[0])
  logger = logging.getLogger(program)
  logger.setLevel(level=logging.DEBUG)
  logger.info("running %s" % ' '.join(sys.argv))

  # check and process input arguments
  if len(sys.argv) < 3:
      print globals()['__doc__'] % locals()
      sys.exit(1)

  model_vector_file,sample_file = sys.argv[1:3]
  logger.debug('vectors文件名:%s', model_vector_file)
  logger.debug('sample文件名:%s', sample_file)
  model = Word2Vec.load_word2vec_format(model_vector_file, binary = False)
#  print model.similarity('泡菜'.decode('utf8'), '蛋糕'.decode('utf8'))
#  print model['泡菜'.decode('utf8')]
#  print myequation.Cosine(model['泡菜'.decode('utf8')], model['蛋糕'.decode('utf8')])
  all_cluster_data = mygen_entity_cluster.GetEntityClustersData(sample_file)
  clusters = [Gen1Cluster(model, all_cluster_data, cluster_name) for cluster_name in all_cluster_data.keys()]
  logger.debug('%d', len(clusters))
  
  sentence = '土俗村参鸡汤的芥末章鱼好吗'
  GenAnswer(sentence, model, clusters)

