#!/usr/bin/python
#coding:utf-8 
import mltoolkits.mylog as mylog
import myltpmodel as myltp
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

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logger.setLevel(level=logging.INFO)

from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

class Word(object):
  def __init__(self, word, vector):
    self.word = word
    self.vector = vector
  def GetVector(self):
    return self.vector
  def GetWordName(self):
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
  def __str__(self):
    str_name = self.name
    str_words = ''
    for word in self.words:
      str_words += word.GetWordName()+','
    return str_name + str_words

class SentModel(object):
  def __init__(self):
    self.sample_file = None
    self.userdict_file = None
    self.model_vector_file = None
    self.rules_file = None

    self.return_rules = None
    self.word2vec_model = None
    self.all_cluster_data = None
    self.clusters = None
  def Load(self, userdict, model_vector, sample, rules):
    self.sample_file = sample
    self.userdict_file = userdict
    self.model_vector_file = model_vector
    self.rules_file = rules
    #加载词典
    jieba.load_userdict(self.userdict_file)
    #加载返回类型规则
    self.return_rules = self.GenReturnRules(self.rules_file)
    #加载词向量文件
    self.word2vec_model = Word2Vec.load_word2vec_format(self.model_vector_file, binary = False)
  #  print model.similarity('泡菜'.decode('utf8'), '蛋糕'.decode('utf8'))
  #  print model['泡菜'.decode('utf8')]
  #  print myequation.Cosine(model['泡菜'.decode('utf8')], model['蛋糕'.decode('utf8')])
    #从样本文件获取所有参数实体类
    self.all_cluster_data = mygen_entity_cluster.GetEntityClustersData(self.sample_file)
    self.clusters = [self.Gen1Cluster(self.word2vec_model, self.all_cluster_data, cluster_name) for cluster_name in self.all_cluster_data.keys()]
#    for cluster in self.clusters:
#      logger.debug('%s', cluster)
    logger.debug('%d', len(self.clusters))


  #获取实体类cluster
  @classmethod
  def Gen1Cluster(self, model, all_data, cluster_name):
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

  #获取返回类型
  @classmethod
  def GenReturnRules(self, fname):
    rules = myltp.ReturnRules()
    if rules.Load(fname) is None:
      return None
    return rules

  @classmethod
  def MostSimilarCluster(self, word, model, clusters):
    if word.decode('utf8') not in model:
      return None,None
    similarity = -1
    cluster_name = None
    for cluster in clusters:
      if cluster.GetSize() <= 0:
        continue
      simi = myequation.Cosine(model[word.decode('utf8')], cluster.GetCentroid())
      logger.debug('%s,类名:%s,相似度:%f',word, cluster.GetName(), simi)
      if similarity <= simi:
        similarity = simi
        cluster_name = cluster.GetName()
    return cluster_name, similarity

  def GenParamAndReturntype(self, sentence):
    return self.GenAnswer(sentence, self.word2vec_model, self.clusters, self.return_rules)

  @classmethod
  def GenAnswer(self, sentence, model, clusters, return_rules):
    final_parameters = {}
    threashold = 0.6
    cut_list = jieba.lcut(sentence, cut_all = False)
    logger.debug('%s', '|'.join(cut_list))
    for word in cut_list:
      cluster_name, similarity = self.MostSimilarCluster(word, model, clusters)
      if similarity >= threashold:
        logger.debug('word:%s MostSimilarCluster:%s %f', word, cluster_name, similarity)
        final_parameters[cluster_name] = word
    #返回类型
    return_type = return_rules.GetReturnType(sentence)
    #输出结果
    logger.debug('%s ', sentence)
    for key in final_parameters.keys():
      logger.debug('%s=%s', key, final_parameters[key])
    logger.debug('返回类型:%s', return_type)
    return final_parameters, return_type

  def GenHttpInterface(self, sentence):
    final_parameters = {}
    threashold = 0.6
    cut_list = jieba.lcut(sentence, cut_all = False)
    logger.debug('%s', '|'.join(cut_list))
    for word in cut_list:
      cluster_name, similarity = self.MostSimilarCluster(word, self.word2vec_model, self.clusters)
      if similarity >= threashold:
        #logger.debug('word:%s MostSimilarCluster:%s %f', word, cluster_name, similarity)
        final_parameters[cluster_name] = word
    #返回类型
    return_type = self.return_rules.GetReturnType(sentence)
    http = 'http://114.55.35.16:8080/AQAInterface/canyin_answer?'
    for key in final_parameters.keys():
      http += 'attr_name=' + key + '&' + 'attr_value=' + final_parameters[key] + '&'
    http += 'returnType=' + return_type
    return http

if __name__ == '__main__':
  logger.info("running %s" % ' '.join(sys.argv))

  # check and process input arguments
  if len(sys.argv) < 5:
      print '参数少'
      sys.exit(1)

  model_vector_file,userdict_file, sample_file,rules_file = sys.argv[1:5]
  logger.debug('词向量文件名:%s', model_vector_file)
  logger.debug('样例文件名:%s', sample_file)
  logger.debug('用户词典文件名:%s', userdict_file)
  logger.debug('返回类型规则文件名:%s', rules_file)

  #加载词典
  jieba.load_userdict(userdict_file)
  #加载返回类型规则
  return_rules = SentModel.GenReturnRules(rules_file)
  #加载词向量文件
  model = Word2Vec.load_word2vec_format(model_vector_file, binary = False)
#  print model.similarity('泡菜'.decode('utf8'), '蛋糕'.decode('utf8'))
#  print model['泡菜'.decode('utf8')]
#  print myequation.Cosine(model['泡菜'.decode('utf8')], model['蛋糕'.decode('utf8')])
  #从样本文件获取所有参数实体类
  all_cluster_data = mygen_entity_cluster.GetEntityClustersData(sample_file)
  clusters = [SentModel.Gen1Cluster(model, all_cluster_data, cluster_name) for cluster_name in all_cluster_data.keys()]
  logger.debug('%d', len(clusters))

  #测试用例
  sentence = '温莎市的土俗村参鸡汤有什么好吃的'
  SentModel.GenAnswer(sentence, model, clusters, return_rules)

  while True:
    sentence = raw_input('输入句子:')
    SentModel.GenAnswer(sentence, model, clusters, return_rules)

