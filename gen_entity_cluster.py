#!/usr/bin/python
#coding:utf-8
import mylog
import myltpmodel as myltp
import logging
import jieba
import jieba.analyse
import numpy as np
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
  sentence = '该类会将文本中的词语转换为词频矩阵'
  sentence = '南池市场有哪几个米其林餐厅?'
  print '|'.join(jieba.lcut(sentence, cut_all = False))

#  jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=())
  #自己设置语料库
#  corpus_file = '***.corpus'
#  tags = jieba.analyse.extract_tags('该类会将文本中的词语转换为词频矩阵', topK=5)
#  print '|'.join(tags)

  filename = sys.argv[1]
#  rawdata = np.loadtxt(filename , dtype = np.object)
#  label_data = rawdata[:,0:4]
#  sentence_data = rawdata[:,4:]
  wf = open(filename + '.cluster', 'wb')
  all_data = {}
  with open(filename, 'rb') as rf:
    while True:
      line = rf.readline()
      if line is None or len(line) == 0:
        break;
      row = myltp.Row(line)
      for key in row.ParamKeys():
        if all_data.has_key(key) is False:
          all_data[key] = []
        #logger.debug('%s:%s', key, row.ParamValue(key))
        all_data[key].append(row.ParamValue(key))
  for key in all_data.keys():
    wf.write(key + ' ')
    wf.write(' '.join(all_data[key]) + '\n')
  wf.flush()
  wf.close()

