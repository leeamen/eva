#!/usr/bin/python
#coding:utf8

#美化
import sys
import xml.etree.cElementTree as et
import os
import re
#import pyltp as ltp
import time
import csv

reload(sys)
sys.setdefaultencoding('utf-8')

import logging
logging.basicConfig(level=logging.INFO,
    format='[%(asctime)s %(msecs)03d][%(name)-10.10s:%(lineno)03d][%(funcName)-15.15s][%(levelname)s] %(message)s',
    datefmt = '%F %T')

#返回类型
class Rules(object):
  def __init__(self):
    self.rules = {}
  def Load(self, fname):
    with open(fname, 'rb') as rf:
      try:
        reader = csv.reader(rf, delimiter = ' ', quotechar = ' ')
        for row in reader:
          self.rules[row[0]] = row[1]
      except:
        return None
#    for key in self.rules.keys():
#      print key, self.rules[key]
    return self.rules

  def GetValue(self, key):
    if self.rules.has_key(key):
      return self.rules[key]
    return None
class ParamRules(Rules):
  def __init__(self):
    Rules.__init__(self)

class ReturnRules(Rules):
  def __init__(self):
    Rules.__init__(self)
    self.default_key = 'default'
  def GetReturnType(self, sentence):
    for key in self.rules.keys():
      if key in sentence:
        return self.rules[key]
    return self.rules[self.default_key]

class Row(object):
  def __init__(self, row):
    self.row = row

    #参数表
    self.parameter = {}

    #
    self.array = filter(lambda x:len(x.strip()) > 0, re.split('{|}', self.row))
    self.return_type = None

    self.sentence = self.array[0].strip()
    param = self.array[1]
    for a in param.split(','):
      try:
        key = a.split('=')[1].strip()
        value = a.split('=')[0].strip()
        self.parameter[key] = value
      except:
        #参数列表有空的:{}
        print '参数列表为空:%s'%(row)
        #返回类型为第二个
        self.return_type = self.array[1].strip()
        break
    if self.return_type is None:
      self.return_type = self.array[2].strip()
    #参数列表处理，取一个
    if '/' in self.return_type or ']' in self.return_type:
     # print self.return_type
      arr = filter(lambda x:len(x.strip()) > 0, re.split('\[|\]|/', self.return_type))
      if len(arr) > 0:
        self.return_type = arr[-1]
     #   print self.return_type
#        time.sleep(2)
  def GetSentence(self):
    return self.sentence

  def ParamKeys(self):
    return self.parameter.keys()

  def ParamValue(self, key):
    try:
      return self.parameter[key]
    except:
      return None
  def GetRetureType(self):
    return self.return_type

