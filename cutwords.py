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
import stat
import os
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def walktree(dirname, callback):
  for f in os.listdir(dirname):
    pathname = os.path.join(dirname, f)
    mode = os.stat(pathname).st_mode
    if stat.S_ISDIR(mode):
      pass
      # It's a directory, recurse into it
      #walktree(pathname, callback)
    elif stat.S_ISREG(mode):
      # It's a file, call the callback function
      callback(pathname)
    else:
      # Unknown file type, print a message
      logger.error('Skipping %s', pathname)
def cutwords(filename):
  if '.txt' != filename[-4:]:
    return
  logger.debug('文件进行切词:%s', filename)
  wf = open('./data/all.cuts', 'a')
  with open(filename, 'rb') as rf:
    while True:
      line = rf.readline()
      if line is None or len(line) == 0:
        break;
      row = myltp.Row(line)
      sentence = row.GetSentence()
      #切词
      cut_list = jieba.lcut(sentence, cut_all = False)
      wf.write(' '.join(cut_list) + '\n')
  wf.flush()
  wf.close()

if __name__ == '__main__':
  sentence = '该类会将文本中的词语转换为词频矩阵'
  sentence = '南池市场有哪几个米其林餐厅?'
  print '|'.join(jieba.lcut(sentence, cut_all = False))
  walktree('data', cutwords)
  sys.exit()
#  jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=())
  #自己设置语料库
#  corpus_file = '***.corpus'
#  tags = jieba.analyse.extract_tags('该类会将文本中的词语转换为词频矩阵', topK=5)
#  print '|'.join(tags)

  filename = sys.argv[1]
  #'user_tag_query.2W.TRAIN.csv'
#  rawdata = np.loadtxt(filename , dtype = np.object)
#  label_data = rawdata[:,0:4]
#  sentence_data = rawdata[:,4:]
  wf = open(filename + '.cuts', 'wb')
  with open(filename, 'rb') as rf:
    while True:
      line = rf.readline()
      if line is None or len(line) == 0:
        break;
      row = myltp.Row(line)
      sentence = row.GetSentence()
      sentence = sentence.strip()
      #切词
      cut_list = jieba.lcut(sentence, cut_all = False)
      wf.write(' '.join(cut_list) + '\n')
  wf.flush()
  wf.close()

