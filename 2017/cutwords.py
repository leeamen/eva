#!/usr/bin/python
#coding:utf-8
import mybaselib
import logging
import jieba
import jieba.analyse
import numpy as np
import csv
import sys
import stat
import os
import re
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Row(object):
  def __init__(self, row):
    arr = filter(lambda x:len(x.strip()) > 0, re.split(' ', row))
    if len(arr) is not 2:
      print 'row:',row
      sys.exit()

    self.sentence = arr[0]
    self.class_label = arr[1]
  def GetSentence(self):
    return self.sentence
  def GetClassLabel(self):
    return self.class_label

def walktree(dirname, callback, userdata):
  for f in os.listdir(dirname):
    pathname = os.path.join(dirname, f)
    mode = os.stat(pathname).st_mode
    if stat.S_ISDIR(mode):
      pass
      # It's a directory, recurse into it
      #walktree(pathname, callback)
    elif stat.S_ISREG(mode):
      # It's a file, call the callback function
      callback(pathname, userdata)
    else:
      # Unknown file type, print a message
      logger.error('Skipping %s', pathname)
def cutwords(filename, userdata):
  if '.txt' != filename[-4:]:
    return
  logger.debug('start process file:%s', filename)
  wf = open(userdata['output'], 'a')
  with open(filename, 'rb') as rf:
    while True:
      line = rf.readline()
      if line is None or len(line) == 0:
        break;
      row = Row(line)
      sentence = row.GetSentence()
      #切词
      cut_list = jieba.lcut(sentence, cut_all = False)
      wf.write(' '.join(cut_list) + '\n')
  wf.flush()
  wf.close()

if __name__ == '__main__':
  #加载自定义词典
  jieba.load_userdict('./data/userdict.data')
  sentence = '该类会将文本中的词语转换为词频矩阵'
  sentence = '春川辣炒鸡排外表是古典的吗?'
  print '|'.join(jieba.lcut(sentence, cut_all = False))
  #所有txt文件切词
  userdata = {}
  userdata['output'] = './data/all.cuts'
  os.system('rm -f ./data/all.cuts')
  walktree('data', cutwords, userdata)

  sys.exit()

#  jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=())
  #自己设置语料库
#  corpus_file = '***.corpus'
#  tags = jieba.analyse.extract_tags('该类会将文本中的词语转换为词频矩阵', topK=5)
#  print '|'.join(tags)
  filename = sys.argv[1]
  wf = open(filename + '.cuts', 'wb')
  with open(filename, 'rb') as rf:
    while True:
      line = rf.readline()
      if line is None or len(line) == 0:
        break;
      row = mybaselib.Row(line)
      sentence = row.GetSentence()
      sentence = sentence.strip()
      #切词
      cut_list = jieba.lcut(sentence, cut_all = False)
      wf.write(' '.join(cut_list) + ' ')
  wf.flush()
  wf.close()

